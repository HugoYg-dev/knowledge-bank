---
title: Should you gather more data?
source_key: dailydoseofds
email_subject: ​MiniMax-M2 vs. Kimi-K2 vs. Sonnet 4.5 on Code Generation​
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Thu, 20 Nov 2025 19:55:54 +0000
email_id: 19aa2d674dcfaef6
article_id: 19aa2d674dcfaef6:1
published: '2025-11-20'
tags:
- MachineLearning

---

# Should you gather more data?

- **原邮件主题**: ​MiniMax-M2 vs. Kimi-K2 vs. Sonnet 4.5 on Code Generation​
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 20 Nov 2025 19:55:54 +0000
- **ID**: 19aa2d674dcfaef6

---

## **Should you gather more data?**

At times, no matter how much you try, the model performance barely improves:

  * Feature engineering gives a marginal improvement.
  * Trying different models does not produce satisfactory results either.
  * and more…

This is usually an indicator that we don’t have enough data to work with.

But since gathering new data can be a time-consuming and tedious process...

...here's a technique to determine whether more data will help:

![](https://substackcdn.com/image/fetch/$s_!FCDu!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F470ae846-8147-44c7-90d7-d1eabd46f6a6_1066x1140.gif)   
---  
  
  * Divide the dataset into “k” equal parts. Usually, 7 to 12 parts are fine.
  * Train models cumulatively on the above subsets and measure the performance on the validation set:

![](https://substackcdn.com/image/fetch/$s_!k8L1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38822747-31ee-435c-8b7f-484b8cf6a52b_2820x1500.png)   
---  
  
  * Train a model on the **first subset** only.
  * Train a model on the **first two subsets** only.
  * And so on…

Plotting the validation performance will produce one of these two lines:

![](https://substackcdn.com/image/fetch/$s_!urXm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7f2395e-72a0-4399-95b4-14780bff0371_1324x780.png)   
---  
  
  * Line A conveys that adding more data will likely increase the model's performance.
  * Line B conveys that the model's performance has already saturated. Adding more data will most likely not result in any considerable gains.

This way, you can ascertain whether gathering data will help.
