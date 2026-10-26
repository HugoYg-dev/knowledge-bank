---
title: "DeepSeek开源FlashMLA之际从原理到代码详解MLA"
source: "https://mp.weixin.qq.com/s/qHAv6u-SwlU4CRQcanoL3g"
author:
  - "[[探知轩]]"
published:
created: 2026-10-26
description:
tags:
  - "clippings"
---
杜凌霄 探知轩 *2025年2月24日 19:51*

## 前言

2025-2-24，DeepSeek如期开源FlashMLA。这是一个使用类似FlashAttention的MLA(**M** ulti-head **L** atent **A** ttention)实现，底层使用Cutlass模板库实现计算kernel。

本文第一部分简要介绍FlashMLA，第二部分详细介绍DeepSeek的MLA算法。

## FlashMLA

FlashMLA: https://github.com/deepseek-ai/FlashMLA

开源五个小时已经收到了4.8K star和204 fork。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_jpg/oCEiaaLlGGWdpu04glWa7IYicPibxt3qP59OSGib2DRC6X3yCwiclPhDBaWaiazZv7rQUms1ibyS5635SkKiadeDfHrC4A/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

**支持的GPU**

目前只支持Hopper GPUs，代码里面专门检查过

```
// mha_fwd_kvcache_mla()
auto dprops = at::cuda::getCurrentDeviceProperties();
bool is_sm90 = dprops->major == 9 && dprops->minor == 0;
TORCH_CHECK(is_sm90);
```

**数据类型**

目前只支持BF16，同样，代码里面强制检查

```
// mha_fwd_kvcache_mla()
auto q_dtype = q.dtype();
TORCH_CHECK(q_dtype == torch::kBFloat16);
TORCH_CHECK(kcache.dtype() == q_dtype, "query and key must have the same dtype");
```

**安装**

先置条件：

- Hopper GPUs
- CUDA 12.3 and above
- PyTorch 2.0 and above
```
>> git clone https://github.com/deepseek-ai/FlashMLA/
>> cd FlashMLA
>> python setup.py install
```

**使用**

整个库对外接口很简洁，只有两个接口：

**get\_mla\_metadata**

- 函数签名：
	```
	get_mla_metadata(cache_seqlens: torch.Tensor, 
	                 num_heads_per_head_k: int, 
	                 num_heads_k: int) -> Tuple[torch.Tensor, torch.Tensor]
	```
- 参数
- **cache\_seqlens**: \[batch\_size, 1\]，标记每个batch里面的输入序列长度；
	- **num\_heads\_per\_head\_k**: 通过计算得到，其中表示MTP(**m** lti- **T** oken **P** rediction)的值，表示query里面attention head的数量，表示MQA里面group数量；
	- **num\_heads\_k**: 就是上面的，示MQA里面group数量。
- 返回
- **tile\_scheduler\_metadata**: (num\_sm\_parts, TileSchedulerMetaDataSize), dtype torch.int32.
	- **num\_splits**: (batch\_size + 1), dtype torch.int32.

**flash\_mla\_with\_kvcache**

- 函数签名
	```
	flash_mla_with_kvcache(
	    q: torch.Tensor,
	    k_cache: torch.Tensor,
	    block_table: torch.Tensor,
	    cache_seqlens: torch.Tensor,
	    head_dim_v: int,
	    tile_scheduler_metadata: torch.Tensor,
	    num_splits: torch.Tensor,
	    softmax_scale: Optional[float] = None,
	    causal: bool = False,
	) -> Tuple[torch.Tensor, torch.Tensor]
	```
- 参数
- **q**: (batch\_size, seq\_len\_q, num\_heads\_q, head\_dim)，输入query
	- **k\_cache**: (num\_blocks, page\_block\_size, num\_heads\_k, head\_dim).
	- **block\_table**: (batch\_size, max\_num\_blocks\_per\_seq), torch.int32.
	- **cache\_seqlens**: (batch\_size), torch.int32.
	- **head\_dim\_v**: Head\_dim of v.
	- **tile\_scheduler\_metadata**: (num\_sm\_parts, TileSchedulerMetaDataSize), torch.int32, return by get\_mla\_metadata.
	- **num\_splits**: (batch\_size + 1), torch.int32, return by get\_mla\_metadata.
	- **softmax\_scale**: float. The scaling of before applying softmax. Default to 1 / sqrt(head\_dim).
	- **causal**: bool. Whether to apply causal attention mask.
- 返回
- **out**: (batch\_size, seq\_len\_q, num\_heads\_q, head\_dim\_v)，输出token
	- **softmax\_lse**: (batch\_size, num\_heads\_q, seq\_len\_q), torch.float32，输出的是

使用范例：

```
from flash_mla import get_mla_metadata, flash_mla_with_kvcache

tile_scheduler_metadata, num_splits = get_mla_metadata(cache_seqlens, s_q * h_q // h_kv, h_kv)

for i in range(num_layers):
    ...
    o_i, lse_i = flash_mla_with_kvcache(
        q_i, kvcache_i, block_table, cache_seqlens, dv,
        tile_scheduler_metadata, num_splits, causal=True,
    )
    ...
```

## MLA

## Multi-Head Attention

我们令表示embedding的维度，表示attention head的数量，表示一个attention head的维度，表示attention head的数量， 表示第个token在某个attention模块的输入。对于标准的 **MHA** (**M** ultiple **H** ead **A** ttention)来说，会首先生成：

虽然使用一个完整的矩阵在做计算，实际上确实多个头的计算矩阵concat在一起做计算而已：

对于其中一个head来说

把以多头形式可以写成

其中表示第个attention head的query，key和value。

Attention的计算可以表示为

其中表示output projection matrix。

公式(7)需要使用历史上所有的，我们把它写成矩阵形式

对于位置以及以后的token来说，的计算都是重复的。为了减少计算量，我们可以把它们存储起来，这就是K-Cache。也是一样，我们同样可以存储起来。我们把存储的K和V缓存一起叫做KV-Cache。对于一个总共层模型，每个token一共需要缓存个元素。个token需要缓存个元素，如果每个元素都使用fp16或者bf16，那么需要个byte的存储。如果我们进一步把batch size考虑在里面，那么需要的存储是。很显然，如果比较大或者(batch size)比较大，KV-Cache将会变得特别大。

## 低秩分解

我们再仔细观察一下里面的每个变量，看哪些部分能够让我们减少存储空间。

- ：batch size如果减小，那么单次读取的weight能够处理的对象就少了，我们一般想让batch size尽量大；
- : 其实这一个是可以减少的。很多KV Cache压缩的算法会去profile哪些head对生成更加重要，进而为它们分配更多的cache空间，那些不重要的就减少空间或者干脆不分配。另外非常出名的MQA采用一个layer的所有head的都共享一个和的方式来减少；在观察到MQA精度损失比较大的情况下提出了GQA(Grouped-Query Attention)，一个group的head共享一个和，和的head数量从减少到个，也就是group数目这么多个。整体来说，这是一个非常活跃的研究领域；
- : 模型的总层数。其实也有一部分研究通过比较输入输出的embedding的相似性来判断某一层是否重要，从而把一些不重要的层进行剪枝。这可以同事达到减少模型weight和KVCache的作用；
- : 序列长度。这是KV-Cache压缩领域研究最多的点。目前大致分为两个大方向：
- 基于retrieval的方法：把KVCache offload到cpu，以页或者聚类的形式组织，q和每个页或者聚类的通过一些代价比较小的方法，比如和聚类重点算attention score等，来得到是否使用这个页或者聚类，每次只把得分的top-k个部分加载到显存计算；
	- 抛弃不重要的token：通过attention score或者attention的系数特征来判别不重要的token，然后把这些token对应的KV都抛弃掉。这部分研究跟LLM的量化一样，都在activation outlier提出来之后取得了比较大的进展，也是属于目前比较主流的KVCache研究方向；
- ：这是一个head的size。其实本文主要的研究对象MLA(Multi-Head Latent Attention)就是主要在这个维度上想办法，我们将在本文后面详细介绍。

想要减少，一种很容易想到的方法就是 **低秩分解(Low-Rank Decomposition) **，毕竟** LORA** 就是利用的这个思想。我们可以如下对和队形低秩压缩：

其中是压缩后的同时为key和value服务的latent vector，表示的是KV压缩之后的维度。表示down-projection矩阵；分别表示key和value的up-projection矩阵。

在上面的这种分解下，KVCache中其实只需要保存就可以了，这是一个远远小于的向量，单个token只需要保存个元素。

为了进一步消减训练的时候的activation memory，论文作者把query也进行了低秩压缩：

其中是query压缩后的latent vector；表示query压缩之后的维度；, 是query的down-projection矩阵和up-projection矩阵。

**压缩原理** ：因为可以使用压缩的回复没有压缩的，所以KV-Cache中只需要存储 即可。

## 当低秩压缩遇上ROPE

ROPE(**Ro** tary **P** osition **E** mbedding )现在基本上已经统治了LLM，它是对绝对位置编码(Absolute Position Embedding)和相对位置编码(Releative Position Embedding)的改进。笼统地说，它需要给query和key向量都施加一个位置相关的旋转矩阵：

我们现在来计算它们之间的点积

从上面公式就可以看出，和各自的位置息息相关，没有办法吸收到前面和后面任何一个矩阵里面。换句话说，这种情况下， **只存储来压缩KV-Cache的路行不通了** 。

现在的困境就成了：

- 如果不使用ROPE位置编码，可以极大节省KV-Cache，但是模型效果不好。哪怕是用ALIBI这样的位置编码，效果都不如ROPE好；
- 如果使用ROPE位置编码，模型效果好，但是没有办法节省KV-Cache。

为了走出这个困境，DeepSeek提出了一种折中的方法：

**为都增加一个额外的维度来添加ROPE编码，之前的维度不使用ROPE编码，总长度变为。**

其中，共享一个额外的RoPE向量，来为所有的head增加一个位置编码的投影，为query的每个头都增加一个用做RoPE编码的投影。

其实是把下面的带标准RoPE的流程

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/oCEiaaLlGGWdpu04glWa7IYicPibxt3qP59MXEMWLYGS7CrVMicaW69IR1BQWLNmSgBs3UGgeHmOqDic8bvhgwwCAOQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

转变为

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/oCEiaaLlGGWdpu04glWa7IYicPibxt3qP59EOdwNoyxvXeREibxxXTUtDdmdmC7CwaDLe4wFiaHHaBgvaOr8ZfyTBNg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

我们把公式进行总结，归结为下面的一系列公式：

**KV-Cache显存节省**

MHA需要个byte的显存来存储KV-Cache；而MLA需要，只要，那么就会节省很多显存。

## 实现差异

DeepSeek现在一共有是三个版本的MLA实现：

- FlashMLA： 使用Cutlass实现；
- DeepseekV2Attention： from https://huggingface.co/deepseek-ai/DeepSeek-V2/blob/main/modeling\_deepseek.py
- MLA: from https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py

FlashMLA底层完全使用C++实现，本文不做代码具体分析。V2中的DeepseekV2Attention的实现本质上和V3中的native一样， **其实并没有节省KV-Cache** ，V3版本的非native版本是跟论文一致，节省了显存。下面我们直接先看加了注释的代码，然后再详细解释，期望搞懂真实代码实现：

```
# from: https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py
class MLA(nn.Module):
    """
    Multi-Headed Attention Layer (MLA).

    Attributes:
        dim (int): Dimensionality of the input features.
        n_heads (int): Number of attention heads.
        n_local_heads (int): Number of local attention heads for distributed systems.
        q_lora_rank (int): Rank for low-rank query projection.
        kv_lora_rank (int): Rank for low-rank key/value projection.
        qk_nope_head_dim (int): Dimensionality of non-positional query/key projections.
        qk_rope_head_dim (int): Dimensionality of rotary-positional query/key projections.
        qk_head_dim (int): Total dimensionality of query/key projections.
        v_head_dim (int): Dimensionality of value projections.
        softmax_scale (float): Scaling factor for softmax in attention computation.
    """
    def __init__(self, args: ModelArgs):
        super().__init__()
        self.dim = args.dim
        self.n_heads = args.n_heads
        self.n_local_heads = args.n_heads // world_size
        # 对应 query 压缩后的隐向量的维度 d'_c
        self.q_lora_rank = args.q_lora_rank
        # 对应 key-value 压缩后的隐向量维度 d_c
        self.kv_lora_rank = args.kv_lora_rank
        # 表示query和key的向量中应用rope部分的维度, $d_h$
        self.qk_nope_head_dim = args.qk_nope_head_dim
        # 对应$d_h^R$， 表示应用了rope的 queries 和 key 的一个 head 的维度。
        self.qk_rope_head_dim = args.qk_rope_head_dim
        # $d_h + d_h^R$, 注意力头大小为非rope部分大小加上rope部分大小
        self.qk_head_dim = args.qk_nope_head_dim + args.qk_rope_head_dim
        self.v_head_dim = args.v_head_dim

        # 不适用低秩分解，回归到传统MHA
        if self.q_lora_rank == 0:
            self.wq = ColumnParallelLinear(self.dim, self.n_heads * self.qk_head_dim)
        else:
            # 其实就是$W^{DQ}$，用来生成$c_t^Q$
            self.wq_a = Linear(self.dim, self.q_lora_rank)
            self.q_norm = RMSNorm(self.q_lora_rank)
            # $W^{UQ}$
            self.wq_b = ColumnParallelLinear(self.q_lora_rank, self.n_heads * self.qk_head_dim)
        # $ [W^{DKV}; W^{KR}] $
        self.wkv_a = Linear(self.dim, self.kv_lora_rank + self.qk_rope_head_dim)
        self.kv_norm = RMSNorm(self.kv_lora_rank)
        # $ [W^{UK}; W^{UV}] $
        self.wkv_b = ColumnParallelLinear(self.kv_lora_rank, self.n_heads * (self.qk_nope_head_dim + self.v_head_dim))
        self.wo = RowParallelLinear(self.n_heads * self.v_head_dim, self.dim)
        self.softmax_scale = self.qk_head_dim ** -0.5
        if args.max_seq_len > args.original_seq_len:
            mscale = 0.1 * args.mscale * math.log(args.rope_factor) + 1.0
            self.softmax_scale = self.softmax_scale * mscale * mscale

        # native模式下，kvcache存储的是没有压缩的数据，大小为d_h + d_h^R, 不但没有节省，反而增加了显存消耗
        if attn_impl == "naive":
            self.register_buffer("k_cache", torch.zeros(args.max_batch_size, args.max_seq_len, self.n_local_heads, self.qk_head_dim), persistent=False)
            self.register_buffer("v_cache", torch.zeros(args.max_batch_size, args.max_seq_len, self.n_local_heads, self.v_head_dim), persistent=False)
        # 在非native模式下，存储的是压缩的c，大小为d_c
        else:
            self.register_buffer("kv_cache", torch.zeros(args.max_batch_size, args.max_seq_len, self.kv_lora_rank), persistent=False)
            self.register_buffer("pe_cache", torch.zeros(args.max_batch_size, args.max_seq_len, self.qk_rope_head_dim), persistent=False)

    def forward(self, x: torch.Tensor, start_pos: int, freqs_cis: torch.Tensor, mask: Optional[torch.Tensor]):
        """
        Forward pass for the Multi-Headed Attention Layer (MLA).

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, seq_len, dim).
            start_pos (int): Starting position in the sequence for caching.
            freqs_cis (torch.Tensor): Precomputed complex exponential values for rotary embeddings.
            mask (Optional[torch.Tensor]): Mask tensor to exclude certain positions from attention.

        Returns:
            torch.Tensor: Output tensor with the same shape as the input.
        """
        bsz, seqlen, _ = x.size()
        end_pos = start_pos + seqlen
        if self.q_lora_rank == 0:
            q = self.wq(x)
        else:
            q = self.wq_b(self.q_norm(self.wq_a(x)))
        q = q.view(bsz, seqlen, self.n_local_heads, self.qk_head_dim)
        q_nope, q_pe = torch.split(q, [self.qk_nope_head_dim, self.qk_rope_head_dim], dim=-1)
        q_pe = apply_rotary_emb(q_pe, freqs_cis)
        kv = self.wkv_a(x)
        kv, k_pe = torch.split(kv, [self.kv_lora_rank, self.qk_rope_head_dim], dim=-1)
        k_pe = apply_rotary_emb(k_pe.unsqueeze(2), freqs_cis)
        if attn_impl == "naive":
            q = torch.cat([q_nope, q_pe], dim=-1)
            kv = self.wkv_b(self.kv_norm(kv))
            kv = kv.view(bsz, seqlen, self.n_local_heads, self.qk_nope_head_dim + self.v_head_dim)
            k_nope, v = torch.split(kv, [self.qk_nope_head_dim, self.v_head_dim], dim=-1)
            k = torch.cat([k_nope, k_pe.expand(-1, -1, self.n_local_heads, -1)], dim=-1)
            self.k_cache[:bsz, start_pos:end_pos] = k
            self.v_cache[:bsz, start_pos:end_pos] = v
            scores = torch.einsum("bshd,bthd->bsht", q, self.k_cache[:bsz, :end_pos]) * self.softmax_scale
        else:
            wkv_b = self.wkv_b.weight if self.wkv_b.scale isNoneelse weight_dequant(self.wkv_b.weight, self.wkv_b.scale, block_size) 
            wkv_b = wkv_b.view(self.n_local_heads, -1, self.kv_lora_rank)
            q_nope = torch.einsum("bshd,hdc->bshc", q_nope, wkv_b[:, :self.qk_nope_head_dim])
            self.kv_cache[:bsz, start_pos:end_pos] = self.kv_norm(kv)
            self.pe_cache[:bsz, start_pos:end_pos] = k_pe.squeeze(2)
            scores = (torch.einsum("bshc,btc->bsht", q_nope, self.kv_cache[:bsz, :end_pos]) +
                      torch.einsum("bshr,btr->bsht", q_pe, self.pe_cache[:bsz, :end_pos])) * self.softmax_scale
        # 运用causal mask
        if mask isnotNone:
            scores += mask.unsqueeze(1)
        scores = scores.softmax(dim=-1, dtype=torch.float32).type_as(x)
        if attn_impl == "naive":
            x = torch.einsum("bsht,bthd->bshd", scores, self.v_cache[:bsz, :end_pos])
        else:
            x = torch.einsum("bsht,btc->bshc", scores, self.kv_cache[:bsz, :end_pos])
            x = torch.einsum("bshc,hdc->bshd", x, wkv_b[:, -self.v_head_dim:])
        x = self.wo(x.flatten(2))
        return x
```

实际操作为

- native模式
- 非native模式

可以看到，非native模式才是符合论文的。

## 参考资料

\[1\]. FlashMLA：https://github.com/deepseek-ai/FlashMLA

\[2\]. DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model

\[3\]. DeepSeek-V3 Technical Report

\[4\]. Huggingface Deepseek V2: https://huggingface.co/deepseek-ai/DeepSeek-V2

\[5\]. Github Deepseek V3: https://github.com/deepseek-ai/DeepSeek-V3/

**微信扫一扫赞赏作者**

DeepSeek · 目录

闪记

复制 LaTeX 公式