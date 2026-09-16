---
title: CPU vs GPU vs TPU vs NPU vs LPU
source_key: dailydoseofds
email_subject: Serverless vs. On-prem vs. Edge Deployment
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 28 Jul 2026 21:23:05 +0000
email_id: 19faa9c1ec5cf9ba
article_id: 19faa9c1ec5cf9ba:1
published: '2026-07-28'
tags:
- Infra/gpu

---

# CPU vs GPU vs TPU vs NPU vs LPU

- **原邮件主题**: Serverless vs. On-prem vs. Edge Deployment
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 28 Jul 2026 21:23:05 +0000
- **ID**: 19faa9c1ec5cf9ba

---

## [**CPU vs GPU vs TPU vs NPU vs LPU**](<https://fff97757.click.kit-mail3.com/4zuwmw6lz0hehpxmvm3txh63p02rzf5h6ng99/7qh7h8h9r0qv5pazh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vaW1wbGVtZW50aW5nLW1hc3NpdmVseS1wYXJhbGxlbGl6ZWQtY3VkYS1wcm9ncmFtcy1mcm9tLXNjcmF0Y2gtdXNpbmctY3VkYS1wcm9ncmFtbWluZw==>)

5 hardware architectures power AI today.

Each one makes a fundamentally different tradeoff between flexibility, parallelism, and memory access.

The visual below maps the internal architecture of all five side by side:

![](https://substackcdn.com/image/fetch/$s_!UFKM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a2fea20-6b3c-49d7-9fe8-1326f8b1d21e_1250x1250.jpeg)   
---  
  
#### CPU

It is built for general-purpose computing. A few powerful cores handle complex logic, branching, and system-level tasks.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/4cFcSe3hu3p5r8UdHtC7dZ/email)   
---  
  
It has deep cache hierarchies and off-chip main memory (DRAM). It’s great for operating systems, databases, and decision-heavy code, but not that great for repetitive math like matrix multiplications.

#### GPU

Instead of a few powerful cores, GPUs spread work across thousands of smaller cores that all execute the same instruction on different data.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/be74uXjtJyZrL9S7isHvqc/email)   
---  
  
This is why GPUs dominate AI training. The parallelism maps directly to the kind of math neural networks need.

#### TPU

They go one step further with specialization.

The core compute unit is a grid of multiply-accumulate (MAC) units where data flows through in a wave pattern.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/dhYRfnLgrF4qACgX56Fc4p/email)   
---  
  
Weights enter from one side, activations from the other, and partial results propagate without going back to memory each time.

The entire execution is compiler-controlled, not hardware-scheduled. Google designed TPUs specifically for neural network workloads.

#### NPU

This is an edge-optimized variant.

The architecture is built around a Neural Compute Engine packed with MAC arrays and on-chip SRAM, but instead of high-bandwidth memory (HBM), NPUs use low-power system memory.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/9rGBZYGBphFvZMS29EyxdM/email)   
---  
  
The design goal is to run inference at single-digit watt power budgets, like smartphones, wearables, and IoT devices.

Apple Neural Engine and Intel’s NPU follow this pattern.

#### LPU (Language Processing Unit)

This is the newest entrant, by Groq.

The architecture removes off-chip memory from the critical path entirely. All weight storage lives in on-chip SRAM.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/xu1S6ybVQ32hveiJyo6ZG3/email)   
---  
  
Execution is fully deterministic and compiler-scheduled, which means zero cache misses and zero runtime scheduling overhead.

The tradeoff is that it provides limited memory per chip, which means you need hundreds of chips linked together to serve a single large model. But the latency advantage is real.

* * *

AI compute has evolved from general-purpose flexibility (CPU) to extreme specialization (LPU). Each step trades some level of generality for efficiency.

The visual below maps the internal architecture of all five side by side, and it was inspired by ByteByteGo’s post on CPU vs GPU vs TPU. We expanded it to include two more architectures that are becoming central to AI inference today.

![](https://substackcdn.com/image/fetch/$s_!M4eb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fa59656-7f14-4c9b-970f-14645fae90cf_1250x1250.jpeg)   
---  
  
That said, if you want to get hands-on with actual GPU programming using CUDA, learn about how CUDA operates GPU’s threads, blocks, grids (with visuals), etc., we covered it here: [](<https://fff97757.click.kit-mail3.com/4zuwmw6lz0hehpxmvm3txh63p02rzf5h6ng99/owhkhqhw24p3d7cvhr/aHR0cHM6Ly9zdWJzdGFjay5jb20vcmVkaXJlY3QvYTA5MjBiNTgtY2U4OS00NDhhLThmYzItOTIyOTQ4NDdmYmE0P2o9ZXlKMUlqb2ljREJ5YVRJaWZRLlFsckFybjR2Nl9vck5SZmtlTVI3SmR3VkdScjRIZjNiT3daS2pPVDd5cWc=>)[**Implementing (Massively) Parallelized CUDA Programs From Scratch Using CUDA Programming**](<https://fff97757.click.kit-mail3.com/4zuwmw6lz0hehpxmvm3txh63p02rzf5h6ng99/7qh7h8h9r0qv5pazh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vaW1wbGVtZW50aW5nLW1hc3NpdmVseS1wYXJhbGxlbGl6ZWQtY3VkYS1wcm9ncmFtcy1mcm9tLXNjcmF0Y2gtdXNpbmctY3VkYS1wcm9ncmFtbWluZw==>).

👉 Over to you: Which of these 5 have you actually worked with or deployed on?
