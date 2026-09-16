---
title: Platt Scaling for model calibration
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

# Platt Scaling for model calibration

- **原邮件主题**: 7 Categorical Data Encoding Techniques
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 02 Dec 2025 20:34:54 +0000
- **ID**: 19ae0c67c504face

---

## [**Platt Scaling for model calibration**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>)

Platt scaling is likely one of the simplest techniques if you want to calibrate binary classification models.

The below visual summarizes how it works:

![](https://substackcdn.com/image/fetch/$s_!RUSy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ca2110-d4af-4327-a2c5-a224efe77323_1174x1126.gif) “Validation set” can also be called “calibration set”  
---  
  
Let’s understand what calibration is and how Platt scaling works.

_We talked about model calibration in detail in a two-part deep dive below:_

[**A Crash Course on Model Calibration – Part 1**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>) _**.**_

[**A Crash Course on Model Calibration – Part 2**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-part-2/>) _**.**_

* * *

# **The problem**

Say a government hospital wants to conduct a medical test on patients. Since the test is expensive, doctors want to ensure that the govt. funding is used optimally.

A reliable estimate from a model reflecting the chances of a patient having the disease can be helpful.

For instance, if the model predicts a 75% probability across some patients, then ideally, out of 100 patients, ~75 should actually have that disease.

![](https://substackcdn.com/image/fetch/$s_!Psir!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5993c7cc-82d7-46d2-9ebe-75332f1ae4c5_2828x1623.png)   
---  
  
This means the model is well calibrated, i.e., the confidence and accuracy resonate with each other.

However, many experiments have revealed that modern ML models are typically not well-calibrated.

For instance, consider the following plot, which compares a LeNet (a relatively older model) with a ResNet (a relatively newer model) on the CIFAR-100 dataset.

![](https://substackcdn.com/image/fetch/$s_!I0xD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ecbe22d-3d72-4b06-b41b-da55dfb6fc2e_1739x974.png)   
---  
  
  * LeNet produced:
    * Accuracy = ~0.55
    * Average confidence = ~0.54
  * ResNet produced:
    * Accuracy = ~0.7
    * Average confidence = ~0.9

This shows that despite being more accurate, the ResNet model is overconfident in its predictions. While the model thinks it’s 90% confident in its predictions, in reality, it only turns out to be 70% accurate.

This must be fixed if you are reliant on probabilities for decision-making.

Calibration solves this.

And Platt scaling is a common technique.

![](https://substackcdn.com/image/fetch/$s_!RUSy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ca2110-d4af-4327-a2c5-a224efe77323_1174x1126.gif)   
---  
  
The primary goal is to find a logistic function that maps the raw scores (or logits) from a model to probabilities between 0 and 1.

_Note: It is not always necessary to use logits. One may use the predicted probabilities as well if that leads to stable results._

Here’s a step-by-step breakdown of how it works:

  * Train a model (say, a neural network) on the training dataset. This will produce a model that will likely be uncalibrated.

![](https://substackcdn.com/image/fetch/$s_!iS5V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fcecbaa-03a1-491b-8d35-03eea22f5e80_2980x900.png)   
---  
  
  * Pass the validation data through the above model and obtain logits (output before converting to probability using sigmoid):

![](https://substackcdn.com/image/fetch/$s_!4BtG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5d2bb77-4cad-4b9f-a9be-1f2e7caedd4d_2976x688.png)   
---  
  
  * Next, train a logistic regression model that predicts the actual outcome using the above logits. Done!

![](https://substackcdn.com/image/fetch/$s_!G2CH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf15ff09-aacb-440e-8382-bc2093670a2f_2976x716.png)   
---  
  
  * Now, to generate a calibrated prediction, obtain the logit for a new instance using the first (uncalibrated) model. Pass the logit through the logistic regression model trained in step 3 to obtain a calibrated probability:

![](https://substackcdn.com/image/fetch/$s_!hGyM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ef653dc-8058-4cee-a22b-fd6a62cc69c1_2980x580.png)   
---  
  
Here’s a plot depicting its efficacy with SVMs. It shows the relationship between predicted and empirical probabilities for the original and calibrated models.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/eb9PH3wpYAMy46nGKfySN8/email)   
---  
  
The ideal calibration line (a 45-degree line) indicates perfect calibration, where predicted probabilities match empirical probabilities exactly. From the above plot, it is clear that:

  * The SVM model (blue line) produces highly miscalibrated probabilities.
  * With Platt scaling, however, we get much better calibration (not entirely perfect though).

That said, one common issue with Platt scaling is that it can be sensitive to the amount of data available for calibration. More specifically, when the calibration set is quite small, Platt scaling may not produce reliable probability estimates.

If you want to go through the implementations and learn several other techniques for model calibration that you can utilize (for both binary and multi-class), we covered them in detail in a two-part deep dive below:

  * [**A Crash Course on Model Calibration – Part 1**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>)
  * [**A Crash Course on Model Calibration – Part 2**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-part-2/>)

👉 Over to you: What is your go-to technique for calibrating binary classification models?

Thanks for reading!
