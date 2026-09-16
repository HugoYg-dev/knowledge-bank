---
title: A subtle neural network optimization technique
source_key: dailydoseofds
email_subject: Avoid Using PCA for Visualization Unless...
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Sat, 18 Oct 2025 20:59:57 +0000
email_id: 199f91f3eaa6509e
article_id: 199f91f3eaa6509e:1
published: '2025-10-18'
tags:
- DeepLearning
- Skill/data-analysis
- Infra/gpu
- Infra/training

---

# A subtle neural network optimization technique

- **原邮件主题**: Avoid Using PCA for Visualization Unless...
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 18 Oct 2025 20:59:57 +0000
- **ID**: 199f91f3eaa6509e

---

## [**A subtle neural network optimization technique**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>)

Imagine an image classification task, say, MNIST, for simplicity.

Normalizing/scaling the pixel values is a common technique to stabilize model training.

Here’s what the implementation looks like:

  * First, we load the dataset, transform it, define the model, etc.
  * Next, we have the training loop where the data is transferred to the GPU.

Here's the problem with this approach:

If you look at the profiler:

  * Most of the time/resources will be allocated to the kernel (the actual training code).
  * However, a significant amount of time will also be dedicated to data transfer from CPU to GPU.

Reducing the data transfer is simple.

Recall that the original dataset was composed of pixel values. These were 8-bit integers, and we normalized them to 32-bit floats.

Next, we transferred these 32-bit floating-point tensors to the GPU. This meant that normalizing the data led to more data being transferred.

Solution?

Moving the normalization step after the data transfer will solve this, since we shall be transferring 8-bit integers instead of 32-bit floats.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/9ogxgy9Tye6uZT7sjDDB5L/email)   
---  
  
As a result, you will notice a significant drop in the data transfer step.

Of course, this technique doesn’t apply to all neural network use cases, like NLP, where we inherently deal with 32-bit float embeddings.

[**We implemented 15 more techniques to optimize neural network training here →**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>)

👉 Over to you: What are some lesser-known ways of optimizing model training that you are aware of?
