---
title: NVIDIA researchers built a new transformer variant
source_key: dailydoseofds
email_subject: The Four Types of Agent Loops
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 14 Jul 2026 16:27:49 +0000
email_id: 19f6174c7b5adc67
article_id: 19f6174c7b5adc67:1
published: '2026-07-14'
tags:
- Infra/serving
- LLM/inference

---

# NVIDIA researchers built a new transformer variant

- **原邮件主题**: The Four Types of Agent Loops
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 14 Jul 2026 16:27:49 +0000
- **ID**: 19f6174c7b5adc67

---

## **NVIDIA researchers built a new transformer variant**

One small change to the layers made:

  * decoding 1.7x faster
  * long-reasoning accuracy up 6.5 points

In a typical transformer architecture, every attention layer computes Q, K, and V. 

NVIDIA's tweak adds a fourth projection, which predicts what the next layer will need.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/qZFwWkXKtYWxZpuw6afa8m/email)   
---  
  
To understand why they did this, let's first see what happens in a Transformer architecture during inference right now.

Sparse attention was an attempt to handle long-context inference. Instead of attending to every cached token, modern designs score the KV cache in blocks, keep the top-k, and attend only to those.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/c99WwKDBDUy7ifocb99N76/email)   
---  
  
That cuts attention compute and bandwidth, but this still leaves us with two problems.

> First, the KV cache still grows with every generated token.

At 100K+ context, it no longer fits in GPU memory and gets offloaded to CPU RAM.

Now every layer must first copy its selected KV blocks from CPU memory back to the GPU. That copy is slow, the GPU sits idle while it waits, and the stall repeats at every layer of every decode step.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/tbVkqQpj8jxRb9ipYm8zeT/email)   
---  
  
> Second, the selection step itself is not free.

Standard selectors score every candidate block with every query head in a GQA group (grouped-query attention, where several query heads share one KV head), then softmax each head's scores and sum them across the group.

During decode, the sparse attention itself is cheap because there is only one query token.

But the expensive part is deciding which blocks to attend to, and that cost keeps growing with context length.

Both problems trace back to the same design in today's sparse attention methods, i.e., the attention query drives the block selection.

Selection needs the query vector Q, and Q only exists once its layer is already running. By then, it's too late to fetch anything early.

The query also drags its multi-head layout into selection, so all that scoring computation runs just to make one top-k decision.

A recent paper from NVIDIA and MIT called SparDA breaks this coupling with one architectural change.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/e3s8cn95yaDd9BHp5bfCQQ/email)   
---  
  
Each layer now emits four projections instead of three:

↳ Q, K, V, and a Forecast.

The Forecast from layer L predicts which KV blocks layer L+1 will need. 

Layer L+1's own query performs the sparse attention over those selected blocks.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/aEHPvzQBaFvmGiByZbXvku/email)   
---  
  
This one change fixes both problems.

Since the next layer's block set is known while the current layer is still computing, the runtime fetches those blocks from CPU memory on a separate CUDA stream.

The copy overlaps with the current layer's compute, so the GPU no longer waits for it.

And since the Forecast is separate from the attention query, it doesn't need one score per query head.

SparDA uses one Forecast head per GQA group, which removes the per-query-head scoring loop and skips the softmax step entirely.

DeepSeek did something similar in DSA, where a small indexer picks important tokens instead of the query doing it.

SparDA applies the same idea to blocks and adds the prefetch angle that DSA doesn't touch.

The cost of the change is small.

The Forecast adds just 33.5M parameters on an 8B model (0.41%), and only those projections are trained, using a KL loss that matches the original selector's block distribution.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/212NPHj53f5VC8bfPNHjgJ/email)   
---  
  
On MiniCPM4.1-8B and NOSA-8B, accuracy matches or beats the sparse baseline, with NOSA-8B gaining +6.5 on long reasoning.

Prefill runs up to 1.25x faster and decode up to 1.7x faster than the sparse offload baseline.

There's one more benefit.

Because prefetch hides the offload cost, most of the KV cache can live in CPU RAM, and the freed GPU memory fits much bigger batches, pushing decode throughput up to 5.3x over the non-offload sparse baseline.

That said, this lookahead will only pay off during decode with CPU offload. During prefill, all keys already live on the GPU, so the gain there comes purely from the cheaper selection.

Here's the paper: [**https://arxiv.org/abs/2606.04511**](<https://fff97757.click.kit-mail3.com/n4uqvqx86whvhxz7pxxc6h673wwnlclhgovww/reh8hohml6rnm9s2h6/aHR0cHM6Ly9hcnhpdi5vcmcvYWJzLzI2MDYuMDQ1MTE=>)

We wrote a first-principles breakdown of how the KV cache works. It walks through why the model stores keys and values at all, why the cache grows with every token, and a comparison of LLM generation speed with and without KV caching.

[**Read it here →**](<https://fff97757.click.kit-mail3.com/n4uqvqx86whvhxz7pxxc6h673wwnlclhgovww/08hwh9h26l5q2oclh5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcC9rdi1jYWNoaW5nLWluLWxsbXMtZXhwbGFpbmVkLXZpc3VhbGx5Lw==>)
