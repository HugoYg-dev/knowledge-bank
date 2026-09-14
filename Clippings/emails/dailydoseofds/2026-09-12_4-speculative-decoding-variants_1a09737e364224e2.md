---
title: " 4 speculative decoding variants "
source_key: "dailydoseofds"
email_subject: "4 Speculative Decoding Variants"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Sat, 12 Sep 2026 20:03:35 +0000"
email_id: "1a09737e364224e2"
article_id: "1a09737e364224e2:2"
published: "2026-09-12"
tags: []
---

#  4 speculative decoding variants 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 4 Speculative Decoding Variants
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 12 Sep 2026 20:03:35 +0000
- **邮件 ID**: 1a09737e364224e2
- **文章 ID**: 1a09737e364224e2:2

---

## [**4 speculative decoding variants**](<https://www.dailydoseofds.com/p/speculative-decoding-in-llms/>)

Large-model decoding often spends one full model run producing a single token, even when the next few tokens are predictable.

Speculative decoding tries to get several useful tokens from that run instead of just one.

![](https://substackcdn.com/image/fetch/$s_!4B33!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bc1a238-dc67-4b49-affd-166dc2bd3097_1376x768.jpeg)   
---  
  
A cheaper path drafts a short continuation. The large model checks those tokens together, keeps the accepted prefix, and corrects the first mismatch. Draft tokens never reach the output without verification from the large model.

The main difference between speculative decoding variants is how they produce that draft. Some use a second model, while others build drafting into the target model itself.

![](https://substackcdn.com/image/fetch/$s_!gje4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6eff00d9-1d41-489e-8e47-30a6b04ce957_944x684.gif)   
---  
  
Let’s look at the four approaches and the engineering tradeoffs behind each one.

To dive deeper into the full LLMOps lifecycle, we have covered every bit of this in the LLMOps course, starting from fundamentals to production.



[**Start here →**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

#### The common speculative decoding loop

Every variant has two stages: draft several tokens cheaply, then verify them with the target model in parallel.

Suppose the drafter proposes five tokens. If the target accepts the first three and rejects the fourth, the first three move to the output. The target supplies the replacement at position four, while the remaining draft is discarded.

![](https://substackcdn.com/image/fetch/$s_!RTr5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95419d15-ef03-441e-8791-064875e0c8c8_1376x482.jpeg)   
---  
  
When all five tokens are accepted, the verifier can add one more token from the same pass. The sequence advances by six tokens after one target-model run.

For greedy decoding, this means checking whether the predicted tokens match. Sampling requires an acceptance and correction rule based on both probability distributions.

The original algorithm preserves the target model’s distribution, so acceleration does not require changing the result.

#### 1\. Two-model speculative decoding

The original approach pairs a small draft model with a larger target model. The small model generates a few tokens sequentially, then the target verifies the full block at once.

![](https://substackcdn.com/image/fetch/$s_!Z2rG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a4c00ff-6f1e-4d85-8cee-5196666d673f_1376x592.jpeg)   
---  
  
This is still the first setup to test. It works with an unchanged target model, and most inference stacks already support some form of assisted generation. The original paper reported 2x to 3x acceleration on T5-XXL with identical outputs.

The draft model needs to be cheap enough to justify its work but accurate enough to earn a useful acceptance rate. A larger drafter often predicts better, yet its added latency can reduce the final speedup.

![](https://substackcdn.com/image/fetch/$s_!aXxx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8f77667-ac8d-43ba-af62-6b1bcf55254a_1376x768.jpeg)   
---  
  
There is also a clear memory cost. The server holds another set of weights and a separate KV cache. Closely matched model families are usually easier to serve because their tokenizers and output behavior align better.

#### 2\. EAGLE drafts from hidden states

EAGLE removes the independent draft language model. It trains a lightweight module to predict the target model’s second-to-top-layer features, then converts those predicted features into candidate tokens.

Instead of asking a separately trained model to approximate the target, EAGLE drafts from the target model’s own internal representation.

![](https://substackcdn.com/image/fetch/$s_!ZtCH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc997ad75-91bf-4803-91ea-3a308573baf0_1376x768.jpeg)   
---  
  
Feature prediction has an ambiguity problem because different tokens can produce similar hidden states. EAGLE also feeds in the token sequence shifted forward by one position, giving the draft module enough information to make the feature prediction more precise.

The paper reported 2.7x to 3.5x latency speedups for LLaMA2-Chat 70B and roughly doubled throughput in its evaluated setup. In practice, EAGLE fits best when the checkpoint and serving engine can be managed together because its draft module is trained for a specific target.

#### 3\. Medusa uses parallel prediction heads

Medusa adds several small decoding heads to the target model. One head predicts the next token, another predicts two positions ahead, and later heads predict positions farther into the continuation.

All heads run from the same model state. This makes drafting parallel, but it also means one head cannot condition on what another head predicted. Their individual guesses do not always combine into a consistent sequence.

![](https://substackcdn.com/image/fetch/$s_!LjLS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ac1a522-425e-4cec-84e2-a83b283b6bc3_1376x768.jpeg)   
---  
  
Medusa handles this by arranging alternatives into a candidate tree. Tree attention lets the target verify several possible continuations in one pass, and the verified branch determines the accepted prefix.

![](https://substackcdn.com/image/fetch/$s_!dmND!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4a31e29-bc03-4bb4-8834-d6addb9c5270_1376x768.jpeg)   
---  
  
Medusa-1 freezes the backbone and trains only the added heads. Its paper reports more than 2.2x speedup without changing the backbone’s generation quality. Medusa-2 jointly tunes the heads and backbone, reporting 2.3x to 3.6x, but it requires a more involved training recipe.

Consider Medusa when a second model is undesirable and training small heads is feasible. Candidate-tree width becomes the main serving control because wider trees improve coverage while increasing verification work and temporary memory.

#### 4\. LayerSkip exits from early layers

LayerSkip uses the target model as both drafter and verifier. Early transformer layers produce draft tokens, while the remaining layers check and correct them.

This removes the second model and added prediction heads. Drafting and verification also share weights, vocabulary, activations, and part of the computation.

![](https://substackcdn.com/image/fetch/$s_!nmDG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6eef94ae-e7a5-47ce-9156-d44f1eedf638_1376x768.jpeg)   
---  
  
LayerSkip does require the right checkpoint. Its training recipe uses layer dropout and an early-exit loss so intermediate layers learn to produce useful predictions. A compatible checkpoint needs no separate drafter or added heads, but an arbitrary pretrained model will not provide reliable early exits automatically.

The paper reported speedups up to 2.16x on CNN/DailyMail summarization, 1.82x on coding, and 2.0x on TOPv2 semantic parsing. I would treat LayerSkip as a training decision made before deployment, not an optimization applied later to any model.

#### Choosing between the four variants

The number that matters is accepted tokens per target-model pass after accounting for drafting time and verification overhead.

![](https://substackcdn.com/image/fetch/$s_!Ooyx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6ef5346-1b92-420c-9153-2677d5404912_1376x768.jpeg)   
---  
  
  * Two-model decoding is the easiest place to begin because it leaves the target untouched.
  * EAGLE and Medusa reduce the cost of carrying another model but introduce target-specific training and serving code.
  * LayerSkip has the fewest inference-time components, provided the checkpoint was trained for early exits.

The benchmark should reproduce the real workload. Low-temperature code generation usually produces more agreement than high-temperature writing. Heavy batching can also reduce the gain because the GPU is already doing more useful work during each decode step.

All four methods still rely on KV caching. Speculative decoding reduces the number of target-model runs, while the KV cache prevents accepted context from being recomputed during the next iteration.

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

👉 Over to you: Which speculative decoding approach best matches the models you can modify and the memory available in your serving stack?
