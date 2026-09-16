---
title: 4 ways to test ML models in production
source_key: dailydoseofds
email_subject: 4 Ways to Test ML Models in Production
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 03 Feb 2025 19:22:45 +0000
email_id: 194cd43e281f59cc
article_id: 194cd43e281f59cc:1
published: '2025-02-03'
tags:
- MachineLearning
- Infra/platform

---

# 4 ways to test ML models in production

- **原邮件主题**: 4 Ways to Test ML Models in Production
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 03 Feb 2025 19:22:45 +0000
- **ID**: 194cd43e281f59cc

---

## [**4 ways to test ML models in production**](<https://www.dailydoseofds.com/5-must-know-ways-to-test-ml-models-in-production-implementation-included>)  
  
Continuing the discussion from agent testing…

…the following visual depicts 4 strategies to test ML models in production:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a8b694f-87c0-4109-937c-482a0eff6e37_1198x1092.gif) Current model is called the legacy model, and new model is called the candidate model.  
---  
  
We covered one more technique (Multi-armed bandits deployments) and the implementation of all five techniques: [**5 Must-Know Ways to Test ML Models in Production (Implementation Included)**](<https://www.dailydoseofds.com/5-must-know-ways-to-test-ml-models-in-production-implementation-included>).

* * *

# **Why care?**

Despite rigorously testing an ML model locally (on validation and test sets), it could be a terrible idea to instantly replace the previous model with the new model.

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7db6208-37b7-4cd6-b004-c8a4a494631a_1820x676.png)   
---  
  
A more reliable strategy is to test the model in production (yes, on real-world incoming data).

While this might sound risky, ML teams do it all the time, and it isn’t that complicated.

* * *

# **#1) A/B testing**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc361e6f-bc8b-4673-b3b8-ada70f1a27b7_3368x704.png)   
---  
  
  * Distribute the incoming requests **non-uniformly** between the legacy model and the candidate model.
  * Limit the exposure of the candidate model to avoid any potential risks.

* * *

# **#2) Canary testing**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0ad2e03-ad3d-4a7c-9d0f-1cfc31fb1224_3392x904.png)   
---  
  
  * A/B testing may affect all users since it randomly distributes “traffic” to either model (irrespective of the user).
  * In canary testing, the candidate model is exposed to a small subset of users in production and gradually rolled out to more users.

* * *

# **#3) Interleaved testing**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F357e35c0-c475-4430-983f-336bffd93f1a_3364x700.png)   
---  
  
  * This involves mixing the predictions of multiple models in the response.
  * Consider Amazon’s recommendation engine. In interleaved deployments, some product recommendations displayed on their homepage can come from the legacy model, and others from the candidate model.

* * *

# **#4) Shadow testing**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef5c13c2-46d3-47e8-a5a0-d0ebb6a5fb73_3364x828.png)   
---  
  
  * All of the above techniques affect some (or all) users.
  * Shadow testing (or dark launches) lets us test a new model in a production environment **without affecting the user experience**.
  * The candidate model is deployed alongside the existing legacy model and serves requests like the legacy model. However, the output is not sent back to the user. Instead, the output is logged for later use to benchmark its performance against the legacy model.
  * We explicitly deploy the candidate model instead of testing offline because the exact production environment can be difficult to replicate offline.
  * Shadow testing offers risk-free testing of the candidate model in a production environment.

* * *

That said, don't forget to check out [**Maxim**](<https://dub.sh/maxim-ai-eval>) for Agent testing.

[**Test Agents with Maxim**](<https://dub.sh/maxim-ai-eval>)  
---  
  
It provides an end-to-end evaluation and observability platform that will help you ship AI agents reliably and **> 5x faster!**

👉 Over to you: Which ML testing technique looks most interesting to you?

Thanks for reading!
