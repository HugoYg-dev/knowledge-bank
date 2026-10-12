---
title: "MTFM：美团统一推荐基座大模型在外卖多业务场景的落地实践 | 美团 · 技术团队"
source: "https://tech.meituan.com/2026/09/22/Meituan-Foundation-Model-for-Recommendation.html"
author:
published:
created: 2026-10-10
description: "美团在 MTGR 基础上提出统一推荐基座大模型 MTFM，首次实现外卖多个主要业务的统一精排模型。"
tags:
  - "clippings"
---
![MTFM：美团统一推荐基座大模型在外卖多业务场景的落地实践](https://p0.meituan.net/meituantechblog/77b54a39ba4d36c8718ec7a410dfd93c889437.jpg)

> 美团在 MTGR 基础上提出统一推荐基座大模型 MTFM，首次实现外卖多个主要业务的统一精排模型。围绕规模可扩展性、场景可延展性与架构高效性三大挑战，MTFM以异构 Tokenizer 与动态掩码实现多场景特征免对齐，通过混合注意力与 Target Scale-Up 提升模型 Scaling 能力，借鉴 LLM 优化实践提升深层网络训练效果，并以 User-Level 训练范式与定制算子保证系统开销可控。美团外卖多个业务订单量提升 2.06%~6.68% 不等，推理成本降低 24%，相关工作已被 KDD 2026 收录。

## 1\. 引言

我们去年提出了 MTGR <sup>[1]</sup> —— 一种新的生成式精排框架，在美团外卖推荐场景验证了 Scaling Law 的有效性，并取得显著业务收益。然而，推荐领域的 Scaling Law 探索往往局限于单场景内部，模型被限制在单场景孤岛中，跨场景的数据、算力和架构无法充分复用。在美团这一问题尤为突出，推荐覆盖外卖首页、拼好饭等多个业务场景，各场景长期独立建模。与此同时，大语言模型（LLM）已验证一条清晰路径：基座模型（Foundation Model）足以统一处理编程、数学、写作等多领域任务，也可以将文本、图像、语音等异构信息表示为 Token 序列并进行端到端学习，展现出了强泛化性与可扩展性。因此，我们认为美团推荐的下一个阶段关键在于打通跨场景的异构性，充分利用多场景数据提升 Scaling Law 的上限，即建设统一推荐基座大模型。

推荐基座大模型主要面临三个核心挑战：规模可扩展性（Scalability）、场景可延展性（Extensibility）和架构高效性（Efficiency）。规模可扩展性要求模型在参数规模、数据量扩大时，效果能够稳定、可预期地提升；场景可延展性要求模型能够低成本适配已有场景或接入新场景；架构高效性要求模型在处理多场景的海量数据时，训推仍保持可接受成本开销。

为解决上述挑战，我们在 MTGR 的基础上，提出美团统一推荐基座大模型 **MTFM（Meituan Foundation Model for Recommendation）** 。MTFM 使用类 Transformer 骨干进行端到端建模，提出 Target Token Scale-Up 提升模型能力，借鉴 LLM 实践优化深层网络训练策略；通过异构 Tokenizer 替代固定特征模板，支持多场景异构特征免显式对齐；提出 Self-Attention 和 Target Attention 堆叠的混合架构，结合 User-Level 样本和 GPU 算子优化提升训推效率。

**MTFM 首次实现外卖多个主要业务的统一精排模型并在各核心场景完成全量，相关工作于 2026 年 5 月被 KDD 2026 接收** <sup>[2]</sup> 。

- **场景收益** ：全面超越 MTGR 或 DLRM 基线模型，各业务离线指标大幅度提升，在线效果最显著的业务线订单增长超过6%；
- **Scaling** ：在模型参数量、序列长度上展现了稳健的 Scaling 能力，为后续落地更大规模基座打下基础；
- **资源效率** ：单样本计算量达到 192 GFLOPs，对比传统 DLRM 提升数百倍，在线推理成本降低 24.0%。

## 2\. 工业界探索

**多场景建模**

核心目标是在共享跨业务用户兴趣表达的同时，兼顾不同业务间的分布差异与个性化需求。多场景建模主要沿着两条方向演进。第一类方法遵循“先同构、再解耦”的范式，通过将模型参数拆分为域共享与域特定部分。例如，STAR <sup>[3]</sup> 采用星型拓扑结构，将领域参数锚定在共享中心参数周围；M3OE <sup>[4]</sup> 进一步引入多个 MoE 模块，在通用、领域和任务层面学习层次化用户偏好；MLoRA <sup>[5]</sup> 则通过轻量化 LoRA 适配不同领域，提高参数效率。第二类方法开始探索多场景基座模型方向，通常采用“基座模型 + 专家模型”的架构，例如 ExFM <sup>[6]</sup> 将超大规模模型知识蒸馏到场景专家模型，LFM4Ads <sup>[7]</sup> 通过多粒度机制在特征与任务间迁移表示，这类方法非端到端建模、可能限制模型能力上限。

**具备 Scaling 能力的排序模型**

推荐模型 Scaling 范式主要沿着三条方向演进。第一类方法聚焦 DLRM 骨干扩容，通过扩展特定可堆叠模块实现扩展，例如 RankMixer <sup>[8]</sup> 、TokenMixer-Large <sup>[9]</sup> ，通过 Token Mixing、Per-Token FFN 与 Sparse-MoE 增强特征交互能力。第二类方法将输入特征切分成独立 Token，采用 Transformer Backbone 进行端到端统一建模。具体而言， HSTU <sup>[10]</sup> 将推荐重新定义为序列转导任务，采用高性能架构捕获用户行为模式；MTGR 在此基础上引入交叉特征与双向注意力机制，以进一步丰富特征交互；OneTrans <sup>[11]</sup> 通过金字塔式的截断策略提升训推效率。第三类方法探索生成式自回归推荐，例如 OneRec <sup>[12]</sup> ，通过 NTP 将推荐改写为序列生成任务，尝试以统一生成框架替代传统“召回-排序”架构。

## 3\. MTFM 模型

MTFM 的模型架构如图 1 所示，支持多场景统一建模，面向基座模型的三个核心属性进行创新改造：

![图1 MTFM 模型架构图](https://p0.meituan.net/meituantechblog/5dcc2af83b5b9da04717c9fcff76b69a1943722.png)

- **规模可扩展性** ：整体采用 Transformer 类 Block 堆叠作为骨干网络，并针对性进行 Target Token Scale-Up 设计，以支持用户序列与 Target 信息的 Scalability。
- **场景可延展性** ：将多域输入抽象为统一的异构 Token 序列，让模型无需人工对齐特征模板、无损地提取各场景的异构信号，并通过动态 Mask 机制对跨场景信息与时间因果关系进行可见性控制，避免信息泄漏。
- **架构高效性** ：受 LLM 混合架构启发，MTFM 引入混合注意力机制（Hybrid Target Attention），避免了 Self-Attention 平方复杂度的性能瓶颈，在少数关键层使用 Self-Attention 以维持全局依赖捕捉，主要堆叠 Target Attention 将算力分配给更加重要的 Target-Aware 计算。

### 3.1 异构 Tokenizer

MTFM 将多业务输入统一组织为三类 Token：H-Token、R-Token 与 T-Token。其中，H-Token 表示用户跨业务历史行为序列，包括商家统一序列与商品统一序列，用于建模用户长期兴趣；R-Token 表示用户近实时行为序列，包括点击、加购等行为，按行为时间戳统一排序；T-Token 表示待预估目标（商家、商品或券包），包含上下文特征、候选侧特征及交叉特征。其中，H-Token、R-Token 全业务共享，T-Token 各业务独立维护。

模型采用统一 Token 化范式：针对 H-Token、R-Token，不同序列使用序列独立 Tokenizer 完成编码；针对 T-Token，将上下文特征与候选侧特征进行拼接，再通过业务独立 Tokenizer 编码。最终，所有 H-Token、R-Token 与 T-Token 按顺序堆叠，形成统一的 Token 序列输入共享 Attention Backbone，在无需显式对齐跨业务特征体系的情况下，实现多场景统一建模。

### 3.2 动态掩码机制

为防止跨场景、时间的信息泄露，MTFM 进一步扩展 MTGR 的掩码策略。在下图 Mask 矩阵中，每一行代表当前 Token 在注意力计算时能看到序列中的哪些 Token，每一列代表当前 Token 能被哪些 Token 看到。对 H-Token、R-Token、T-Token 三类 Token，可见性如下：

- **H（History）-Token** ：可被所有 Token 看到，历史行为是全场景共享的用户上下文。
- **R（Realtime）-Token** ：按时间因果可见，实时序列内部为标准 Causal Mask，且每个 Target Token 只能看到发生在该次曝光之前的实时行为。
- **T（Target）-Token** ：只能被自身看到，同一请求内的不同候选之间互不感知。

![图2 多场景 Token 动态 Mask 示意图](https://p0.meituan.net/meituantechblog/350cda9fa75200bfba4489d29acfe0e9269575.png)

### 3.3 高效注意力架构

#### 3.3.1 注意力架构 V1：混合注意力架构

MTGR 采用多层 Full Attention 进行全序列建模，其计算复杂度随序列长度呈平方增长。统一模型包含多条千级长度序列，直接堆叠 Full Attention 会导致训练与推理成本难以接受。另一方面，推荐任务的预估结果高度依赖 Target 侧特征，已有工作（如 STCA <sup>[13]</sup> 、OneRec V2 <sup>[14]</sup> LazyDecoder）表明，Target Attention 能够以更低成本完成有效的信息提取。

基于此，MTFM V1 借鉴 LLM 中的混合 Attention 架构（Qwen3-Next <sup>[15]</sup> 、MiMo-V2-Flash <sup>[16]</sup> ），交错堆叠 Full Attention 与 Target Attention 层，以降低长序列建模复杂度。具体而言，Full Attention 层负责全序列信息聚合；Target Attention 层中，T-Token 仅以全序列 Token 为 Key/Value 执行注意力提取，不再参与全序列自注意力计算，从而显著降低计算量。在此基础上，进一步引入 GQA（Grouped-Query Attention），降低 Attention 的开销。

最终模型采用 Target:Full=3:1 的混合结构，共 16 层（4 个 Block，每个 Block 包含 1 层 Full Attention 与 3 层 Target Attention）。消融实验表明，该配置在各任务 GAUC 上均取得最优效果；同时由于显存占用下降，batch size 可扩大 1.7 倍，样本吞吐达到全 Full Attention 架构的 2.9 倍。

![图3 MTFM V1 混合注意力架构示意图](https://p1.meituan.net/meituantechblog/7213f9e758a9da433f5fac161359f927241435.png)

![图表1 混合架构比例消融（GAUC 为某业务场景离线指标）](https://p1.meituan.net/meituantechblog/e2b404e68769cad042d85b19d6ac694e189234.png)

#### 3.3.2 注意力架构 V2：Target Scale-Up

混合架构以更低成本取得了与全 Full Attention 相当的效果，说明将更多计算集中在 Target 侧是一条值得进一步扩展的方向。而在 MTFM 多场景长序列中，单个 Target Token 包含的特征数量，远多于单个 User Token 的特征数量，但是在 Token 化阶段 Target 和 User 侧都被视为同一维度的单个 Token，这会造成 Target 信息的过度压缩，在信息密度分配上是不合理的。因此在 MTFM V1 的混合架构基础上，MTFM V2（模型结构图见图 1）进一步对 Target Attention Layer 采用 Target Scale-Up 的方式来增大模型规模，以进一步实现 Scaling-Up。

**具体方案** ：

1、 **Target Token Embedding 构造** ：采用 AutoSplit <sup>[17]</sup> ，每个 Target 的 User & Context & Item 特征经过一层 Linear 映射到 4 个 Token Embeddings。

2、 **Per-token Q Projection & FFN** ：在 Target Attention 层，每个 Target 的 4 个 Token 经过不同的 Q Projection Matrix 和 SwiGLU FFN。

3、 **Self-Attention & Target Attention 参数分离** ：位于同一层的 Self-Attention 和 Target Attention 有独立的 QKV Projection Matrix、 SwiGLU FFN 参数。

4、 **Target Token Mixing** ：拆分后的 Target Token 各自独立与用户序列进行 Cross Attention，经过独立的 FFN，如果不进行交叉，4 个 Target Token 在 Mean Pooling 前完全没有交互，会导致各 Token 在相同 KV 下趋向学到冗余相似的表征（表征坍缩）。因此采用 RankMixer <sup>[18]</sup> 中的 Mixing 模块，以零参数低计算量对 Target Token 进行交叉，促使各 Token 学习不同的表征。

### 3.4 多场景统一训练

为了实现多业务间的知识共享与差异建模，采用“共享基座 + 业务解耦”的多任务架构。具体而言，经过混合 Attention 聚合后的各业务 T-Token 表征，被送入 MMoE 层进行跨业务信息提取，再接入业务独立的任务塔，完成 CTR、CTCVR 等目标预估。其中，长序列兴趣建模能力主要沉淀在共享 Attention Backbone 中，而不同业务的分布差异则由 MMoE 门控与任务塔参数承担。

在训练与部署层面，MTFM 采用“一图多业务”的设计范式。训练阶段，以用户为粒度聚合同一用户当日全场景曝光 Target，并共享序列侧 Attention 计算，使多个业务能够复用同一份用户兴趣表征，大幅降低长序列训练成本。线上部署阶段，各业务导出图保留共享序列基座与独享 Task Tower，使在线计算限定在当前业务相关组件上，减少无效 FLOPs 消耗，在统一建模的同时控制推理成本，实现“统一训练、多业务部署”。

实验表明，跨场景的信息迁移可有效缓解数据稀疏问题。具体体现在小流量业务显著提升 0.60~0.93pp不等，中流量业务提升 0.25pp，大流量业务持平微正。

![图表2 多业务联合训练 vs 各业务独立训练离线效果对比](https://p1.meituan.net/meituantechblog/d4297064755e2e7bdbbb028f4931f6f7154150.png)

## 4\. 统一样本与行为序列

传统 DLRM 模型以曝光（PV）为粒度构建样本，多场景样本通过固定模板强制对齐，存在序列重复存储、计算的问题，资源利用率低。MTGR 将样本组织成单用户（UV）粒度，MTFM 进一步升级为外卖全业务的统一用户粒度样本，同一用户的外卖多业务曝光聚合成 1 条样本，共享模型中最耗费算力的长序列 Attention 部分计算。

### 4.1 统一 User-Level 样本

MTFM 训练时按 User-Level 聚合样本、推理时按各业务 Request-Level 聚合候选，训练阶段算力复用经济性收益进一步放大。特征组织上，由于各业务的供给类型、展现形态不同，特征 Schema 无法直接对齐。相应地，各业务首先在内部按 User-Level 聚合业务独立特征，再与共享的用户序列以及其他业务的样本进行合并。模型训、推时多 Target 共享长序列计算，实现了算力资源的高效复用。

### 4.2 统一行为序列

过往各业务独立维护场域内的行为序列，存在数据链路和 SideInfo 体系重复建设、跨场景行为信息缺失等问题，这一问题在数据稀疏的小流量业务中尤为严重。为此，MTFM 将全场景行为统一为商家、商品长序列，聚合外卖多场景的点击、加购、完单行为，构建覆盖质、价、品、情景化信息的通用 SideInfo。受益于 4.1 节的 User-Level 训练范式升级，整体资源消耗在可控范围内。各业务均使用全场景行为信号建模，提升了用户兴趣刻画的全面性，消融实验同步显示外卖多个业务均取得显著提升。

![图表3 统一序列对比仅使用场景独立序列的消融实验](https://p1.meituan.net/meituantechblog/b6ad3f8e330af485a0bcdf079ea92d8a91064.png)

## 5\. 训练策略

多业务联合训练叠加网络层数加深，使模型优化难度显著提升。项目初期发现多组随机重复实验的离线指标波动超过 0.4pp，严重影响迭代基准的置信度。通过监控中间层激活值、参数值、梯度值等指标，完善训练动态追踪，发现离线效果与部分层的梯度大小具有强相关性（图4，Run A、B、C为模型随机重复实验），基于此判断存在局部梯度衰减、参数退化的问题。为此从初始化、优化器两个方向系统性解决。另外针对多业务联合训练范式下样本稀疏引发的梯度噪声增大、无效梯度等问题，我们改进损失函数，完善优化器逻辑、并引入梯度累积。

![图4 模型随机重复实验中训练效果与关键层梯度强度的一致性对比](https://p0.meituan.net/meituantechblog/9f4c80a7522871d9befa400d3fabb44f249068.png)

### 5.1 深层网络训练稳定性提升

深度感知的初始化策略：MTFM 的骨干网络是带有残差连接的多层 HSTU，残差结构使得网络输出的 std 随深度累积不断变大，训练初期存在激活值过大导致非线性激活层饱和的风险。借鉴 GPT-2 针对多层 Transformer 的初始化策略，在初始化 HSTU 每个 Block 的输出投影层时按深度缩放标准差：

$$
W_{o_{proj}} \sim \mathcal{N}(0,\frac{0.02}{\sqrt{L}})
$$

其中 L = 16 为本次推全模型 HSTU 总层数，其他线性层的 std 仍设置为常数 0.02——使残差分支累积后的总方差保持在相对稳定的量级，改善深层模型训练初期的梯度稳定性。

**优化器升级** ：将部分 Dense 参数由 AdamW 切换为 Muon — 一种主要面向二维矩阵参数、近年来在 LLM 领域得到广泛应用的优化器。Muon 使用 Newton-Schulz 迭代正交化更新梯度矩阵，以改善更新方向和训练效率。实践中借鉴了月之暗面的最新实践：增加 Weight Decay、Update RMS Scale，以提升训练的稳定性。我们针对 Muon 的覆盖范围进行探索，发现仅将 Muon 作用于 HSTU 的 UQKV 投影与 Output Projection，可以在速度与效果之间取得最佳平衡。

整体叠加两个优化策略，5~10 组随机实验的 train AUC 波动幅度从 0.4pp 降至 0.1pp，离线实验的稳定性和可复现性得到明显改善。

### 5.2 多业务联合训练优化

**动态归一化** ：初期的联合损失采用各业务损失分别归一化后相加的形式：

$$
L = \sum_{s} \frac{1}{|B_s|} \sum_{i \in B_s} \mathrm{loss}_i
$$

其中 $B_s$ 为 batch 内业务的样本集合。由于小流量业务的有效 batch size 小，基于其归一化损失得到的梯度存在较大噪声，既影响自身个性化参数（如 MMoE、任务塔）的收敛，也通过共享参数间接影响其他业务。为此将损失改为按 batch 内各业务 PV 占比动态加权，该形式可化简为等价的全局归一化——不区分业务、对 batch 内全部样本统一归一，修改后的 loss 形式如下：

$$
L=\frac{\sum_{s}\sum_{0\leq i \leq |B_s|-1} loss_{s,i}}{\sum_{s'}|B_{s'}|}
$$

**稀疏更新改进** ：多业务联合建模的范式下，稀疏样本带来了一个新的问题：部分 batch 内不含小流量业务的 Target，其 Tokenizer、MMoE 专家与任务塔在该步没有梯度，但这些参数仍在被持续衰减。为此在优化器的计算逻辑中跳过零梯度 Weight Decay，并将零梯度检测合并为单次批量同步、非零参数更新批量向量化以减少 kernel launch 次数提升训练吞吐。此外，为提升小业务的训练稳定性，引入步长为2的梯度累积，降低优化器 step 频率提升训练速度。

## 6\. 训推性能

MTFM 的单样本计算量较 DLRM 模型增长数百倍，系统性的性能优化是基座大模型成功落地的前提。为此，从训练、推理两部分，解决模型计算量和存储量激增带来的诸多性能挑战。

### 6.1 训练性能

- **FA 镜像与 Mask Kernel 优化** ：HSTU 动态 Attention 在 2k 长序列下，逐样本构造动态 Mask 因不连续访存与频繁 kernel launch 耗时高达 22ms。MTFM 基于 Flash-Attention V2 重构：将多维 Mask 预处理好一维 jagged mask 存入 Share Memory 供轻量读取；Mask 构造从 for-loop 改写为 Triton Kernel，降至 1ms；扩展 FA2 接口支持 Full/Target Attention、动态 Mask 读取与 SiLU 融合。相比 NVIDIA <sup>[19]</sup> 实现，优化后前向加速 128%、反向加速 152%。
- **GLN Kernel 融合** ：MTFM 序列由终身行为、实时行为、候选 Target 等多种异构 Token 拼接构成，各类型使用独立的 LayerNorm 参数。传统实现按 group 循环执行，多次 kernel launch 和冗余 global memory 读写，成为长序列训练中的瓶颈。
- **优化方案** ：前向基于 Triton 重构 Group LayerNorm（GLN）算子。将多组参数统一组织为 \[G, D\] 大矩阵，通过 seq\_group\_id\_mask 为每个 Token 动态索引对应 group，单次 kernel 完成全部 Token 归一化；同时实现 GLN-ADD 与 GLN-MUL 融合算子，避免高频的中间结果回写。反向梯度改为分块归约：各处理单元独立累积局部梯度后统一汇总，避免多 Token 并发累加同一份共享参数带来的串行排队。在 2k 长序列下，GLN 的内存带宽利用率从 30% 提升至 60% 以上，整体相对原生实现提速超过 30%。
- **Muon 性能优化** ：针对原生 Muon 优化器中 Newton-Schulz（NS）正交化逐 2D 参数串行执行、GPU 利用率低的问题，首先借鉴了 flash-muon <sup>[20]</sup> （利用 X@Xᵀ 对称性仅计算上三角，FLOP 减半）。该做法在大矩阵场景下收益明显，但 MTFM 中矩阵普遍偏小，反而因额外 Triton 启动开销拖慢性能。因此采用针对小矩阵的批处理策略：将同一优化步骤中形状相同的权重梯度堆叠为 (B, M, N) 的批量张量，整组 NS 批量并行执行。批量化后，整个 NS 阶段 kernel launch 收敛至数十次，阶段加速 241%，端到端训练吞吐提升 19%。
- **消除阻塞点** ：随着特征规模和序列长度增长，训练瓶颈正从 Attention 计算转向 Host/Device 协同效率。典型阻塞点包括 torch.unique、TorchRec wait() 同步、HashTable 优化器 step，以及业务代码如.item() 引发的 D2H 同步。
- **优化方案** ：核心思路是将“串行等待”转化为“并行重叠”。① 重构 TorchRec 数据分发和 HashTable 优化器链路，通过异步数据传输与计算重叠，削减通信、回传和更新中的闲置间隙，结合去重与截断优化降低冗余计算；② 将原先按 embedding 维度拆分的多个 HashtableCollection 融合为单个统一集合，所有特征一次性查表，消除多实例间的调度与同步开销；③ 基于 AI Agent Infra，将 repeat\_interleave 等存在 D2H 阻塞的原生算子改写为纯 GPU 实现，频繁访问的 CPU 常量迁移为 GPU Tensor 预计算。最终，MTFM 训练流水线整体训练速度提升约 15%。
- **特征精简** ：多业务统一后特征规模达 1.3K+，利用 Agent Auto Research 分析与分组搜索验证，删减近 500 个特征且 GAUC 无损，释放显存以增大 batch size，训练吞吐 +6%，线上特征处理耗时同步降低。

### 6.2 推理性能

- **查表合并** ：多个 Hashtable 查询存在同表重复加载问题，导致显存碎片严重、多表查询串行化。将多个查询共享同一张表后，显存占用由 22GB 降至 5.9GB。
- **Attention Maskfunc 规则跳算** ：在 MTFM 的 HSTU 结构中，进入 Attention 的序列可抽象为 User 和 Item 两部分，两者的 Mask 逻辑不同，对此分别做了针对性优化：
	- User 侧使用自定义 Mask（区别于 LLM 的 Causal Mask），在早期实现中，Mask 在 Attention 中以 element-wise 乘作用在 Q \* K^T 的矩阵结果，在多场景长序列中 Mask 含大量零值，计算效率极低。对此优化方案是预扫描 Mask 生成有效计算索引，在 Attention 计算过程中仅对存在有效 Key 的 Block 执行计算，跳过全零块，在长序列下单算子延迟降低约 50%。
		- Item 侧的 Mask 逻辑为 Item 可见 User，User 不可见 Item，即 User→Item 方向的 Attention 计算完全无效。利用这一可见性先验规则直接跳过该方向计算，在 2000 User + 200 Item 配置下延迟降低 13%。
- **GLN 自定义算子** ：原生 GLN 按 index 取数→归一化→写回，因 index 不连续产生大量乱序访问和显存拷贝。改为基于 Mask 的 GLN，直接通过掩码定位有效位置，避免重排开销；结合 block/warp 规约与向量化读取加速。吞吐提升 38%。
- **推理图精简** ：识别并融合冗余算子，合并连续的 Cast 转换，减少数值格式转换引发的额外内存搬运开销、降低访存压力，并重排计算顺序提升数据局部性，吞吐提升 20%。

## 7\. 模型效果

### 7.1 Scaling Law 验证

MTFM 在网络层数、Token Dim、序列长度三个维度上表现出了稳健的 Scaling 能力（图5~7）：

- 网络层数（图5）：随着模型层数增加，各业务离线效果稳步增长，离线指标与网络层数高度相关；
- Token Dim（图6）：随着 Token 维度增大，序列 SideInfo 中的丰富语义得以充分表达，同时能建模 Q、K 之间更丰富的交互关系，在 192~768 范围内观察到效果显著提升；
- 序列长度（图7）：在 400~2000 范围内序列长度 Scaling 现象明显，随着入图序列长度增长，模型能够建模更长期的用户偏好，模型离线 GAUC 稳定提升。

![图5 MTFM 网络层数 Scaling 曲线](https://p1.meituan.net/meituantechblog/f8a8f4305500f58e7589110852dee058290854.png)

![图6 MTFM Token Dim Scaling 曲线](https://p1.meituan.net/meituantechblog/4d1acda945187eff14734d3404169320294779.png)

![图7 MTFM 序列长度 Scaling 曲线](https://p0.meituan.net/meituantechblog/8cc049d8c3ebdf201c4eccbc564d8378302919.png)

### 7.2 各业务离线效果

MTFM 统一模型离线 GAUC 全面超越各场景基线，并且在 Target Token Scale-Up 上展现了更好的扩展效果。

![图表4 统一模型 vs 各业务基线模型（离线 GAUC 相对基准的提升）](https://p0.meituan.net/meituantechblog/ed0c8d75745431ea9057373dce831016165307.png)

### 7.3 各业务线上效果

目前，MTFM V1 在美团外卖多个业务完成全量，核心订单指标提升显著，在线效果最显著的业务线订单增长超过6%，同时这也是最近两年多个核心业务推荐场景单次优化的最大收益。

## 8\. 总结与展望

MTFM 是一个真正意义上实现多场景特征免对齐的推荐基座大模型架构，具备规模可扩展性（Scalability）、场景可延展性（Extensibility）和架构高效性（Efficiency）这三个关键特质。具体以类 Transformer 骨干网络为基础，通过 Target Token Scale-Up 提升模型能力，借鉴 LLM 优化实践提升训练效果；设计异构 Tokenizer 和动态掩码机制支持多场景端到端统一建模；通过混合注意力、多场景 User-Level 训练、高效 GPU 定制算子等提升训推效率。首次实现外卖多场景统一精排模型，取得显著的离线 GAUC 与在线 A/B 效果提升，展现了良好的规模效应与算力经济性。在未来，我们将和各团队紧密合作，充分吸纳 LLM 与推荐领域业界最新进展，不断提升模型能力和 Infra 能力，继续拓展基座模型在推荐场景的能力边界。主要方向如下：

- **Scaling 与 Infra 协同** ：算法&工程 Co-Design，实现更高效的 Infra，设计高 Scaling ROI 的模型结构平衡计算量与参数量，实现模型参数量 1-2 个数量级的提升，进一步验证模型参数、序列长度的 Scaling Law。
- **基座模型场景延伸** ：将 MTFM 推广到更多业务场景，通过 Co-Train、蒸馏等方式实现 MTFM-Lite，更低成本为各场景带来基座模型红利。

## 9\. 团队招聘

算法团队来自搜索和推荐平台部/推荐算法部，负责美团各场景的商家、商品自然流量分发以及大模型相关创新能力建设，包括推荐算法、大模型应用算法等。业务核心，技术能力强，每年有多篇论文发表在 KDD、SIGIR、CIKM 等会议。当前，LLM 在推荐领域的落地仍在深度迭代中，机会广阔潜力大，欢迎各路英才加入，联系方式liuying153@meituan.com。此外，欢迎校招同学投递推荐大模型算法北斗岗位， [【北斗】推荐大模型算法工程师](https://zhaopin.meituan.com/web/position/detail?jobUnionId=4530463043&token=3094526ce7454330b1a43572e9fa2cea&jobShareType=1&share_source=cplink) 。

搜索和推荐平台部/机器学习架构组，负责美团各业务的搜索推荐机器学习引擎的工程架构工作，包括模型训练、模型推理、用户特征平台建设等。团队技术能力强，工作氛围好，当前正在深度探索下一代搜推架构等多个前沿方向，欢迎感兴趣的同学加入，联系方式：dengyuanyuan02@meituan.com。也欢迎校招同学投递大模型训推引擎北斗岗位 [【北斗】大模型训推引擎工程师（后训练/推理方向）](https://zhaopin.meituan.com/web/position/detail?jobUnionId=4530177703&highlightType=campus) 。

## 参考文献

- \[1\] MTGR：Han R, Yin B, Chen S, et al. Mtgr: Industrial-scale generative recommendation framework in meituan\[C\]//Proceedings of the 34th ACM International Conference on Information and Knowledge Management. 2025: 5731-5738
- \[2\] KDD 2026：MTFM: A Scalable and Alignment-free Foundation Model for Industrial Recommendation in Meituan（https://dl.acm.org/doi/abs/10.1145/3770855.3818452）
- \[3\] STAR：Xiang-Rong Sheng, Liqin Zhao, Guorui Zhou, Xinyao Ding, Binding Dai, Qiang Luo, Siran Yang, Jingshan Lv, Chi Zhang, Hongbo Deng, et al. 2021. One model to serve all: Star topology adaptive recommender for multi-domain ctr prediction. In Proceedings of the 30th ACM International Conference on Information & Knowledge Management. 4104–4113.
- \[4\] M3OE：Zijian Zhang, Shuchang Liu, Jiaao Yu, Qingpeng Cai, Xiangyu Zhao, Chunxu Zhang, Ziru Liu, Qidong Liu, Hongwei Zhao, Lantao Hu, et al. 2024. M3oe: Multi-domain multi-task mixture-of experts recommendation framework. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval. 893–902.
- \[5\] MLoRA：Zhiming Yang, Haining Gao, Dehong Gao, Luwei Yang, Libin Yang, Xiaoyan Cai, Wei Ning, and Guannan Zhang. 2024. Mlora: Multi-domain low-rank adaptive network for ctr prediction. In Proceedings of the 18th ACM Conference on Recommender Systems. 287–297.
- \[6\] ExFM：Ads Recommendation. 2025. External Large Foundation Model: How to Efficiently Serve Trillions of Parameters for Online Ads Recommendation. arXiv preprint arXiv:2502.17494 (2025).
- \[7\] LFM4Ads：Shangyu Zhang, Shijie Quan, Zhongren Wang, Junwei Pan, Tianqu Zhuang, Bo Fu, Yilong Sun, Jieying Lin, Jushuo Chen, Xiaotian Li, et al. 2025. Large Foundation Model for Ads Recommendation. arXiv preprint arXiv:2508.14948 (2025).
- \[8\] RankMixer：Zhu J, Fan Z, Zhu X, et al. Rankmixer: Scaling up ranking models in industrial recommenders\[C\]//Proceedings of the 34th ACM International Conference on Information and Knowledge Management. 2025: 6309-6316.
- \[9\] TokenMixer-Large：Jiang Y, Zhu J, Han X, et al. Tokenmixer-large: Scaling up large ranking models in industrial recommenders\[C\]//Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2. 2026: 7489-7500.
- \[10\] HSTU：Zhai J, Liao L, Liu X, et al. Actions speak louder than words: Trillion-parameter sequential transducers for generative recommendations\[J\]. arXiv preprint arXiv:2402.17152, 2024.
- \[11\] OneTrans：https://arxiv.org/abs/2510.26104
- \[12\] OneRec：Zhou G, Deng J, Zhang J, et al. Onerec technical report\[J\]. arXiv preprint arXiv:2506.13695, 2025.
- \[13\] STCA：Guan, Lin, et al. "Make it long, keep it fast: End-to-end 10k-sequence modeling at billion scale on Douyin." Proceedings of the ACM Web Conference 2026. 2026.
- \[14\] OneRec V2：Zhou, Guorui, et al. "Onerec-v2 technical report, 2025." https://arxiv.org/abs/2508.20900 (2025).
- \[15\] Qwen3-Next：Team Qwen. "Qwen3-Next: Towards Ultimate Training & Inference Efficiency." https://qwen.ai/blog?id=qwen3-next (2025).
- \[16\] MiMo-V2-Flash：Xiao, Bangjun, et al. "Mimo-v2-flash technical report." arXiv:2601.02780 (2026).
- \[17\] AutoSplit：参考 OneTranshttps://arxiv.org/abs/2510.26104
- \[18\] RankMixer：https://arxiv.org/abs/2507.15551
- \[19\] NVIDIA 开源自定义 Mask：https://github.com/NVIDIA/recsys-examples/blob/main/corelib/hstu/README.md
- \[20\] Flash-Muon：https://github.com/nil0x9/flash-muon/blob/main/README.md