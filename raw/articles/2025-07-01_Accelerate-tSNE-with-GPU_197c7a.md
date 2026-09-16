---
title: Accelerate tSNE with GPU
source_key: dailydoseofds
email_subject: uv Cheatsheet and Hands-on Guide for Python Devs
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 01 Jul 2025 20:28:05 +0000
email_id: 197c7ace7fc9ab0e
article_id: 197c7ace7fc9ab0e:1
published: '2025-07-01'
tags:
- MachineLearning
- Infra/gpu

---

# Accelerate tSNE with GPU

- **原邮件主题**: uv Cheatsheet and Hands-on Guide for Python Devs
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 01 Jul 2025 20:28:05 +0000
- **ID**: 197c7ace7fc9ab0e

---

## **Accelerate tSNE with GPU**

The run-time of t-SNE is quadratically related to the number of data points.

Thus, it becomes difficult to use t-SNE from Sklearn implementations when your data has over 40k+ data points.

tSNE-CUDA is an optimized CUDA version of the tSNE algorithm. Thus, it provides immense speedups over the standard Sklearn implementation:

![](https://substackcdn.com/image/fetch/$s_!lpcj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53e8fc42-7d81-4ea2-a999-d1e75bc0ce6f_1456x1110.png)   
---  
  
As depicted above, the GPU-accelerated implementation is 33 times faster than the Sklearn implementation.

That said, this implementation only supports `n_components=2`, i.e., you can only project to two dimensions.

The authors do not intend to support more dimensions since this will require significant changes to the code.

But in my opinion, the support for more dimensions doesn’t matter because tSNE is used to generate 2D projections in 99% of the use cases.

These are the benchmarking results by the authors:

![](https://substackcdn.com/image/fetch/$s_!uvwb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f1fe3b2-d1a8-46f7-a83b-662b56a39315_1456x392.png)   
---  
  
It depicts that on the CIFAR-10 training set (50k images), tSNE-CUDA is 700x Faster than Sklearn.

Further reading:

  * This was just about tSNE, you can accelerate other ML algorithms with GPUs. Read this to learn more: [**Sklearn Models are Not Deployment Friendly! Supercharge Them With Tensor Computations**](<https://www.dailydoseofds.com/sklearn-models-are-not-deployment-friendly-supercharge-them-with-gpus-first/>)****[**.**](<https://www.dailydoseofds.com/sklearn-models-are-not-deployment-friendly-supercharge-them-with-gpus-first/>)****
  * Also, do you know how t-SNE works end-to-end? Read this to learn more: [**Formulating and Implementing the t-SNE Algorithm From Scratch**](<https://www.dailydoseofds.com/formulating-and-implementing-the-t-sne-algorithm-from-scratch/>).

