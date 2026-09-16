---
title: Memory Pinning to accelerate model training
source_key: dailydoseofds
email_subject: Memory Pinning to Accelerate Model Training
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Wed, 07 May 2025 19:30:13 +0000
email_id: 196ac3a283f20357
article_id: 196ac3a283f20357:1
published: '2025-05-07'
tags:
- DeepLearning
- Skill/python
- Infra/training

---

# Memory Pinning to accelerate model training

- **原邮件主题**: Memory Pinning to Accelerate Model Training
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 07 May 2025 19:30:13 +0000
- **ID**: 196ac3a283f20357

---

## **Memory Pinning to accelerate model training**

If you regularly use GPUs to accelerate model training, let us show you a simple technique to accelerate model training…

…by changing just two lines of code.

Let’s begin!

* * *

Here’s how we typically train a neural network using PyTorch:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5b739f4-38ff-4caf-94d7-01490c333363_1456x958.png)   
---  
  
  * Line 5 transfers the data to the GPU from the CPU.
  * Everything executes on the GPU after the data transfer, i.e., lines 7-15.

This means:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe437cb84-f778-46d5-a010-5e254cff7d5f_1740x676.png)   
---  
  
  * When the GPU is working, the CPU is idle,
  * And when the CPU is working, the GPU is idle.

This can be optimized as follows:

  * When the model is being trained on the 1st mini-batch, the CPU can transfer the 2nd mini-batch to the GPU.
  * This ensures that the GPU does not have to wait for the next mini-batch as soon as it has processed the current mini-batch.

Thus, the resource utilization chart should look like:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00a246a7-bcd3-4fb6-91f2-8e0bf76e56f7_1916x676.png)   
---  
  
While the CPU may remain idle, this ensures that the GPU (which is the actual accelerator) is never idle.

This is known as **memory pinning** , and it is used to speed up the data transfer from the CPU to the GPU by making the training workflow asynchronous.

Enabling this is quite simple in PyTorch.

1) First, when defining the DataLoader object, set `pin_memory=True` and specify `num_workers`.

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fc81815-cdf2-40d1-a623-04d758221ee8_1456x458.png)   
---  
  
2) During the data transfer step in the training step, specify `non_blocking=True`, as depicted below:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85ca03e3-8876-4137-97fa-4e726b48f94b_1456x770.png)   
---  
  
Done!

The speedup with a simple neural network is depicted below:

  * Without memory pinning, the model takes 43 seconds to train on 5 epochs.

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda9a47a8-388c-4de9-9614-18dc75009b9d_1456x518.png)   
---  
  
  * But with memory pinning, the same model trains in less than 10 seconds:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd52321e9-afe7-41eb-b4d6-14e1b58005c2_1456x599.png)   
---  
  
That said, remember that if several tensors are allocated to the pinned memory, it will block a substantial portion of RAM. 

This impacts the memory available to other operations. Thus, always profile your code to track the memory consumption.

Also, if the tensors are small, memory pinning has a negligible effect since the data transfer from the CPU to the GPU does not take that time anyway:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6350bff1-4524-446b-a403-be59491c727f_1688x732.png)   
---  
  
👉 Over to you: What are some other ways to optimize model training?

One way is multi-GPU training, which we covered here: [**A Beginner-friendly Guide to Multi-GPU Model Training**](<https://www.dailydoseofds.com/a-beginner-friendly-guide-to-multi-gpu-model-training/>)**.**

And here are 15 more ways to optimize neural network training: [**15 Ways to Optimize Neural Network Training (With Implementation)**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>).

Lastly, here’s an article that teaches CUDA programming from scratch, which will help you understand the underlying details of CUDA and how it works: [**Implementing (Massively) Parallelized CUDA Programs From Scratch Using CUDA Programming**](<https://www.dailydoseofds.com/implementing-massively-parallelized-cuda-programs-from-scratch-using-cuda-programming/>)**.**
