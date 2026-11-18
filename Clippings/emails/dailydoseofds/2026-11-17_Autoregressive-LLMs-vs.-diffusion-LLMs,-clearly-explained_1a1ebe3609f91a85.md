---
title: " Autoregressive LLMs vs. diffusion LLMs, clearly explained "
source_key: "dailydoseofds"
email_subject: "The next AI inference architecture, clearly explained (4x faster than GPUs)"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Tue, 17 Nov 2026 23:41:49 +0000"
email_id: "1a1ebe3609f91a85"
article_id: "1a1ebe3609f91a85:2"
published: "2026-11-17"
content_tier: "email_fallback"
tags: []
---

#  Autoregressive LLMs vs. diffusion LLMs, clearly explained 

- **邮件来源**: dailydoseofds
- **原邮件主题**: The next AI inference architecture, clearly explained (4x faster than GPUs)
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 17 Nov 2026 23:41:49 +0000
- **邮件 ID**: 1a1ebe3609f91a85
- **文章 ID**: 1a1ebe3609f91a85:2
- **内容层级**: email_fallback

---

## [**Autoregressive LLMs vs. diffusion LLMs, clearly explained**](<https://www.dailydoseofds.com/diffusion-models-part-1/>)

Generating 500 tokens doesn't always require 500 sequential decoding steps.

Autoregressive models extend a response one token at a time. Masked diffusion models can predict multiple positions together, then repeat that process to complete the response.

Both can use transformer components such as embeddings, attention, and feed-forward layers. Their attention patterns and training objectives differ.

#### 1) Autoregressive LLMs

In standard autoregressive decoding, each forward pass produces a probability distribution for the next token.

The selected token is appended, and generation continues from that longer sequence.

Causal attention prevents a position from accessing future positions. Earlier token representations therefore stay unchanged as new tokens arrive.

That allows their KV to be cached and reused.

A 500-token response normally requires 500 sequential token-generation steps, although techniques such as speculative decoding can reduce expensive model passes.

#### 2) Diffusion LLMs

In the masked diffusion approach shown below, generation starts with masked output positions alongside the prompt.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/aGyaNQ9QxN2jTpwFEp76hc/email) An autoregressive LLM emits one token per pass, while a diffusion LLM predicts many masked tokens at once and keeps the most confident ones.  
---  
  
A denoising pass predicts candidate tokens for multiple positions using bidirectional context.

With confidence-based sampling, selected predictions are retained while other positions remain masked for subsequent steps.

The model progressively fills the sequence. It doesn't necessarily produce a complete draft and repeatedly rewrite every token.

Some implementations generate block by block rather than processing the entire response together.

Multiple tokens can be finalized per step, allowing fewer steps than output tokens. The step budget affects both speed and quality.

There are some engineering tradeoffs.

Bidirectional attention makes standard autoregressive KV reuse harder. A token's representation can change when surrounding positions are updated, even if that token itself stays fixed.

Caching therefore depends on the architecture and decoding strategy. Block diffusion, for example, can support KV caching across completed blocks.

Fewer steps also don't guarantee lower latency. Each step may process many positions, so total computation and implementation matter.

Bidirectional conditioning also supports filling gaps in text or code.

[**You can read the diffusion models series here →**](<https://www.dailydoseofds.com/diffusion-models-part-1/>)

  * [**Read Part 1 on the theory, math, and why they work →**](<https://www.dailydoseofds.com/diffusion-models-part-1/>)
  * [**Read Part 2 on training, inference, and practical engineering →**](<https://www.dailydoseofds.com/diffusion-models-part-2/>)

👉 Over to you: Where would a diffusion LLM be a better fit than an autoregressive one in your stack?
