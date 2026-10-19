---
title: " A tricky LLM interview question: "
source_key: "dailydoseofds"
email_subject: "A Full Walkthrough on Multimodal Jev"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Thu, 15 Oct 2026 23:06:22 +0000"
email_id: "1a141d112851aa57"
article_id: "1a141d112851aa57:3"
published: "2026-10-15"
content_tier: "email_fallback"
tags: []
---

#  A tricky LLM interview question: 

- **邮件来源**: dailydoseofds
- **原邮件主题**: A Full Walkthrough on Multimodal Jev
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 15 Oct 2026 23:06:22 +0000
- **邮件 ID**: 1a141d112851aa57
- **文章 ID**: 1a141d112851aa57:3
- **内容层级**: email_fallback

---

## [**A tricky LLM interview question:**](<https://www.dailydoseofds.com/llmops-crash-course-part-1/>)

You move your LLM to a faster GPU.

Profiling confirms its kernels now finish sooner, but the time between generated tokens barely changes.

The model, precision, and batch size are identical.

Where did the expected speedup go?

(answer below)

An LLM forward pass is not one giant GPU operation.

It launches a sequence of operations for attention, matmul, normalization, sampling, data movement, and other work.

![](https://substackcdn.com/image/fetch/$s_!zHAB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356df081-532e-4a86-9f95-76013bd5ea18_2752x1536.jpeg)   
---  
  
Without CUDA Graphs, the CPU prepares and submits these operations individually.

Each launch adds only a small amount of overhead, but token-by-token decoding repeats a similar sequence for every generated token.

This creates a strange bottleneck.

Some kernels finish in only a few microseconds. The GPU can complete one kernel before the CPU has submitted the next one.

That leaves empty spaces in a profiler trace. These gaps are not model computation. They show the GPU waiting for its next operation.

CUDA Graphs change how this work reaches the GPU.

The runtime captures a repeatable sequence of operations once, including their dependencies. Later iterations replay the captured sequence through one graph launch instead of submitting every operation separately.

To be clear, the kernels themselves do not become substantially faster.

Also, the model does not get smaller, and the forward pass performs almost the same computation.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/9dKQcbNvge63Tcmj5GhRLF/email)   
---  
  
Most of the gain comes from removing CPU launch work between kernels.

This is especially useful during LLM decoding.

Each decoding step processes one new token per sequence. This produces many short, repeated GPU operations where launch overhead can become a meaningful part of total latency.

Prefill often behaves differently.

A large prompt gives the GPU more parallel work, producing longer-running kernels. When those kernels already keep the GPU busy, reducing launch overhead matters less.

![](https://substackcdn.com/image/fetch/$s_!LZc7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bfcdefa-c7f7-4513-9986-76adb62b7968_2752x1536.jpeg)   
---  
  
There is also a tradeoff.

A captured graph expects the same kernel sequence, stable arguments, fixed memory addresses, and a compatible execution structure on every replay.

Inference servers handle varying batch sizes and different prefill, mixed, and decode workloads. One captured graph cannot cover every execution path efficiently.

Engines such as vLLM and TensorRT-LLM therefore capture graphs for several common execution cases and batch sizes.

When a live batch does not match a captured size, the engine may use eager execution or pad the batch to a captured size.

Capturing more sizes improves graph coverage, but it also consumes more GPU memory and increases startup time.

![](https://substackcdn.com/image/fetch/$s_!4Goh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a2092c9-44db-4dbb-8d3d-e8bd810657e5_2752x1536.jpeg)   
---  
  
So CUDA Graphs are not a universal inference speed switch.

They trade flexibility and setup cost for lower steady-state launch overhead.

The visual below shows the core mechanism.

![](https://substackcdn.com/image/fetch/$s_!z9xw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3b110a9-a7f1-4929-ac35-2dd185bcbb98_1300x1195.png)   
---  
  
  * Without a graph, the CPU submits each kernel independently and may leave idle gaps on the GPU timeline.
  * With a graph, the sequence is captured once and replayed as a unit.

CUDA Graphs are one example of why LLM inference needs a specialized serving engine rather than a standard prediction API.
