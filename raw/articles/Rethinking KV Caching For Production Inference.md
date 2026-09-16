---
title: "Rethinking KV Caching For Production Inference"
source: "https://www.dailydoseofds.com/p/rethinking-kv-caching-for-production-inference/"
author:
  - "[[dailydoseofds]]"
published: 2026-07-07
created: 2026-09-15
description: "A practitioner's guide to KV cache management in production."
tags:
  - Infra/serving
  - LLM/inference

---
Researchers at Stanford studied how AI agents actually spend their inference budgets.

One key finding was that ~62% of what gets sent to an agent on every call is just repeated content, i.e., the same system prompts, tool definitions, and documents, which are fed in again and again.

So every time the agent takes a single step, you hand it everything from scratch, even if it just processed the exact same info one turn ago:

![](https://substackcdn.com/image/fetch/$s_!BIUd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ebb39b4-9521-4593-8c33-50617cad14f3_1200x900.png)

Per-token prices dropped 80% between 2023 and 2026, with GPT-4 class models falling from $30/M to $0.40/M tokens. But agentic workflows consume 5 to 30x more tokens per task than a standard chatbot query, because every step re-sends all that context.

So even though each token got cheaper, the total bill went up, since volume outran the price cuts.

Uber shared a similar story recently. After rolling out Claude Code across their engineering org burned through their entire 2026 AI budget in just 4 months. Gartner now forecasts that 40% of AI agent projects will be cancelled by 2027 because of cost overruns alone.

The industry is optimizing the wrong variable. Making tokens cheaper doesn’t help if most of those tokens shouldn’t exist in the first place.

So, in this article, we’ll learn about [**a new open-source architecture called LMCache**](https://github.com/lmcache/lmcache?ref=dailydoseofds.com) that moves cache management out of the inference engine entirely.

![](https://substackcdn.com/image/fetch/$s_!fFcv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3469bd3a-08a1-4389-89fb-59434b6cb71c_960x671.gif)

Teams running it are seeing up to 14x faster time-to-first-token, so understanding it now puts you ahead of nearly everyone running inference today.

---

#### What happens when we prompt a model in a naive setup

Every time you prompt a model, it runs every token through the attention mechanism. For each token, the model computes a Key vector and a Value vector across every attention layer. These vectors capture how the model understands each token’s relationship to every other token in the context.

![](https://substackcdn.com/image/fetch/$s_!VbSm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b4b874e-c487-4872-a9df-eb59252341ba_1200x900.png)

This collection of K and V vectors is called the KV cache, and the computation scales quadratically with input length.

![](https://substackcdn.com/image/fetch/$s_!hDhz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F098550ae-41d0-4c13-83ab-a84e8d010185_1200x800.png)

One MI300X GPU generates roughly 15 TB of KV cache per day. Most of it gets thrown away after each request.

The KV cache for your system prompt is identical every time you send it. The KV cache for a document you uploaded is identical every time a user asks about it. But the model re-derives that same understanding from scratch, every single time.

Think of it like re-reading a textbook from page 1 every time someone asks a follow-up about chapter 7. You already understood chapters 1 through 6, but you have no way to save and reuse that understanding.

---

#### What prefix caching solves and what it doesn’t

The industry noticed the above problem and built a technique called prompt caching to deal with it.

If two consecutive requests share the same opening tokens (the “prefix”), the provider stores the KV cache from the first request and reuses it on the second. The model skips recomputing those tokens and only processes what’s new.

![](https://substackcdn.com/image/fetch/$s_!tjF8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5560c971-cd1f-4e6c-babd-2ca69a6d94fe_1024x565.png)

This is incredibly helpful. Anthropic's own implementation gives a 90% cost reduction on cached input tokens. Hit rates of 60 to 85% are achievable for stable workloads. For teams with stable system prompts and tool definitions, this is the single highest-leverage optimization available today.

But prefix caching has a hard ceiling.

The cached portion must be an exact, byte-for-byte prefix of the new request. If you change anything in the cached region (even a single character), it leads to a full cache miss, and it happens in three common scenarios:

![](https://substackcdn.com/image/fetch/$s_!jhH-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b235653-a216-4f9d-a696-0bc3d1849358_1200x675.png)

- RAG with multiple documents → You cache document `A` alone and document `B` alone. If a new query needs both documents, the 2nd document’s cached KV state is invalid since it was computed without awareness of the first document.
- Document order changes → The same three documents appear in different orders across requests. Every permutation is a cache miss, even though the documents themselves are identical.
- Growing conversation history → Each new turn changes the full context after the prefix. Earlier cached states beyond the stable prefix become useless.
![](https://substackcdn.com/image/fetch/$s_!asa0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01ff49cb-bcea-4f62-a4f2-7f5aeadc2ddc_1024x559.png)

Alibaba Cloud’s production data validates these limitations. 10% of KV cache blocks serve 77% of all hits. Most cached content never gets reused because the rigid prefix-matching rule prevents it.

Prefix caching is a meaningful optimization, but it only helps when your context has a long, unchanging beginning, and many real-world workloads don’t look like that.

---

#### Another performance bottleneck with caching

Every KV cache library runs inside the inference engine’s process. That means cache operations (storing, loading, moving KV tensors around) and the actual inference computation share the same resources.

They can’t run at the same time, so when the engine is busy managing cache, it stops doing inference, and vice versa.

![Image](https://substackcdn.com/image/fetch/$s_!-F2O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ce860fb-5781-405c-ac3b-a7aa6afa5a0e_1200x675.jpeg)

Google's TurboQuant shows this effect. It is a recent KV cache quantization technique that compresses the cache to 3 bits per value with zero accuracy loss. But when it runs inside the inference engine, it causes 20%+ inference slowdown.

Cache management and inference serving are fundamentally different workloads.

One is I/O-heavy (moving large tensors between GPU, CPU, and storage). The other is compute-heavy (matrix multiplications on GPU).

---

#### LMCache and the disaggregated approach

LMCache is an [**open-source project**](https://github.com/lmcache/lmcache?ref=dailydoseofds.com) (10k+ stars) that takes a fundamentally different approach. Instead of running cache management inside the inference engine, it runs as a completely separate process alongside it.

![](https://substackcdn.com/image/fetch/$s_!PWy0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4d68035-dc85-47a2-807e-ae3019333712_2397x1333.png)

In practice, LMCache connects to the inference engine through shared GPU memory. The engine just tells LMCache “here are the block IDs I need” (tiny messages, almost no data).

All the heavy work of actually moving KV tensors between GPU, CPU, and storage happens inside LMCache’s own process. The inference engine doesn’t even notice it’s happening.

This separation produces three benefits:

![](https://substackcdn.com/image/fetch/$s_!Ii23!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf6a69a5-e245-4987-b37a-7fcd52a3a3bb_1200x800.png)

- No resource contention → Cache I/O never blocks inference, and inference never blocks cache I/O. The 20% throughput loss from running optimization techniques inside the engine disappears.
- Zero-copy sharing across GPUs → In the traditional setup, sharing cached data between two GPUs requires multiple memory copies. LMCache lets both GPUs read and write the same memory region directly, skipping those copies entirely.
- Multi-tier parallel loading → Cached data can live across GPU memory, CPU RAM, local SSD, and remote storage. Traditional approaches check these one by one, bottlenecking on the slowest tier. LMCache checks all of them simultaneously and streams data from wherever it finds a match, in parallel.

> The performance difference is significant. On H200 GPUs with the Qwen3-235B model and 50 concurrent users, LMCache delivers 14x faster time-to-first-token and 4x faster decoding compared to in-process caching. Startup time drops from over 3 minutes to about 30 seconds.

Also, LMCache integrates with all major inference engines (vLLM, SGLang, TensorRT-LLM) and supports both NVIDIA and AMD GPUs.

---

#### Solving the prefix problem with CacheBlend

LMCache’s architecture solves the performance side of caching.

But recall another problem we discussed above, where a query needed 2 documents.

The LMCache team’s research paper CacheBlend, which won the EuroSys 2025 Best Paper Award, directly addresses this limitation.

The observation is that in modern transformer models, most tokens primarily attend to their own local context. Only a small fraction of tokens have strong connections across document boundaries.

CacheBlend exploits this by identifying just those few tokens and selectively recomputing only them. Everything else gets reused as-is from the independent caches.

![](https://substackcdn.com/image/fetch/$s_!PY8R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80e0eaa8-329d-4687-a3bc-62a29400170c_1200x675.png)

This gives 2 to 4x faster processing for multi-document queries (the kind you see in RAG apps) without any quality loss. Instead of recomputing everything from scratch when documents are combined, CacheBlend recovers the missing cross-document understanding at a fraction of the cost.

---

#### Using LMCache in production

[**LMCache**](https://github.com/lmcache/lmcache?ref=dailydoseofds.com) isn’t a research prototype but rather ships with the infrastructure that production teams expect.

- Prometheus and OpenTelemetry integration for tracking cache hit rates and I/O performance.
- Kubernetes operator for deployment
- CLI for debugging and benchmarking.

If the inference engine crashes, LMCache preserves all cached data on CPU and storage, so recovery doesn’t start cold.

If LMCache itself crashes, the inference engine enters a downgrade mode where caching is disabled, but inference continues normally, and it reconnects automatically when the cache process recovers.

Neither failure takes the whole system down.

[**You can find the LMCache GitHub repo here →**](https://github.com/lmcache/lmcache?ref=dailydoseofds.com)

**(don’t forget to star it ⭐️)**

Good day!

Published on Jul 7, 2026[Previous](https://www.dailydoseofds.com/p/how-to-reduce-llm-costs-by-50-60-using-model-routing/)

[

How to Reduce LLM Costs by 50-60% Using Model Routing

](https://www.dailydoseofds.com/p/how-to-reduce-llm-costs-by-50-60-using-model-routing/)