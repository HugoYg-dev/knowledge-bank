---
title: Why ML models need calibration?
source_key: dailydoseofds
email_subject: 4 Parallel Processing Techniques in Python
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Wed, 04 Feb 2026 21:13:10 +0000
email_id: 19c2a80854fc31f8
article_id: 19c2a80854fc31f8:1
published: '2026-02-04'
tags:
- MachineLearning

---

# Why ML models need calibration?

- **原邮件主题**: 4 Parallel Processing Techniques in Python
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 04 Feb 2026 21:13:10 +0000
- **ID**: 19c2a80854fc31f8

---

## [** _Why ML models need calibration?_**](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>)

Modern neural networks being trained today are highly misleading.

They appear to be heavily overconfident in their predictions.

For instance, if a model predicts an event with a 70% probability, then ideally, out of 100 such predictions, approximately 70 should result in the event occurring.

However, many experiments have revealed that modern neural networks appear to be losing this ability, as depicted below:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/mPC4gXVgFbgsXKhBFnKYRR/email)   
---  
  
  * The average confidence of LeNet (an old model) closely matches its accuracy.
  * The average confidence of the ResNet (a relatively modern model) is substantially higher than its accuracy.

[ _**Calibration**_](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>) solves this.

A model is calibrated if the predicted probabilities align with the actual outcomes.

Handling this is important because the model will be used in decision-making and an overly confident can be fatal.

To exemplify, say a government hospital wants to conduct an expensive medical test on patients.

To ensure that the govt. funding is used optimally, a reliable probability estimate can help the doctors make this decision.

If the model isn't calibrated, it will produce overly confident predictions.

There has been a rising concern in the industry about ensuring that our machine learning models communicate their confidence effectively.

Thus, being able to detect miscalibration and fix is a super skill one can possess.

_****_[ _**Learn how to build well-calibrated models in this crash course →**_](<https://www.dailydoseofds.com/a-crash-course-of-model-calibration-classification-models/>)

P.S. Assuming you care about probabilities, which model would you prefer in the image below?  

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/rk7sgmxdPXmhgPukKzccqV/email)   
---
