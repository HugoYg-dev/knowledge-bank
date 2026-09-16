---
title: Cross-model KV cache transfer in LLM families
source_key: dailydoseofds
email_subject: How to Query Billion+ Rows on Postgres Without Overhead
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 10 Aug 2026 13:49:07 +0000
email_id: 19febef2c6003814
article_id: 19febef2c6003814:2
published: '2026-08-10'
tags:
- LLM/inference
- Infra/serving

---

#  Cross-model KV cache transfer in LLM families 

- **邮件来源**: dailydoseofds
- **原邮件主题**: How to Query Billion+ Rows on Postgres Without Overhead
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 10 Aug 2026 13:49:07 +0000
- **邮件 ID**: 19febef2c6003814
- **文章 ID**: 19febef2c6003814:2

---

## [**Cross-model KV cache transfer in LLM families**](<https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/>)

NVIDIA released a paper in which they shared a method to make the KV cache transferable between models.

The target model skips prefill entirely, and the conversion runs 2.7 to 25x faster than processing the context again.

Let’s understand why this is so important today.

During LLM token generation, every turn sends the entire conversation back to the model. The model reads all of it again before writing a single new token, and all of it is billed as input.

[**Prompt caching**](<https://www.dailydoseofds.com/p/prompt-caching-in-llms/>) allows Anthropic and other providers to hold the KV cache for a stable prefix and bill a hit at roughly 10% of the base input rate, because the compute was already done once.

![](https://substackcdn.com/image/fetch/$s_!w4Oc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92b62ea1-5dfe-408b-9a42-ae47a469910d_1024x559.png)   
---  
  
The 90% reduction is one of the largest levers in LLM serving, which is why so much production work goes into keeping prefixes byte-stable.

But the cache only works on the model that produced it. Keys and values are produced from that model’s weights, so no other model can read them.

In practice, the constraint shows up in LLM routing. If the traffic is shifted to a different model for cost/capability reasons, the accumulated KV cache becomes invalid.

![](https://substackcdn.com/image/fetch/$s_!HgS-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7dc7db3b-5d5e-4e4a-9751-60fb0cef8fb9_1416x417.png)   
---  
  
As a result, the accumulated context has to be processed from scratch, and it’s billed at full rate.

NVIDIA’s recent paper treats this as a representation problem.

Prefill’s only output is the KV cache, so to move KV between models, we need to convert one model’s cache into the format the other expects.

They first checked whether the conversion has any structure worth exploiting.

They found that moving from Qwen3 14B to 32B, a plain linear regression from a single source layer reconstructed 56% of the variance in the target model’s keys.

![](https://substackcdn.com/image/fetch/$s_!A5lx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a82c54c-3a0a-4262-952a-94cfd4b223de_1315x856.png)   
---  
  
The two models obviously may have different layer counts, so there is no natural one-to-one pairing between them.

For each target layer, they rank every source layer by how well it predicts that layer, then feed the top eight in together, which takes the reconstruction to 79%.

The mapper itself has three parts:

![](https://substackcdn.com/image/fetch/$s_!t0Qp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5223d8c-7480-4957-86dc-c5d86f571e91_960x362.gif)   
---  
  
> Each target layer and head gets its own independent linear map, solved in one closed-form step rather than by gradient descent.

> The cross-layer selection described above is the second part, and their ablation shows it carries the most weight of the three.

> Keys also carry a position-dependent rotation from RoPE. They strip that rotation, fit the map in position-free space, then reapply the target model’s rotation at inference.

Across six pairs from Qwen3, Llama 3.1, and Ministral 3, four retain 73 to 98% of the receiving model’s standalone accuracy, and the conversion runs 3-25x faster than processing the context again.

![](https://substackcdn.com/image/fetch/$s_!LSYn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F554cf094-9c75-4830-a90c-74f92b622ee5_1109x281.png)   
---  
  
Prior work on cross-model KV reuse exists, but it either trains a neural adapter per pair or requires both models to be architecturally identical.

This is probably the first version that is closed-form and training-free, so a lot of it is still open research.

Every pair tested belongs to one family, so it works on Qwen to Qwen and Llama to Llama.

Cross-family transfer is listed as future work.

All six pairs mentioned above also happen to share the KV head count and per-head dimension across scales. Mismatched head configurations are currently untested.

The researchers scoped this to dense full-attention only, so sliding-window and attention-recurrent hybrids still need work.

Here’s the paper: [**https://arxiv.org/abs/2608.03893**](<https://arxiv.org/abs/2608.03893>)

Plenty of work is yet to be done. Still, the constraint being solved is genuine.

Every model swap currently invalidates the full KV that was already paid for, and this is the first result showing that work might be recoverable without training anything extra.

To dive deeper into KV cache management specifically for running LLMs in production, we wrote a [**full 50 min deep dive**](<https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/>) that covers:

![](https://substackcdn.com/image/fetch/$s_!qjvk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57d39cfb-3419-41df-a2d5-c87e33c960b5_1086x644.png)   
---  
  
  * Why prefill dominates RAG latency, not retrieval
  * How the KV cache works and what it costs in memory
  * Why prefix caching approaches zero hit rate for RAG workloads
  * Three independent failures when you try to reuse cached chunks
  * Six published approaches to fix them
  * Hands-on implementation that covers every problem and fixes
  * Best practices for production to assess what applies to your system

[**Read the full deep dive here →**](<https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/>)

[**Production RAG Deep Dive**](<https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/>)  
---
