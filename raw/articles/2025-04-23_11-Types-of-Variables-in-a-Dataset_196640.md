---
title: 11 Types of Variables in a Dataset
source_key: dailydoseofds
email_subject: 11 Types of Variables in a Dataset
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Wed, 23 Apr 2025 18:56:17 +0000
email_id: 19664020d007efe2
article_id: 19664020d007efe2:1
published: '2025-04-23'
tags:
- Skill/data-analysis
content_tier: "web_canonical"
canonical_url: "https://www.dailydoseofds.com/p/11-types-of-variables-in-a-dataset/"
---

# 11 Types of Variables in a Dataset

- **原邮件主题**: 11 Types of Variables in a Dataset
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 23 Apr 2025 18:56:17 +0000
- **ID**: 19664020d007efe2
- **官网长文**: https://www.dailydoseofds.com/p/11-types-of-variables-in-a-dataset/
- **内容层级**: web_canonical

---

In any tabular dataset, we typically categorize the columns as either a feature or a target.

However, there are so many variables that one may find/define in their dataset, which I want to discuss today.

These are depicted in the animation below:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f74dcd89e-96e0-4a1a-864e-bf4a2abc2539_1204x1072-1.gif)

Let’s begin!

* * *

#### **# 1-2) Independent and dependent variables**

These are the most common and fundamental to ML.

Independent variables are the features that are used as input to predict the outcome. They are also referred to as **predictors/features/explanatory variables.**

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fe7c41cfb-bf18-48d2-b3d2-7dbf64cda703_590x230-1.png)

The dependent variable is the outcome that is being predicted. It is also called the target, response, or output variable.

* * *

#### **# 3-4) Confounding and correlated variables**

Confounding variables are typically found in a cause-and-effect study (causal inference).

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f22cb8f8c-9061-48fe-9282-7b8cb802cee8_249x231-1.png)

These variables are not of primary interest in the cause-and-effect equation but can potentially lead to spurious associations.

To exemplify, say we want to measure the effect of ice cream sales on the sales of air conditioners.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fdeb78665-3dc0-4ce0-8c70-20197bb20759_648x254-1.png)

As you may have guessed, these two measurements are highly correlated.

However, there’s a confounding variable — **temperature** , which influences both ice cream sales and the sales of air conditioners.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f3b0b9497-6279-4c14-a340-e950d7a9dfd6_757x260-1.png)

To study the true casual impact, it is essential to consider the confounder (temperature). Otherwise, the study will produce misleading results.

In fact, it is due to the confounding variables that we hear the statement: “Correlation does not imply causation.”

In the above example:

  * There is a high correlation between ice cream sales and sales of air conditioners.
  * But the sales of air conditioners (effect) are **NOT** caused by ice cream sales.

Also, in this case, the air conditioner and ice cream sales are **correlated variables**.

More formally, a change in one variable is associated with a change in another.

* * *

#### **#5) Control variables**

In the above example, to measure the true effect of ice cream sales on air conditioner sales, we must ensure that the temperature remains unchanged throughout the study.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f8936ca07-fa58-4d16-8225-6e92faac6446_757x240-1.png)

Once controlled, temperature becomes a **control variable**.

More formally, these are variables that are not the primary focus of the study but are crucial to account for to ensure that the effect we intend to measure is not biased or confounded by other factors.

* * *

#### **#6) Latent variables**

A variable that is not directly observed but is inferred from other observed variables.

For instance, we use clustering algorithms because the true labels do not exist, and we want to infer them somehow.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f866092b2-95f3-4ada-b034-e574d24b99b7_580x230-1.png)

The true label is a latent variable in this case.

Another common example of a latent variable is “intelligence.”

Intelligence itself cannot be directly measured; it is a latent variable.

However, we can infer intelligence through various observable indicators such as test scores, problem-solving abilities, and memory retention.

We also learned about Latent variables when we studied [**Gaussian mixture models**](<https://www.dailydoseofds.com/gaussian-mixture-models-gmm/>) if you remember.

* * *

#### **#7) Interaction variables**

As the name suggests, these variables represent the interaction effect between two or more variables, and are often used in regression analysis.

Here’s an instance I remember using them in.

In a project, I studied the impact of population density and income levels on spending behavior.

  * I created three groups for population density — HIGH, MEDIUM, and LOW (one-hot encoded).
  * Likewise, I created three groups for income levels — HIGH, MEDIUM, and LOW (one-hot encoded).

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fc8a4260c-0a97-48b4-aab1-c83eb84b35f3_639x240-1.png)

To do regression analysis, I created interaction variables by cross-multiplying both one-hot columns.

This produced 9 interaction variables:

  * Population-High and Income-High
  * Population-High and Income-Med
  * Population-High and Income-Low
  * Population-Med and Income-High
  * and so on…

Conducting the regression analysis on interaction variables revealed more useful insights than what I observed without them.

To summarize, the core idea is to study two or more variables together rather than independently.

* * *

#### **# 8-9)** Stationary and Non-Stationary variables:

The concept of stationarity often appears in time-series analysis.

Stationary variables are those whose statistical properties (mean, variance) DO NOT change over time.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f0197e3bc-30f1-4883-a267-0fbb3529fd10_720x277-1.png)

On the flip side, if a variable’s statistical properties change over time, they are called non-stationary variables.

Preserving stationarity in statistical learning is critical because these models are fundamentally reliant on the assumption that samples are identically distributed.

But if the probability distribution of variables is evolving over time, (non-stationary), the above assumption gets violated.

That is why, typically, using direct values of the non-stationary feature (like the absolute value of the stock price) is not recommended.

Instead, I have always found it better to define features in terms of relative changes:

$$ \frac{\delta P}{P} \rightarrow \text{relative change in stock price} $$

* * *

#### **#10)** Lagged variables

Talking of time series, lagged variables are pretty commonly used in feature engineering and data analytics.

As the name suggests, a lagged variable represents previous time points’ values of a given variable, essentially shifting the data series by a specified number of periods/rows.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f121deea9-e8bc-439c-83e6-f73ee95bbbcc_800x274-1.png)

For instance, when predicting next month’s sales figures, we might include the sales figures from the previous month as a lagged variable.

Lagged features may include:

  * 7-day lag on website traffic to predict current website traffic.
  * 30-day lag on stock prices to predict the next month’s closing prices.
  * And so on…

* * *

#### **#11)** Leaky variables

Yet again, as the name suggests, these variables (unintentionally) provide information about the target variable that would not be available at the time of prediction.

This leads to overly optimistic model performance during training but fails to generalize to new data.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f58c97651-a6a0-41d2-b65e-0b89270c3dcb_528x320-1.png)

I recently talked about leaky variable(s) in this newsletter through random splitting.

To reiterate, consider a dataset containing medical imaging data.

Each sample consists of **multiple images** (e.g., different views of the same patient’s body part), and the model is intended to detect the severity of a disease.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f1b48b60e-53e6-43cc-bc1d-93441ed46721_481x271-1.png)

In this case, randomly splitting the images into train and test sets will result in data leakage.

This is because images of the same patient will end up in both the training and test sets, allowing the model to “see” information from the same patient during training and testing.

Here’s a paper which committed this mistake (and later corrected it):

![Image](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f6498f95a-0569-47eb-9c21-32012227988e_1004x646-jpeg-1.jpg)

To avoid this, a patient must only belong to the test or train/val set, not both.

This is called group splitting:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f2d73b8ff-d3da-42da-a8ce-385cc03270e0_2758x960-png-1.jpg)

Creating forward-lag features is another way leaky variables get created unintentionally at times:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f72a6fb12-dae1-43d3-b43b-511b7de7cd9d_800x274-1.png)

* * *

That’s it.

From the above discussion, it is pretty clear that there is a whole world of variables beyond features, targets, categorical and numerical variables, etc.

Of course, there are a few more types of variables that I haven’t covered here, as I intend to cover them in another issue.

But till then, can you tell me which ones I have missed?

Thanks for reading!
