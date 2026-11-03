---
title: " 6 steps to build an ML model "
source_key: "dailydoseofds"
email_subject: "12 Optimizers for Training Neural Networks, clearly explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Mon, 02 Nov 2026 21:31:12 +0000"
email_id: "1a19e2c67284daff"
article_id: "1a19e2c67284daff:3"
published: "2026-11-02"
content_tier: "email_fallback"
tags: []
---

#  6 steps to build an ML model 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 12 Optimizers for Training Neural Networks, clearly explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 02 Nov 2026 21:31:12 +0000
- **邮件 ID**: 1a19e2c67284daff
- **文章 ID**: 1a19e2c67284daff:3
- **内容层级**: email_fallback

---

## [**6 steps to build an ML model**](<https://www.dailydoseofds.com/mlops-crash-course-part-1/>)

Building an ML model isn’t just about picking an algorithm and hitting train.

Getting it to production requires 6 steps, and the algorithm selection is just one of them.

Here’s the full breakdown:

![](https://substackcdn.com/image/fetch/$s_!ytPd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F555558d9-8eec-4ed5-98cd-05630b83f4b6_894x1010.png)   
---  
  
On a side note, we have already covered MLOps from a fully beginner-friendly perspective in our 18-part crash course.



It covers foundations, ML system lifecycle, reproducibility, versioning, data and pipeline engineering, Spark, model compression, Deployment phase, Kubernetes, cloud infra, virtualisation, deep dive into AWS, and monitoring in production.



[**Start with MLOps Part 1 here →**](<https://www.dailydoseofds.com/mlops-crash-course-part-1/>)

[**MLOps Crash Course Part 1**](<https://www.dailydoseofds.com/mlops-crash-course-part-1/>)  
---  
  
#### **Step 1: Setting objectives**

Before writing a single line of code, you need clarity.

What problem are you solving? Is ML even the right approach? What does success look like?

![](https://substackcdn.com/image/fetch/$s_!HIME!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad096ecd-4ecd-4518-b687-9ab01b12ee46_1253x213.png)   
---  
  
This means identifying the use case, running a feasibility study, and defining your KPIs upfront.

#### **Step 2: Data preparation**

This is where you’ll spend most of your time since no fancy algorithm fixes bad data.

![](https://substackcdn.com/image/fetch/$s_!CoQo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d1afa1d-c2eb-45bb-a999-32a6bda273f6_1253x213.png)   
---  
  
Here, you collect your data, clean it (handle missing values, outliers, inconsistencies), engineer meaningful features, and split it properly into train/validation/test sets.

#### **Step 3: Choose the algorithm**

Now you pick your approach, like Random Forest, XGBoost, Neural network, etc.

![](https://substackcdn.com/image/fetch/$s_!oBhV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F059f6329-d90b-4491-b0dc-76b9e57717f7_1253x213.png)   
---  
  
The choice depends on your problem type, data size, interpretability needs, and latency requirements.

Also, decide on your framework: scikit-learn for classical ML, TensorFlow, or PyTorch for deep learning.

#### **Step 4: Train the model**

Feed your prepared data to the model and let it learn.

![](https://substackcdn.com/image/fetch/$s_!0x1-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcba72e0c-682f-4245-bd46-def02f6569d3_1253x213.png)   
---  
  
But training isn’t a one-shot thing. Here, you iterate, adjust hyperparameters and experiment with different configurations.

This loop continues until performance plateaus.

#### **Step 5: Evaluate and test**

Now, you test how good your model really is.

Run it on your held-out test set. Analyze metrics relevant to your problem (accuracy, precision, recall, F1, AUC).

![](https://substackcdn.com/image/fetch/$s_!lkIB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecd93306-5a27-4bb0-9579-b63700910566_1253x213.png)   
---  
  
And don’t forget bias testing. Your model should work fairly across different segments.

#### **Step 6: Deploy and monitor**

![](https://substackcdn.com/image/fetch/$s_!A6RZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c49242-4c3c-47ba-a987-f7feecc10b09_1253x213.png)   
---  
  
Finally, you containerize it, deploy it to the cloud (AWS, GCP, Azure), and set up monitoring.

Moreover, since models degrade over time, you need to catch data drifts and other issues before your users do.

* * *

That’s the full picture.

The algorithm typically gets all the attention, but it’s maybe 15% of the work. The rest is Engineering, infra, and careful thinking.

If you want to see this in practice, we have already covered MLOps from a fully beginner-friendly perspective in our 18-part course.

It covers foundations, ML system lifecycle, reproducibility, versioning, data and pipeline engineering, Spark, model compression, deployment phase, Kubernetes, cloud infra, virtualisation, deep dive into AWS, and monitoring in production.

[**Start with MLOps Part 1 here →**](<https://www.dailydoseofds.com/mlops-crash-course-part-1/>)

[**MLOps Crash Course Part 1**](<https://www.dailydoseofds.com/mlops-crash-course-part-1/>)  
---  
  
👉 Over to you: Have we missed any step in the model-building process?
