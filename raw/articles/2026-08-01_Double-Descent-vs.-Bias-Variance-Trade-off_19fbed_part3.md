---
title: Double Descent vs. Bias-Variance Trade-off
source_key: dailydoseofds
email_subject: ​Build a Stock Market Research Agentic Workflow​
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Sat, 01 Aug 2026 19:38:29 +0000
email_id: 19fbed5d2cd155dd
article_id: 19fbed5d2cd155dd:1
published: '2026-08-01'
tags:
- MachineLearning
- DeepLearning

---

# Double Descent vs. Bias-Variance Trade-off

- **原邮件主题**: ​Build a Stock Market Research Agentic Workflow​
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 01 Aug 2026 19:38:29 +0000
- **ID**: 19fbed5d2cd155dd

---

## **Double Descent vs. Bias-Variance Trade-off**

It is well-known that as the number of model parameters increases, the model gradually overfits the data.

For instance, consider fitting a polynomial regression model trained on this dummy dataset below:

![](https://substackcdn.com/image/fetch/$s_!Q9WH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36f1c853-be3c-44a0-aebd-46feee2fb33a_1332x676.png)   
---  
  
In case you don’t know, this is called a polynomial regression model:

![](https://substackcdn.com/image/fetch/$s_!zcWU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdddae24e-d5ac-4da8-9173-599a92968871_2656x676.png)   
---  
  
Here, as we’ll increase the degree (`m`):

  * The training loss will get closer to zero.
  * The test (or validation) loss will first decrease and then increase.

This is also evident from the following loss plot:

![](https://substackcdn.com/image/fetch/$s_!_gaF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1576320a-f8dd-4405-a677-0f94e09b2c57_1724x820.png)   
---  
  
But notice what happens when you continue increasing the degree (`m`):

![](https://substackcdn.com/image/fetch/$s_!sloX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F129ff991-6c05-43b3-a100-88e6eaab16a6_1884x964.png)   
---  
  
Why does the test loss increase to a certain point but then decrease again?

What you see here is called the “double descent phenomenon,” and it is commonly observed in many deep learning models.

It depicts that increasing the model complexity beyond the point of interpolation can improve generalization performance.

And it’s hard to fathom since it challenges the traditional bias-variance trade-off:

![](https://substackcdn.com/image/fetch/$s_!ne4P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93d53257-e78b-4d4d-8c59-060097efc60b_1684x816.png)   
---  
  
To the best of our knowledge, this is still an open question, and it isn’t entirely clear why neural networks exhibit this behavior.

Some theories suggest that the model applies an implicit regularization that allows it to precisely focus on an apt number of parameters for generalization.

You can actually try it yourself:

  * Create a small dummy dataset of size n.
  * Train a polynomial regression of degree m, starting from 1 to a value greater than n.
  * Plot the test loss and training loss for each m.

👉 Over to you: What do you think about the possible causes?
