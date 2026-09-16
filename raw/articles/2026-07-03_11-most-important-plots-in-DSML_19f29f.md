---
title: 11 most important plots in DS/ML
source_key: dailydoseofds
email_subject: Prompt, Context, Harness & Loop Engineering
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 03 Jul 2026 21:51:22 +0000
email_id: 19f29f70428b228f
article_id: 19f29f70428b228f:1
published: '2026-07-03'
tags:
- MachineLearning

---

# 11 most important plots in DS/ML

- **原邮件主题**: Prompt, Context, Harness & Loop Engineering
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 03 Jul 2026 21:51:22 +0000
- **ID**: 19f29f70428b228f

---

## **11 most important plots in DS/ML**

This visual depicts the 11 most important and must-know plots in DS:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F286632a3-be0e-45ba-bfa2-dfdaa275d090_793x944.gif)   
---  
  
Today, let’s understand them briefly and how they are used.

# **1) KS Plot:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25a87b56-cedd-4938-9363-5c76e09c1b72_1244x676.png)   
---  
  
  * It is used to assess the distributional differences.
  * The idea is to measure the maximum distance between the cumulative distribution functions (CDF) of two distributions.
  * The lower the maximum distance, the more likely they belong to the same distribution.

# **2) SHAP Plot:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d9a3c85-2d42-4453-9dad-20ae24da3994_1208x776.png)   
---  
  
  * It summarizes feature importance to a model’s predictions by considering interactions/dependencies between them.
  * It is useful in determining how different values (low or high) of a feature affect the overall output.
  * We covered model interpretability extensively in our 3-part crash course. Start here: [**A Crash Course on Model Interpretability →**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8kdnera3hg95p5nrighgmk33/7qh7h8h923nm8gczh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYS1jcmFzaC1jb3Vyc2Utb24tbW9kZWwtaW50ZXJwcmV0YWJpbGl0eS1wYXJ0LTEv>)

# **3) ROC Curve:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F474c275c-114a-4e25-a35a-d87199b799b8_1200x716.png)   
---  
  
  * It depicts the tradeoff between the true positive rate (good performance) and the false positive rate (bad performance) across different classification thresholds.
  * The idea is to balance TPR (good performance) vs. FPR (bad performance).

# **4) Precision-Recall Curve:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1827901-140d-440e-ad1a-399bfab36e0f_1448x676.png)   
---  
  
  * It depicts the tradeoff between Precision and Recall across different classification thresholds.

# **5) QQ Plot:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0725182f-9dbd-41ca-880e-7d789abc8bc5_1272x704.png)   
---  
  
  * It assesses the distributional similarity between observed data and theoretical distribution.
  * It plots the quantiles of the two distributions against each other.
  * Deviations from the straight line indicate a departure from the assumed distribution.

#  **6) Cumulative Explained Variance Plot** :

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa79c8fc6-4092-403b-aba9-a5b6b38e04d8_1468x688.png)   
---  
  
  * It is useful in determining the number of dimensions we can reduce our data to while preserving max variance during PCA.
  * Read the full article on PCA here for more clarity: [**Formulating the Principal Component Analysis (PCA) Algorithm From Scratch**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8kdnera3hg95p5nrighgmk33/owhkhqhwm5q7l3uvhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZm9ybXVsYXRpbmctdGhlLXByaW5jaXBhbC1jb21wb25lbnQtYW5hbHlzaXMtYWxnb3JpdGhtLWZyb20tc2NyYXRjaC8=>).

# **7) Elbow Curve:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccf1a5ed-bdbd-4543-a993-7f27f5ace198_1336x688.png)   
---  
  
  * The plot helps identify the optimal number of clusters for the k-means algorithm.
  * The point of the elbow depicts the ideal number of clusters.

# **8) Silhouette Curve:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd0676d3-17cc-40eb-8928-b3f0a8f931f2_1456x1380.png)   
---  
  
  * The Elbow curve is often ineffective when you have plenty of clusters.
  * Silhouette Curve is a better alternative, as depicted above.

# **9) Gini-Impurity and Entropy:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1dd132d-25f8-4091-854d-2d5eb6e5381d_1308x676.png)   
---  
  
  * They are used to measure the impurity or disorder of a node or split in a decision tree.
  * The plot compares Gini impurity and Entropy across different splits.
  * This provides insights into the tradeoff between these measures.

#  **10) Bias-Variance Tradeoff** :

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0437d11-f1b1-4ef2-ac24-05522e472593_1496x676.png)   
---  
  
  * It’s probably the most popular plot on this list.
  * It is used to find the right balance between the bias and the variance of a model against complexity.

# **11) Partial Dependency Plots:**

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F727cfc1e-bb11-4961-8938-176bbe8f6bfa_1276x676.png)   
---  
  
  * Depicts the dependence between target and features.
  * A plot between the target and one feature forms → 1-way PDP.
  * A plot between the target and two feature forms → 2-way PDP.
  * In the leftmost plot, an increase in temperature generally results in a higher target value.
  * We covered model interpretability extensively in our 3-part crash course. Start here: [**A crash course on model interpretability →**](<https://fff97757.click.kit-mail3.com/27uprpxd03foh8kdnera3hg95p5nrighgmk33/7qh7h8h923nm8gczh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vYS1jcmFzaC1jb3Vyc2Utb24tbW9kZWwtaW50ZXJwcmV0YWJpbGl0eS1wYXJ0LTEv>)

👉 Over to you: Which important plots have I missed here?
