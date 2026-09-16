---
title: Build portable ML models with ONNX
source_key: dailydoseofds
email_subject: The No. 1 Deep Researcher Beats Claude and ChatGPT Using a Counterintuitive
  Trick
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 25 May 2026 20:09:08 +0000
email_id: 19e60c170373504b
article_id: 19e60c170373504b:1
published: '2026-05-25'
tags:
- Infra/serving

---

# Build portable ML models with ONNX

- **原邮件主题**: The No. 1 Deep Researcher Beats Claude and ChatGPT Using a Counterintuitive Trick
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 25 May 2026 20:09:08 +0000
- **ID**: 19e60c170373504b

---

## [**Build portable ML models with ONNX**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8z5z2df3hg973v5wsghgmk33/l2hehmhl9ow44dh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWxvcHMtY3Jhc2gtY291cnNlLXBhcnQtMTAv>)

Most ML teams train models in PyTorch or TensorFlow, but production systems don’t care about it.

They care about speed, portability, and stability.

This disconnect between training and serving is where most deployment headaches begin.

You might train a model in PyTorch, but your inference stack could be a C++ service, a mobile device, a GPU-optimized runtime, or a CPU-only production environment.

![](https://substackcdn.com/image/fetch/$s_!A-5x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F080ae02d-3684-433c-bea2-7531caabf3b2_1209x752.png)   
---  
  
Without a common format, every framework-to-runtime transition becomes a custom engineering problem, and teams end up rewriting export logic for each deployment target.

This is exactly the problem ONNX (Open Neural Network Exchange) was built to solve, and the visual below captures why it exists in the first place.

![](https://substackcdn.com/image/fetch/$s_!PqST!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5730a6c-39fa-42a1-864f-bb3911694340_960x439.webp)   
---  
  
Let’s break it down.

_On a side note, we’ve already covered ONNX in depth as part of our 18-part MLOps course, where we walk through several such concepts and tools step-by-step._

[** _Learn deployment with ONNX in a hands-on manner here →_**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8z5z2df3hg973v5wsghgmk33/l2hehmhl9ow44dh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWxvcHMtY3Jhc2gtY291cnNlLXBhcnQtMTAv>)

* * *

# What ONNX actually is

ONNX acts as a framework-agnostic intermediate representation that sits between training and deployment.

An ONNX model is essentially a saved computation graph with standardized operators, explicit tensor shapes, metadata, and all weights baked in.

Think of it as a neutral language for neural networks.

PyTorch and TensorFlow can export to ONNX, and production runtimes can consume from ONNX, which makes models portable across training frameworks and deployment targets.

![](https://substackcdn.com/image/fetch/$s_!OEKl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f721df6-fde8-4eb3-ae8b-04108da33fdc_1456x1103.png)   
---  
  
# Why operator standardization matters

Every framework has its own internal representation for operations.

ONNX defines a common operator set so exporters can map framework-specific ops to a shared vocabulary.

![](https://substackcdn.com/image/fetch/$s_!IL8-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b88a17a-d049-4195-87f0-9275fa0b04a9_1024x572.png)   
---  
  
# Where ONNX Runtime comes in

ONNX by itself is just a format, a way to represent models.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/cmjAvGL3cBazZ1yN7pcnH6/email)   
---  
  
ONNX Runtime (ORT) is the execution engine that turns that format into fast inference.

Under the hood, ORT loads the ONNX graph, applies graph-level optimizations, partitions the graph across hardware backends, and executes each subgraph efficiently.

All of this happens automatically once you load and run the model.

![](https://substackcdn.com/image/fetch/$s_!eQkA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0796145-8fac-4ac1-a125-63269307bbed_1456x708.png)   
---  
  
Here’s a glimpse of the output when we use ONNX and ORT for simple MNIST label prediction:

![](https://substackcdn.com/image/fetch/$s_!BAcP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9671f4de-4f26-4549-978d-a0042d5ca78b_1456x630.png)   
---  
  
That said, ONNX isn’t magic since there are some important caveats to know about.

  * Not every framework op maps perfectly to ONNX operators
  * Execution Provider coverage varies across hardware targets
  * Graph partitioning is heuristic-based, not guaranteed optimal
  * Startup time can increase depending on model complexity
  * Mixed precision inference can introduce small numerical drift
  * Custom ops require additional engineering effort to support

ONNX simplifies deployment significantly, but it doesn’t remove the need for careful validation before going to production.

If you remember just one thing, remember this flow:

![](https://substackcdn.com/image/fetch/$s_!YZHB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d6ddd91-6692-4ab2-aa16-f25769d3f79d_1046x477.png)   
---  
  
  1. Train model in PyTorch or TensorFlow
  2. Export to ONNX
  3. Run anywhere using ONNX Runtime

That’s the bridge ONNX provides between the framework you love and the runtime you need.

[**To see this end-to-end with complete code and context, we’ve already covered ONNX as part of our MLOps course, including export, runtime execution, and trade-offs. Read here →**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8z5z2df3hg973v5wsghgmk33/l2hehmhl9ow44dh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWxvcHMtY3Jhc2gtY291cnNlLXBhcnQtMTAv>)

[**Also, to start from the foundations and build up to this ONNX stage (and beyond), you can begin here →**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8z5z2df3hg973v5wsghgmk33/m2h7h5h3pow99xtm/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbWxvcHMtY3Jhc2gtY291cnNlLXBhcnQtMS8=>)

👉 Over to you: Where did you use ONNX recently, and what’s stopping you from using it more?
