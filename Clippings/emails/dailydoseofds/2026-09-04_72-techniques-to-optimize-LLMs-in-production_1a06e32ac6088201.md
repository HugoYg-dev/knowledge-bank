---
title: " 72 techniques to optimize LLMs in production "
source_key: "dailydoseofds"
email_subject: "5 Embedding Compression Techniques"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Fri, 04 Sep 2026 20:53:29 +0000"
email_id: "1a06e32ac6088201"
article_id: "1a06e32ac6088201:3"
published: "2026-09-04"
tags: []
---

#  72 techniques to optimize LLMs in production 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 5 Embedding Compression Techniques
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 04 Sep 2026 20:53:29 +0000
- **邮件 ID**: 1a06e32ac6088201
- **文章 ID**: 1a06e32ac6088201:3

---

## [**72 techniques to optimize LLMs in production**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

On an H100 running Llama 70B, a single inference request hits 92% GPU compute utilization during prefill, then drops to 28% during decode on the same hardware a moment later. The workload changed, not the GPU.

For context:

  * Prefill processes the entire prompt in parallel and saturates tensor cores.
  * Decode generates one token at a time and reads the full KV cache from HBM at every step, which makes it memory-bandwidth bound.

This asymmetry is why a single optimization never gets you very far, and why LLM inference prices have still fallen roughly 10x per year, with GPT-4-level performance going from $20 per million tokens in late 2022 to around $0.40 today.

Most of that drop came from the serving stack, and we put together this visual, which lists the techniques that go into optimizing [**LLMs in production**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>).

![](https://substackcdn.com/image/fetch/$s_!mRT-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F945c4676-d214-41d9-ac1e-062caf345ae7_1190x1107.png)   
---  
  
Every technique in the grid above is a response to one of three bottlenecks: prefill compute, decode memory bandwidth, or the cost of everything that wraps the model.

Stacking enough of these techniques closes the 5-8x cost-efficiency gap between optimized vLLM or TensorRT-LLM deployments and naive FP16 inference.

Today, let’s walk through the nine layers, what each one actually solves, and how they stack up in a real production deployment.

We covered a lot more in the [**LLMOps course**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>) with implementations and engineering logic.

[**You can start reading it here →**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

* * *

#### [1\. Model compression](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>)

![](https://substackcdn.com/image/fetch/$s_!i67T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f42345b-db28-40e1-9e38-48c3166d7d77_1961x513.png)   
---  
  
Model weights live in GPU memory all the time.

A 70B model in FP16 is 140GB before you load a single token of context. Compression attacks this usage directly.

  * INT8 halves the memory vs FP16.
  * INT4 cuts it 4x.
  * FP8 gives you native tensor core support on Hopper and Blackwell, which means compression plus speedup.

GPTQ, AWQ, and SmoothQuant are the three main algorithms here.

  * GPTQ uses Hessian-based second-order information
  * AWQ preserves salient weights based on activation magnitudes,
  * SmoothQuant handles both weights and activations at W8A8.

Distillation and pruning attack the parameter count itself rather than the bits per parameter.

Multi-LoRA serving is the escape hatch for multi-tenant deployments, where you keep one base model in memory and hot-swap small adapter weights per request.

We covered this specific pillar in

  * [**Part 9 of MLOps course →**](<https://www.dailydoseofds.com/mlops-crash-course-part-9/>)
  * [**Part 10 of MLOps course →**](<https://www.dailydoseofds.com/mlops-crash-course-part-10>)
  * [**Part 12 of LLOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-12/>)

#### 2\. Attention and architecture

![](https://substackcdn.com/image/fetch/$s_!vrck!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F687c51ac-ef1b-43a4-825e-b1ff1f696321_1089x513.png)   
---  
  
Standard attention is `O(N²)`. At 128K context, this will have 16 billion computations, which is why naive attention is infeasible at long context even on H100-class hardware.

FlashAttention reorders the attention math to be IO-aware, avoiding materializing the full `N×N` matrix.

[**PagedAttention**](<https://www.dailydoseofds.com/p/paged-attention-in-llms/>) applies OS-style virtual memory to the KV cache, eliminating fragmentation.

MQA, GQA, and MLA attack the number of KV heads.

MQA shares one KV head across all queries, GQA groups them, MLA compresses keys and values into a low-rank latent. DeepSeek-V2 reported a 93.3% KV cache reduction from MLA alone.

Sliding window attention restricts each token to a local window. MoE activates only a subset of experts per token. These are architectural choices driven entirely by serving economics.

We covered this specific pillar in:

  * [**Part 3 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-3/>)
  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)

#### 3\. Decoding

![](https://substackcdn.com/image/fetch/$s_!hnO_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31a8182e-931b-4f56-9875-17c617c21833_1540x307.png)   
---  
  
Decode is memory-bound because every new token requires a full pass over the weights and KV cache.

  * [**Speculative decoding**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>) sidesteps this by generating a draft with a cheap model, then verifying in parallel with the main model.
  * Medusa attaches extra prediction heads to the model itself, so the same model can draft its own candidate tokens without needing a separate smaller model.
  * EAGLE improves on this by predicting at the hidden-state level rather than the token level, which gives higher draft accuracy and better speedups.
  * Lookahead decoding skips the draft model entirely. It generates and verifies multiple tokens in parallel from the main model alone.
  * Prompt lookup decoding copies spans directly from the input prompt, which is surprisingly effective for tasks with heavy prompt-output overlap like summarization or code edits.
  * Constrained decoding enforces grammars at the token level, which is how providers guarantee valid JSON.
  * Multi-token prediction trains the model to emit several tokens per forward pass.

We covered this specific pillar in:

  * [**Part 4 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-4/>)
  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)

#### [4\. KV cache](<https://www.dailydoseofds.com/p/kv-caching-in-llms-explained-visually/>)

![](https://substackcdn.com/image/fetch/$s_!4xr8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01ee8c57-216a-431c-bb1f-ce28fa1098c2_1540x307.png)   
---  
  
The KV cache grows linearly with context length, and for long conversations it dominates memory ([**learn KV caching here**](<https://www.dailydoseofds.com/p/kv-caching-in-llms-explained-visually/>))

A 70B model with 4K context per request already consumes several gigabytes of KV just for a modest batch size.

  * Prefix caching reuses KV across requests sharing the same prefix, which is why system prompts and few-shot examples are effectively free after the first request.
  * KV offload tiers cold cache entries to CPU RAM or NVMe.
  * KV cache quantization compresses the cache itself, separate from the weights.
  * Token eviction methods like H2O and SnapKV drop low-attention tokens from the cache. SnapKV reports 92% KV compression at a 1024-token budget with a 3.6x decode speedup.
  * Attention sinks, from the StreamingLLM paper, keep the first few tokens permanently in the cache to prevent long-context generation from going incoherent past the cache limit.
  * Chunked prefill splits long prompts into smaller pieces so decode steps can interleave with prefill work.

We covered this specific pillar in:

  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)

#### 5\. Batching and scheduling

![](https://substackcdn.com/image/fetch/$s_!ACmf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F941e3f74-4a21-4901-81a4-9e52ff76bce2_1540x307.png)   
---  
  
LLM inference is memory-bandwidth bound during decode, which means the GPU is usually starved. Batching more requests together amortizes memory reads across more useful work.

  * [**Continuous batching**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>) does this at the iteration level. As soon as one request finishes generating, a new one takes its slot mid-flight.
  * Dynamic batching waits for a short window to group arriving requests. Batching 32 requests together cuts per-token cost roughly 85% with minor latency impact.
  * [**Prefill-decode disaggregation**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>) splits the two phases onto separate GPU pools. Perplexity, Meta, and Mistral run this in production because co-locating prefill and decode on the same GPU means decode requests freeze every time a new prefill enters the batch.
  * SLO-aware scheduling prioritizes interactive traffic over background jobs.
  * Spot GPU scheduling runs preemptible workloads on cheap capacity.
  * Request deduplication merges identical in-flight queries.

We covered this specific pillar in:

  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)
  * [**Part 14 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-14/>)
  * [**Part 15 of MLOps course →**](<https://www.dailydoseofds.com/mlops-crash-course-part-15/>)

#### 6\. Parallelism and kernels

![](https://substackcdn.com/image/fetch/$s_!5YvD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a7b7511-b108-4c10-8dc3-b7a33e3ced1b_1540x307.png)   
---  
  
  * Tensor parallelism splits weight matrices across GPUs.
  * Pipeline parallelism splits layers.
  * Expert parallelism shards MoE experts across devices.
  * Sequence parallelism splits along the token dimension.
  * CUDA graphs reduce kernel launch overhead, which matters because decode launches thousands of tiny kernels per second.
  * Kernel fusion combines multiple operations into one launch.
  * [**Torch compile**](<https://www.dailydoseofds.com/pytorch-models-are-not-deployment-friendly-supercharge-them-with-torchscript/>) produces fused kernels automatically via graph-level compilation.

We covered this specific pillar in:

  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)

#### 7\. Application caching

![](https://substackcdn.com/image/fetch/$s_!8Nv6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F585d4c23-ee4c-4665-93d1-00e5dab705b3_1318x307.png)   
---  
  
The cheapest inference is the one you skip.

  * Prompt caching reuses the KV state of static prefixes across calls. Anthropic reports up to 90% cost reduction and 85% latency reduction for long cached prompts.
  * Semantic caching matches queries by embedding similarity rather than exact string match, which handles paraphrases.
  * Exact-match caching is the hash-based baseline.
  * Response caching stores completed outputs.
  * Embedding deflection routes simple queries to a vector search without ever calling the LLM.
  * [**Batch API endpoints**](<https://www.dailydoseofds.com/mlops-crash-course-part-11/>) run async jobs at roughly half the per-token price for non-realtime workloads

We covered this specific pillar in:

  * [**Part 13 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-13/>)
  * [**Part 14 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-14/>)

#### 8\. Input/output shaping

![](https://substackcdn.com/image/fetch/$s_!PxY4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7063c153-5642-40d4-9a4d-c82de6f2cf28_885x508.png)   
---  
  
Output tokens cost 3-10x more than input tokens across every major provider. 

Claude Sonnet 4 is $3 per million input versus $15 per million output, so trimming either side of the call translates directly into margin.

  * Prompt compression with tools like LLMLingua achieves up to 20x compression with minimal quality loss.
  * Context pruning drops irrelevant retrieved chunks before they reach the model.
  * System prompt optimization trims static prefixes that bloat every request.
  * Response length caps, structured output modes, and few-shot pruning all attack output volume.
  * Context distillation summarizes long histories into a shorter state.
  * RAG over long context is often cheaper than stuffing everything into the window. Retrieval keeps the prefill bill bounded.

We covered this specific pillar in:

  * [**Part 5 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-5/>)
  * [**Part 6 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-6/>)
  * [**Part 7 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-7/>)
  * [**Part 8 of LLMOps course →**](<https://www.dailydoseofds.com/llmops-crash-course-part-8/>)

#### 9\. Routing and cost

![](https://substackcdn.com/image/fetch/$s_!4GJG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F338cf451-94d1-452a-88b8-c056122ac1dc_1526x303.png)   
---  
  
Not every query needs a frontier model.

  * Model routing picks a smaller model when a smaller model suffices.
  * Model cascading runs a cheap model first and escalates to a larger one only when confidence is low. [**Advisor strategy**](<https://www.dailydoseofds.com/p/advisor-strategy-in-agents/>) is somewhat similar to this:
  * Classifier routing learns which queries go where.
  * Multi-provider failover routes across APIs for reliability and cost.
  * QoS tiers separate fast-and-cheap traffic from slow-and-high-quality.
  * Task-specific fine-tuning lets a 7B model match a 70B model on a narrow domain.
  * Function calling offloads deterministic logic to tools so the model doesn’t spend tokens computing what code could.

We covered a lot more in the [**LLMOps course**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>) with implementations and engineering logic.

[**You can start reading it here →**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)
