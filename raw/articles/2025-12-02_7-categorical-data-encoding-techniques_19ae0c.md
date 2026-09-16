---
title: 7 categorical data encoding techniques
source_key: dailydoseofds
email_subject: 7 Categorical Data Encoding Techniques
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 02 Dec 2025 20:34:54 +0000
email_id: 19ae0c67c504face
article_id: 19ae0c67c504face:1
published: '2025-12-02'
tags:
- MachineLearning

---

# 7 categorical data encoding techniques

- **原邮件主题**: 7 Categorical Data Encoding Techniques
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 02 Dec 2025 20:34:54 +0000
- **ID**: 19ae0c67c504face

---

## **7 categorical data encoding techniques**

Here are 7 ways to encode categorical features:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25e58739-0a9f-42ab-bba6-f932cee49139_962x1120.gif)   
---  
  
* * *

# **1) One-hot encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/5piywkUj2SFDMKvENA8wAW/email)   
---  
  
  * Each category is represented by a binary vector of 0s and 1s. 
  * Each category gets its own binary feature, and only one of them is "hot" (set to 1) at a time, indicating the presence of that category.
  * Number of features = Number of unique categorical labels

# **2) Dummy encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/cp7mwkvzqqN967qAPxFr3P/email)   
---  
  
  * Same as one-hot encoding but with one additional step.
  * After one-hot encoding, we drop a feature randomly.
  * This is done to avoid the dummy variable trap. We covered this here, along with 8 more lesser-known pitfalls and cautionary measures that you will likely run into in your DS projects: [**8 Fatal (Yet Non-obvious) Pitfalls and Cautionary Measures in Data Science**](<https://www.dailydoseofds.com/8-fatal-yet-non-obvious-pitfalls-and-cautionary-measures-in-data-science/>).
  * Number of features = Number of unique categorical labels - 1.

# **3) Effect encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/eDjqfcpAMkog8u5VXyUqTE/email)   
---  
  
  * Similar to dummy encoding but with one additional step.
  * Alter the row with all zeros to -1.
  * This ensures that the resulting binary features represent not only the presence or absence of specific categories but also the contrast between the reference category and the absence of any category.
  * Number of features = Number of unique categorical labels - 1.

# **4) Label encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/udDimyaxugXsYdp72wSHf7/email)   
---  
  
  * Assign each category a unique label.
  * Label encoding introduces an inherent ordering between categories, which may not be the case.
  * Number of features = 1.

# **5) Ordinal encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/79P8S6bSrnhtgbza3Ef2JC/email)   
---  
  
  * Similar to label encoding, assign a unique integer value to each category.
  * The assigned values have an inherent order, meaning that one category is considered greater or smaller than another.
  * Number of features = 1.

# **6) Count encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/hvjSGrcyqSEca6RnGVtrrv/email)   
---  
  
  * Also known as frequency encoding.
  * Encodes categorical features based on the frequency of each category.
  * Thus, instead of replacing the categories with numerical values or binary representations, count encoding directly assigns each category with its corresponding count.
  * Number of features = 1.

# **7) Binary encoding**

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/wF8ngGrAPCmi8WxRNMhvFz/email)   
---  
  
  * Combination of one-hot encoding and ordinal encoding.
  * It represents categories as binary code.
  * Each category is first assigned an ordinal value, and then that value is converted to binary code.
  * The binary code is then split into separate binary features.
  * Useful when dealing with high-cardinality categorical features (or a high number of features) as it reduces the dimensionality compared to one-hot encoding.
  * Number of features = log(n) (in base 2).

While these are some of the most popular techniques, do note that these are not the only techniques for encoding categorical data.

You can try plenty of techniques with the [**category-encoders**](<https://pypi.org/project/category-encoders/>) library.

👉 Over to you: What other common categorical data encoding techniques have I missed?
