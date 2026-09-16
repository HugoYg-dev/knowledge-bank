---
title: Quantile regression
source_key: dailydoseofds
email_subject: 11 LLM Evaluation Methods
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 24 Jul 2026 22:05:08 +0000
email_id: 19f962933027e3e6
article_id: 19f962933027e3e6:1
published: '2026-07-24'
tags:
- MachineLearning

---

# Quantile regression

- **原邮件主题**: 11 LLM Evaluation Methods
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 24 Jul 2026 22:05:08 +0000
- **ID**: 19f962933027e3e6

---

## [**Quantile regression**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/x0hph6he5d07qwh5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZ2VuZXJhbGl6ZWQtbGluZWFyLW1vZGVscy1nbG1zLXRoZS1zdXBlcmNoYXJnZWQtbGluZWFyLXJlZ3Jlc3Npb24v>)

Regression models typically generate a point estimate, which isn’t always useful.

Consider a model predicting salary based on job title, years of experience, and education level.

![](https://substackcdn.com/image/fetch/$s_!HWi4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d66895c-2fa5-48af-b99d-2cda8f3e72c6_1456x487.png)   
---  
  
A traditional regression model provides a scalar salary estimate, specifically, the mean value of the outcome at a particular input.

_More specifically, the prediction is a_ _**mean value**_ _related to the outcome at a particular input. If you read the article on_[ _**generalized linear models**_](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/x0hph6he5d07qwh5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZ2VuZXJhbGl6ZWQtbGluZWFyLW1vZGVscy1nbG1zLXRoZS1zdXBlcmNoYXJnZWQtbGluZWFyLXJlZ3Jlc3Npb24v>) _, we discussed it there._

But a single value of $80k doesn’t tell you much. What’s more useful is getting quantiles to assess best-case and worst-case scenarios:

![](https://substackcdn.com/image/fetch/$s_!pQG7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd5f85ae-6849-437e-905d-f79d1ab16512_1456x506.png)   
---  
  
  * 25th percentile → $65k (25% of employees in similar roles earn $65k or less)
  * 50th percentile → $80k (The median)
  * 75th percentile → $95k (25% of employees earn $95k or more)

This makes sense since there’s always a distribution along the target variable, and a point estimate doesn’t capture that.

![](https://substackcdn.com/image/fetch/$s_!tdV3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c0b6d9c-a209-4e15-b1b4-792508d73483_1456x506.png)   
---  
  
Quantile regression solves this.

* * *

#### What is Quantile Regression?

Quantile regression estimates quantiles of the response variable conditioned on the input. Unlike OLS, which estimates the mean, quantile regression provides estimates for various percentiles.

![](https://substackcdn.com/image/fetch/$s_!Q05D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06e0c6c2-6416-4cf2-ad16-b9e09a20e669_1456x835.png)   
---  
  
#### How does it work?

Consider this dummy dataset with a linear regression fit:

  * Points in green have positive error (true - predicted).
  * Points in red have negative error.

![](https://substackcdn.com/image/fetch/$s_!CpTD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc17bdc69-6589-4555-a953-b5dbc33e6e5d_1300x334.png)   
---  
  
Here’s the trick:

  * To generate the 75th percentile line, assign more weight to the green points. This pulls the prediction line upward.

![](https://substackcdn.com/image/fetch/$s_!qzXe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9d326d7-e492-4b50-a16d-86a76c9a1c19_1456x318.png)   
---  
  
  * To generate the 25th percentile line, assign more weight to the red points. This pulls the line downward.

![](https://substackcdn.com/image/fetch/$s_!z40g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c7daaee-4b19-4b52-bd03-d85bda3bc922_1456x284.png)   
---  
  
To put it another way, the standard error term in linear regression assigns equal loss to predictions equidistant on either side of the actual value.

![](https://substackcdn.com/image/fetch/$s_!xvwy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf342043-e6db-4abd-bbfb-1b763045f12d_1456x558.png)   
---  
  
However, we can parameterize this loss function with a weight “w” so the loss differs on either side:

![](https://substackcdn.com/image/fetch/$s_!2jak!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51b92cc4-b8bb-469b-af2d-58d8f13b3ca0_1456x404.png)   
---  
  
If w>0.5, we get the plot on the left, and if w<0.5, we get the plot on the right:

![](https://substackcdn.com/image/fetch/$s_!XHEh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F996a93c4-a963-431b-8ec6-df6f0abe100f_1456x561.png)   
---  
  
_This is called_ _**quantile loss**_ _(or pinball loss)._

We then train multiple regression models, one per quantile:

  * **75th percentile** → w = 0.75
  * **50th percentile** → w = 0.50
  * **25th percentile** → w = 0.25

During inference, pass the input through each model to get quantile-level predictions.

![](https://substackcdn.com/image/fetch/$s_!ithG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5f39202-dae5-45cd-b1b1-2f4516939eec_1456x894.png)   
---  
  
* * *

#### Implementation from scratch

Consider a dummy dataset with its OLS regression fit. We’ll train multiple regression models, one for every quantile value.

![](https://substackcdn.com/image/fetch/$s_!LeIb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f658ecc-c716-41e1-974e-bf508b8fef95_1456x1047.png)   
---  
  
The loss function:

![](https://substackcdn.com/image/fetch/$s_!SoTj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F407cec6f-5442-43c6-98d4-fca95006e272_1456x404.png)   
---  
  
Here’s a function that computes this based on weight parameter (w) and model weights (θ):

![](https://substackcdn.com/image/fetch/$s_!1p6E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27b3f9a5-7f11-482b-8b96-5c7f183350d3_1456x1014.png)   
---  
  
To obtain optimal weights, use the `minimize` method from Scipy:

![](https://substackcdn.com/image/fetch/$s_!unOk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f61cd48-f5ac-4d99-93ab-18d6e11f4506_1456x619.png)   
---  
  
`minimize()` returns the parameter values that minimize the objective function.

Done!

Running for 5 different values of w:

![](https://substackcdn.com/image/fetch/$s_!68e0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb10d8a6a-92df-4b83-bae5-94fd22b82150_1456x890.png)   
---  
  
As `w` increases, the line moves upward toward higher quantiles, and this gives us quantile estimates as desired.

* * *

Quantile regression works particularly well with tree-based models. LightGBM regression, for instance, natively supports quantile objective functions.

👉 Over to you: Can you train a neural network with quantile loss? What would the procedure look like?
