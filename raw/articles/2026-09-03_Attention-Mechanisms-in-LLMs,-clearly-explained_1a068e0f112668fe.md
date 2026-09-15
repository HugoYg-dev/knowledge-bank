---
title: " Attention Mechanisms in LLMs, clearly explained "
source_key: "dailydoseofds"
email_subject: "Attention Mechanisms in LLMs, clearly explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Thu, 03 Sep 2026 20:06:06 +0000"
email_id: "1a068e0f112668fe"
article_id: "1a068e0f112668fe:2"
published: "2026-09-03"
tags: []
---

#  Attention Mechanisms in LLMs, clearly explained 

- **邮件来源**: dailydoseofds
- **原邮件主题**: Attention Mechanisms in LLMs, clearly explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 03 Sep 2026 20:06:06 +0000
- **邮件 ID**: 1a068e0f112668fe
- **文章 ID**: 1a068e0f112668fe:2

---

## [**Attention Mechanisms in LLMs, clearly explained**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

Every model card advertises its attention mechanism. 

![](https://substackcdn.com/image/fetch/$s_!2V8G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07227f19-126c-491d-975a-f8642518cd3c_3102x1942.png)   
---  
  
Multi-Query Attention, Grouped-Query Attention, and Multi-Head Latent Attention are listed alongside parameter counts and benchmark scores.

They all exist because of the same constraint. Storing attention state for long sequences and large batches runs you out of GPU memory.

And today we break down each of them, in the order they arrived and the flaw each one fixed.

Let’s begin!

To dive deeper into the full LLMOps lifecycle, we have covered every bit of this in the LLMOps course, starting from fundamentals to production.



[**Start here →**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

#### Why attention exists

Early sequence models like Recurrent Neural Networks (RNNs) passed a fixed-size hidden state from token to token. 

The further apart two tokens were, the weaker the connection. Long-range dependencies faded.

![](https://substackcdn.com/image/fetch/$s_!sSMZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2568fb7-a33b-4e43-9387-f4c3aa45d4e2_1376x768.png)   
---  
  
Attention solves this directly. Instead of passing state through a bottleneck, every token gets to look at every other token and decide how relevant each one is. 

Nothing is hidden behind a summarization step.

That directness is what makes transformers powerful. It is also what makes them expensive. The cost lives in the memory required to store what every token has seen.

#### The constraint that drives everything

Every time the model attends, it needs to remember what every previous token looked like. 

During prefill, the model processes your entire prompt at once and computes a key vector and a value vector for each token at each layer.

These get stored in what’s called the KV cache so that decode steps can attend over them without recomputing from scratch.

![](https://substackcdn.com/image/fetch/$s_!kb1Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47c41be8-a081-4154-b100-fbef93e703ab_1376x768.png)   
---  
  
The cache grows with every token generated. For a 70B model at BF16, a single 128K-token context holds roughly 40 GB of KV cache, comparable to the model weights themselves at 4-bit quantization.

The constraint is not compute and not the math in the attention formula. It is the memory that stores what attention has already seen.

#### Self-attention and causal attention

Self-attention lets each token attend to every other token in the same sequence. 

The model computes a query, key, and value for each token, then uses query-key dot products to decide how much each token should attend to every other one. 

This is the base operation inside every transformer layer.

![](https://substackcdn.com/image/fetch/$s_!UZqa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F766c89b7-9953-48f3-9966-edb34bbb08a4_1376x768.png)   
---  
  
Causal attention is self-attention with a triangular mask applied. Each token can only attend to tokens that came before it, never future ones.

This is what makes decoder-only generation possible, because without the mask the model would see the answer before producing it.

![](https://substackcdn.com/image/fetch/$s_!D3Dn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa09869d1-7641-4f61-b864-08ac1b1334f5_1376x768.png)   
---  
  
Cross-attention is different in kind. The queries come from one sequence, the keys and values come from a second sequence.

This is how encoder-decoder models like T5 and Whisper connect the encoder’s output to the decoder. In decoder-only models like Llama and GPT, cross-attention does not appear at all.

#### Multi-Head Attention

Multi-Head Attention (MHA) is the original design from the 2017 Transformer paper. 

Each attention head gets its own independent set of query, key, and value weight matrices. With 32 heads, you have 32 independent KV projections per layer.

![](https://substackcdn.com/image/fetch/$s_!OBP5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7343081a-1501-4cf2-bb09-2731bedadef8_1376x768.png)   
---  
  
The benefit is expressiveness. Different heads learn to track different kinds of relationships simultaneously. One head might track syntactic structure, another semantic proximity, another long-range coreference.

The cost is memory. Every head maintains its own KV cache. A model with 32 layers and 32 heads per layer stores 1,024 separate KV tensors per token per request.

GPT-3 uses 96 heads per layer. At a 128K-token context on a model that size, the KV cache alone fills a GPU before the batch grows at all.

That memory cost is what every design after MHA is built to reduce.

#### Multi-Query Attention

Multi-Query Attention (MQA) takes the most direct route. All query heads still have their own weight matrices, but every query head shares a single key head and a single value head.

The KV cache shrinks by a factor equal to the number of heads. Where MHA stores 32 separate KV projections, MQA stores one.

![](https://substackcdn.com/image/fetch/$s_!IDsa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F665b0e4f-4445-49a5-9b9d-a16907829704_1376x768.png)   
---  
  
Decode gets faster because you are loading far fewer bytes from HBM per step, which matters because decode is memory-bandwidth-bound.

The quality cost is real. Forcing all query heads to share one key and one value loses some of the expressiveness MHA provides.

Falcon, PaLM, and early Gemini variants used MQA and accepted this tradeoff for the throughput gain.

What MQA gives up in quality, the next design largely recovers.

#### Grouped-Query Attention

Grouped-Query Attention (GQA) sits between MHA and MQA. 

Query heads are divided into groups, and each group shares one key head and one value head. The groups are independent of each other.

![](https://substackcdn.com/image/fetch/$s_!_3VA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ea4025a-4df1-4db4-8d03-019790a2f333_1376x768.png)   
---  
  
With 32 query heads and 8 KV groups, you store 8 KV projections instead of 32, a 4x reduction in KV cache size compared to MHA, while recovering most of the quality that MQA trades away.

This balance is why GQA has become the default for almost every major open-weight model released in recent years. Llama 2 70B uses 8 KV groups. Llama 3, Mistral, Mixtral, Gemma, and Qwen all use GQA.

The original GQA paper showed it matches MHA quality at a fraction of the memory cost, and that has held up across model families.

GQA reduces the number of KV heads stored. What comes next compresses the heads themselves.

#### Multi-Head Latent Attention

Multi-Head Latent Attention (MLA) is DeepSeek’s contribution, introduced in DeepSeek-V2 in May 2024. 

Where MQA and GQA reduce the number of KV heads, MLA compresses the full-dimensional key and value vectors into a low-rank latent space before caching them. At attention time, those latent vectors get decompressed back to full dimension.

![](https://substackcdn.com/image/fetch/$s_!mLYI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8402022-4d31-4545-9636-ed0252ffadbb_1376x768.png)   
---  
  
The cached object is the latent vector, not the full KV tensors. This makes the cache footprint smaller than even GQA while preserving more of the expressiveness that MQA sacrifices.

The tradeoff is compute. Decompressing at every attention step adds FLOPs. But at inference, memory bandwidth is the bottleneck far more often than compute, so smaller cache beats extra math in most real serving configurations.

DeepSeek-V2, V3, and R1 all use MLA. On DeepSeek-V2’s benchmarks, MLA matched or exceeded MHA quality while cutting the KV cache to roughly 5-13% of what MHA would require at the same model size.

MHA, MQA, GQA, and MLA are all decisions about what to store. The next technique is about how expensively you compute it.

#### FlashAttention

FlashAttention does not change what attention computes. It changes how the computation accesses memory.

Standard attention builds the full N x N attention matrix, writes it to HBM, reads it back for the softmax, writes the result again, then reads it again for the weighted sum.

For a 4K-token sequence, that matrix is 4,096 x 4,096 values. Moving it in and out of HBM repeatedly is what makes attention the bottleneck for long contexts.

![](https://substackcdn.com/image/fetch/$s_!7pzC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b7e395c-a84c-45ee-9049-abc2c1daa8e2_1376x768.png)   
---  
  
FlashAttention tiles the computation. It processes the attention matrix in blocks that fit in on-chip SRAM, computes the softmax incrementally without materializing the full matrix, and writes the output to HBM once.

The math is identical. The memory traffic is not.

Every major serving engine uses FlashAttention kernels by default today. It is not a new attention type. It is the standard kernel for executing whatever attention type your model uses.

MHA, GQA, and MLA answer what to store and how to compress it. FlashAttention answers how to compute it efficiently. 

Sparse attention takes a different angle. Not which tokens to cache, but how many tokens to attend to at all.

#### Sparse attention

Full attention is O(N²) in sequence length. For a 1M-token context, the attention matrix has a trillion entries. Even with FlashAttention reducing memory traffic, computing attention over that many tokens is not tractable.

Sparse attention skips large portions of the attention matrix. Instead of every token attending to every other token, only a selected subset of pairs gets computed.

![](https://substackcdn.com/image/fetch/$s_!T3D_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc14b841d-da67-47a6-a526-f49580af03fc_1376x768.png)   
---  
  
Sliding Window Attention (SWA) is the simplest variant. Each token attends only to the most recent W tokens. Local context is preserved; distant context is dropped.

Mistral uses SWA on some layers, alternating with full attention on others to maintain both local precision and some global reach.

Native Sparse Attention (NSA) is DeepSeek’s 2025 contribution, distinct from MLA. Rather than applying sparsity post-hoc at inference, NSA trains the model with sparse attention from the start.

Each layer combines three parallel branches: compressed coarse-grained attention for global context, selective fine-grained attention for important token blocks, and sliding window attention for local context. The model learns during pretraining which tokens matter.

![](https://substackcdn.com/image/fetch/$s_!t22f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c807b1c-9706-4d00-b818-bb2677533ab8_1376x768.png)   
---  
  
NSA matches full-attention quality on most benchmarks while running substantially faster on long sequences. 

Qwen2.5-1M uses a sparse attention approach for its million-token context window because at that length full attention consumes over 90% of the forward pass time.

Trained-in sparsity is proving to be the most principled answer to long-context scaling.

#### The serving layer

Everything above lives inside the model weights. PagedAttention and RadixAttention live in the serving engine, and they are answers to the same KV cache pressure at a different level.

When a request arrives, the serving engine needs to allocate GPU memory for its KV cache. The naive approach reserves contiguous memory for the maximum possible sequence length.

A request allowed to generate up to 4,096 tokens gets 4,096 slots reserved upfront, whether it uses 40 or 4,000 of them.

This approach wastes 60-80% of GPU memory. Fragmentation between requests makes it worse.

![](https://substackcdn.com/image/fetch/$s_!5Yv7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2504d853-619d-4812-aa5e-e061619bff14_1376x768.png)   
---  
  
PagedAttention, the mechanism vLLM runs, manages the KV cache the way an OS manages virtual memory. Fixed-size blocks are allocated on demand.

A block table maps each request’s logical blocks to whatever physical blocks happen to be free. There is no pre-allocation, no fragmentation, and memory waste drops below 4%.

RadixAttention, the mechanism SGLang runs, takes the next step. When multiple requests share a common prefix, like a long system prompt sent to every user, the KV blocks for that prefix only need to be computed once.

RadixAttention stores KV blocks in a radix tree indexed by token sequence. A new request walks the tree, finds the longest matching prefix, reuses those blocks, and computes only the genuinely new suffix.

![](https://substackcdn.com/image/fetch/$s_!-3zx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02bfd6c1-f908-4063-aac3-f041b9939ddb_1376x768.png)   
---  
  
On multi-turn workloads, RadixAttention hits 75-95% cache hit rates. A system prompt served to thousands of users gets computed once and reused until evicted by the LRU policy.

PagedAttention and RadixAttention do not change which attention mechanism your model uses. A Llama 3 model with GQA runs fine under either engine. The two layers are independent.

#### Putting it together

The through-line across all of them is the same pressure. KV cache memory is the bottleneck, and every design here is a different move against it.

![](https://substackcdn.com/image/fetch/$s_!3_ds!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d1dac70-5f22-4781-b73b-89e7eedaceb0_1376x768.png)   
---  
  
MQA, GQA, and MLA reduce how much you store per token, each trading a different amount of quality for memory.

FlashAttention reduces how expensively the computation accesses memory, without touching the math at all.

Sparse attention reduces how many tokens you attend to, which is the only answer that scales to million-token contexts.

PagedAttention and RadixAttention work at the serving layer, cutting waste in allocation and reuse rather than in the model itself.

![](https://substackcdn.com/image/fetch/$s_!TIdG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf305054-416c-4eb1-8a45-7cb049bc3f6f_1376x768.png)   
---  
  
Knowing which of these is the binding constraint in your setup is what determines which one actually moves the number for you.

👉 Over to you: was it the model architecture choice, the attention kernel, or the serving engine's cache management that hit you hardest in production?

To dive deeper into the full LLMOps lifecycle, we have covered every bit of it in the LLMOps course, starting from fundamentals to production:

  * [**Read Part 1 on fundamentals of LLMOps here →**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)
  * [**Read Part 2 on understanding the core building blocks of LLMs →**](<https://www.dailydoseofds.com/llmops-crash-course-part-2>)
  * [**Read Part 3 on the key components of LLMs, focusing on the attention mechanism, architectures like transformers and mixture-of-experts, and the fundamentals of pretraining and fine-tuning →**](<https://www.dailydoseofds.com/llmops-crash-course-part-3>)
  * [**Read Part 4 on decoding strategies, generation parameters, best practices, and the broader lifecycle of LLM-based applications →**](<https://www.dailydoseofds.com/llmops-crash-course-part-4>)
  * [**Read Part 5 on context + prompt engineering from a system perspective, in-context learning, types of prompts, and different prompting techniques →**](<https://www.dailydoseofds.com/llmops-crash-course-part-5>)
  * [**Read Part 6 on prompt versioning, defensive prompting, and techniques like verbalized sampling, role prompting, and more →**](<https://www.dailydoseofds.com/llmops-crash-course-part-6>)
  * [**Read Part 7 on context engineering, covering context types, context construction principles, and retrieval-centric techniques for building high-signal inputs →**](<https://www.dailydoseofds.com/llmops-crash-course-part-7>)
  * [**Read Part 8 on memory, dynamic, and temporal context in LLM systems, covering short and long-term memory, dynamic context injection, and common failure modes in agentic applications →**](<https://www.dailydoseofds.com/llmops-crash-course-part-8>)
  * [**Read Part 9 on evaluation methods and approaches for LLM-based applications, primarily focusing on building a strong understanding of the fundamental concepts →**](<https://www.dailydoseofds.com/llmops-crash-course-part-9>)
  * [**Read Part 10 on evaluation benchmarks in LLM applications, with task-specific methodologies, and the core tooling for evaluation of LLM apps →**](<https://www.dailydoseofds.com/llmops-crash-course-part-10>)
  * [**Read Part 11 on evaluation of multi-turn systems, tool use evaluations, tracing, and red teaming →**](<https://www.dailydoseofds.com/llmops-crash-course-part-11>)
  * [**Read Part 12 on LLM fine-tuning, parameter-efficient methods like LoRA and QLoRA, and alignment techniques such as RLHF, DPO, and GRPO →**](<https://www.dailydoseofds.com/llmops-crash-course-part-12/>)
  * [**Read Part 13 on LLM inference optimization, KV caching, PagedAttention, FlashAttention, speculative decoding, and model parallelism →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)
  * [**Read Part 14 on the fundamentals of LLM serving, including API-based access, inference with vLLM, and practical decisions.**](<https://www.dailydoseofds.com/llmops-crash-course-part-14>)

