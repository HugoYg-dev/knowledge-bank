---
title: " 12 optimizers for training neural networks "
source_key: "dailydoseofds"
email_subject: "12 Optimizers for Training Neural Networks, clearly explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Mon, 02 Nov 2026 21:31:12 +0000"
email_id: "1a19e2c67284daff"
article_id: "1a19e2c67284daff:2"
published: "2026-11-02"
content_tier: "email_fallback"
tags: []
---

#  12 optimizers for training neural networks 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 12 Optimizers for Training Neural Networks, clearly explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 02 Nov 2026 21:31:12 +0000
- **邮件 ID**: 1a19e2c67284daff
- **文章 ID**: 1a19e2c67284daff:2
- **内容层级**: email_fallback

---

## [**12 optimizers for training neural networks**](<https://www.dailydoseofds.com/where-did-the-assumptions-of-linear-regression-originate-from/>)

An optimizer can reduce the number of training steps and still make your run slower. Each update has its own compute and memory cost, which becomes part of the training budget.

That tradeoff gets easier to reason about once you look at what each optimizer stores and how it transforms the gradient.

The 12 optimizers in the visual approach this differently. Let’s break them down through the engineering decisions they change, starting with how much gradient history survives each update.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/s4Qq3eFzWnaxvCcJyrpW35) Each of the 12 optimizers changes what it stores and how it turns the gradient into an update.  
---  
  
#### **Smoothing gradients and adapting step sizes**

SGD with momentum keeps a running accumulation of gradients. Directions that persist across batches build up, while inconsistent directions tend to cancel.

This helps reduce oscillation, but momentum alone doesn’t give each parameter its own adaptive step size.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/v9BAonks4WecDApk79Tgw3) Momentum averages away the back-and-forth across the valley, so the steady direction builds speed.  
---  
  
AdaGrad adds that adaptation by accumulating squared gradients for each parameter. Frequently updated parameters receive progressively smaller effective steps, which can help with sparse features.

Its limitation follows directly from that accumulation: the denominator keeps growing, so effective learning rates can become too small.

RMSprop replaces the full accumulation with an exponential moving average of squared gradients. Older observations fade, allowing the scaling to respond to more recent gradients.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/jKdLzxm58xwwGZ7MKP92Kw) AdaGrad’s sum only grows, so its steps shrink toward zero, while RMSprop’s moving average lets old gradients fade.  
---  
  
Adam combines momentum with this second-moment scaling. One moving average tracks gradient direction; another tracks squared gradient magnitude.

That second quantity isn’t a direct curvature measurement. Adam adapts to gradient statistics without estimating the Hessian.

#### **Changing regularization, memory, and gradient history**

AdamW separates weight decay from the adaptive gradient update. Adding an L2 penalty to Adam’s loss lets its adaptive scaling affect that penalty; decoupled weight decay applies parameter shrinkage separately.

That distinction matters when you’re tuning regularization. Weight decay becomes easier to reason about independently of the gradient scaling.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/dPdTeAqkBpjxG4zxTygpoj) With L2 inside Adam, the penalty gets divided by √v too, while AdamW applies the decay to the weights directly.  
---  
  
Memory introduces another constraint. Standard Adam maintains two parameter-sized state arrays, in addition to the model weights and gradients.

With one billion parameters and FP32 moment buffers, those two arrays alone require about 8 GB before sharding or compression.

Adafactor reduces the second-moment storage for matrices using row and column statistics. For an n × m matrix, that replaces nm stored second-moment values with roughly n+m.

You’re trading a full per-parameter estimate for a factored approximation. That’s useful when optimizer state limits the model or batch size you can fit.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/eu7xuaY6tGVHYpzDHSSEBr) Adam’s two FP32 moment buffers take 8 GB at 1B parameters, while Adafactor keeps n + m statistics per matrix instead of n × m.  
---  
  
Lion keeps momentum without a second-moment buffer. Its gradient update uses the sign of a momentum-gradient blend, giving coordinates the same update magnitude within a parameter group.

That changes the update scale, so copying AdamW’s learning rate into Lion isn’t a fair comparison. The Lion paper specifically calls for smaller learning rates.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/bxjZr7u7NrDExN6ijBNG1D) Lion keeps only the sign of the momentum-gradient blend, so every coordinate moves by the same amount.  
---  
  
AdEMAMix takes another approach: it combines fast and slow moving averages of gradients alongside second-moment scaling. Recent gradients remain influential while older directional information survives longer, at the cost of additional state.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/ehK7DPH75xtxGpo9rDcR9X) A fast EMA follows recent gradients while a slow EMA keeps older directions in the update.  
---  
  
#### **Using matrix structure and curvature**

Adam scales coordinates individually. Shampoo uses matrix-valued statistics to transform updates across parameter dimensions, capturing relationships that elementwise scaling misses.

Those richer statistics bring additional storage and matrix computation.

SOAP connects this approach back to Adam. It rotates gradients into the eigenbasis of Shampoo’s preconditioners, applies Adam there, and rotates the update back.

The coordinate system changes how Adam’s elementwise scaling acts on the update. Computing and refreshing that basis also adds overhead.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/9rC8NBSPXzgtk9XCHhwFeq) Shampoo preconditions the gradient from both sides, and SOAP runs Adam in the eigenbasis of those preconditioners.  
---  
  
Muon approximately orthogonalizes momentum updates for matrix parameters using Newton–Schulz iterations. It changes the matrix update’s singular-value structure rather than scaling every coordinate independently.

Parameter selection matters here. Muon is typically applied to hidden weight matrices, with another optimizer handling embeddings, output layers, and vector parameters.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/6mRa7tmPND1vRgdsRc36dL) Muon evens out the singular values of hidden-matrix updates, while embeddings, the output layer, and vector parameters stay on AdamW.  
---  
  
Sophia uses a diagonal curvature estimate to scale momentum, then clips updates elementwise. Its curvature estimate is refreshed periodically, limiting the average overhead of obtaining that information.

#### **Comparing optimizers on your workload**

I’d use AdamW as the reference run for a transformer experiment, then choose alternatives against a specific constraint.

For memory pressure, investigate Adafactor or Lion. For matrix updates, evaluate Muon, Shampoo, or SOAP while accounting for their parameter coverage and implementation costs.

Give each optimizer a learning-rate search. Keep the data, model, and evaluation protocol consistent, and report both validation quality at a fixed compute budget and time to a target quality.

Also measure peak memory and step time. An optimizer that reaches the target in 20% fewer steps but makes each step 30% slower takes about 4% longer overall.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/qn3pdesiu5e5DA3zeE94HR) 80 steps at 1.3 s each take 104 s, so 20% fewer steps still lose to the 100 s baseline on the clock.  
---  
  
The useful result is a reproducible improvement under your training constraints, including the cost of tuning it.

If you want to build these foundations properly, our Classical ML and Deep Learning roadmap covers the full stack in order, from the assumptions behind linear models to neural network training and the architectures built on top:

[**Start the Classical ML and Deep Learning roadmap →**](<https://www.dailydoseofds.com/where-did-the-assumptions-of-linear-regression-originate-from/>)

👉 Over to you: Which optimizer has improved your training runs enough to justify changing your default?
