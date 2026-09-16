---
title: How to actually use train, validation, and test sets
source_key: dailydoseofds
email_subject: How to Actually Use Train, Validation, and Test Sets in ML
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 13 Mar 2026 22:04:43 +0000
email_id: 19ce93b00b8a14f0
article_id: 19ce93b00b8a14f0:1
published: '2026-03-13'
tags:
- MachineLearning

---

# How to actually use train, validation, and test sets

- **原邮件主题**: How to Actually Use Train, Validation, and Test Sets in ML
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 13 Mar 2026 22:04:43 +0000
- **ID**: 19ce93b00b8a14f0

---

## [**How to actually use train, validation, and test sets**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2m7wzripu4pxp99eu7h64xll/g3hnh5hm975p0khr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vOC1mYXRhbC15ZXQtbm9uLW9idmlvdXMtcGl0ZmFsbHMtYW5kLWNhdXRpb25hcnktbWVhc3VyZXMtaW4tZGF0YS1zY2llbmNlLw==>)

It is conventional to split the available data into train, test, and validation sets.

![](https://substackcdn.com/image/fetch/$s_!1dtb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b0d390e-9500-4b33-9b8c-28a6264588de_1108x631.png)   
---  
  
However, there are quite a few misconceptions about how they are meant to be used, especially the validation and test sets.

Today, let’s clear them up and see how to truly use train, validation, and test sets.

[**We covered 8 Cautionary measures in ML here →**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2m7wzripu4pxp99eu7h64xll/g3hnh5hm975p0khr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vOC1mYXRhbC15ZXQtbm9uLW9idmlvdXMtcGl0ZmFsbHMtYW5kLWNhdXRpb25hcnktbWVhc3VyZXMtaW4tZGF0YS1zY2llbmNlLw==>)

[**And 11 powerful techniques to supercharge ML models here →**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2m7wzripu4pxp99eu7h64xll/9qhzhnhdwkm9e2t9/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vMTEtcG93ZXJmdWwtdGVjaG5pcXVlcy10by1zdXBlcmNoYXJnZS15b3VyLW1sLW1vZGVscy8=>)

Let’s begin!

#### **The standard split**

As we all know, we begin by splitting the data into:

  * Train
  * Validation
  * Test

At this point, just assume that the test data does not even exist. Forget about it instantly.

![](https://substackcdn.com/image/fetch/$s_!lGcd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c3ccca4-7898-4230-98ca-d179cbab203d_1480x688.png)   
---  
  
Begin with the train set. This is your whole world now.

![](https://substackcdn.com/image/fetch/$s_!abH7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc0b6c54-6721-4b2c-b962-e28d81075176_1480x639.png)   
---  
  
  * You analyze it
  * You transform it
  * You use it to determine features
  * You fit a model on it

After modeling, you will measure the model’s performance on unseen data.

Bring in the validation set now.

Based on validation performance, improve the model.

Here’s how you iteratively build your model:

![](https://substackcdn.com/image/fetch/$s_!6plt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd867fc1-4a0c-4266-bef1-90d9d20c4345_1368x700.png)   
---  
  
  * Train using a train set
  * Evaluate it using the validation set
  * Improve the model
  * Evaluate again using the validation set
  * Improve the model again
  * and so on.

Until you are satisfied with the model’s performance.

#### **The validation overfitting problem**

Here’s something critical that many practitioners miss:

If you repeatedly tune your model based on validation performance over many iterations, you risk indirectly overfitting to the validation set.

![](https://substackcdn.com/image/fetch/$s_!GIt5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7e12644-7a78-4d70-8c5e-d341b894c4a1_1287x662.png)   
---  
  
This is because every decision you make based on validation performance leaks information from that set into your model selection process.

Think of it this way: If you try 1000 different model configurations and pick the one with the best validation score, you’ve essentially used the validation set as part of your training process.

#### **The solution: Cross-validation**

Instead of relying on a single train-validation split, use k-fold cross-validation.

Here’s how it works:

![](https://substackcdn.com/image/fetch/$s_!aNJZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc7da89f-453b-45cf-a2a1-7eff6431d0cc_1252x654.png)   
---  
  
  1. Split your data into k folds (commonly k=5 or k=10).
  2. For each fold, use (k-1) folds for training and use the remaining fold for validation.
  3. Average the performance across all folds.

This gives you a more robust estimate of model performance because:

  * Every data point gets used for both training and validation
  * You reduce the variance that comes from a single random split
  * You get a better sense of how your model generalizes

When to use cross-validation:

  * When you don’t have much data (highly recommended)
  * When you want robust performance estimates
  * When you’re comparing multiple models or hyperparameter configurations

Trade-off: Cross-validation is computationally more expensive since you train k models instead of one.

#### **For rigorous hyperparameter tuning: Nested Cross-Validation**

If you’re doing extensive hyperparameter tuning, consider nested cross-validation.

This involves two loops:

  * Outer loop: Evaluates the overall modeling approach
  * Inner loop: Tunes hyperparameters

This prevents the hyperparameter tuning process from biasing your performance estimates.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/5s33MPvEq4RY6pUWrYa4Xy/email)   
---  
  
Yes, it’s computationally intensive. But it’s the gold standard when you need unbiased performance estimates.

#### **The test set**

Now, if you are happy with the model’s performance on validation (or cross-validation), there’s one more step before final evaluation.

Retrain on all available training data.

Once you’ve selected your best model and hyperparameters via cross-validation, retrain it on the combined train + validation data. This gives your final model more data to learn from before the ultimate test.

![](https://substackcdn.com/image/fetch/$s_!FK8-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fac60ac-0392-4686-ba70-30ed3b5c188e_1252x617.png)   
---  
  
Now, evaluate it on test data.

✅ What you use a test set for:

  * Get a final and unbiased estimate of the model’s real-world performance

❌ What you DON’T use a test set for:

  * Model selection
  * Hyperparameter tuning
  * Feature engineering decisions
  * Any decision that influences the model

#### **The classroom analogy**

Let’s make this concrete with an analogy.

![](https://substackcdn.com/image/fetch/$s_!Q0F4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3b83084-7e2e-4a2d-bf17-6af49c2895bb_1024x529.png)   
---  
  
Your professor taught you in the classroom. All in-class lessons and examples are the train set.

The professor gave you take-home assignments, which acted like validation sets.

You got some wrong and some right. Based on this, you adjusted your understanding, i.e., improved the model.

Cross-validation is like having multiple different take-home assignments throughout the semester, giving you a better sense of your true understanding.

The final exam is your test set.

If you do well, great!

But if you fail, the professor cannot give you the exact same exam paper next time because your previous evaluation will influence any further evaluations on that specific test set.

#### **What happens if the model fails on test?**

If the model is underperforming on the test set, you have a few options:

##### **Option 1: Go back and improve (but be careful)**

You can iterate further, but understand that your test set has now been “exposed.” Any improvements you make with knowledge of test performance technically biases your evaluation.

##### **Option 2: Use a held-out test set from production data**

In practice, many teams keep a completely separate holdout that only gets evaluated at major milestones (like before deployment).

##### **Option 3: Rely on cross-validation estimates**

If your cross-validation estimates were solid and the test set tells a different story, investigate why. It could indicate:

  * Distribution shift between train/test
  * Data leakage somewhere in your pipeline
  * The test set being unrepresentative

#### **Important considerations often missed**

Here are some important considerations that practitioners often miss that are specific to certain data situations.

##### **1) Temporal/Time-Series data: Never use random splits**

If your data has a time component, random splits cause data leakage.

Why? You might train on future data and validate on past data, which is unrealistic.

![](https://substackcdn.com/image/fetch/$s_!FeRd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F881d826e-9bed-4388-b4fb-e8bead1e3d99_1024x526.png)   
---  
  
Solution: Use chronological splits.

  * Train on data from time T₀ to T₁
  * Validate on data from T₁ to T₂
  * Test on data from T₂ to T₃

For time series, use time-series cross-validation (also called walk-forward validation), where you progressively expand the training window.

##### **2) Stratification for imbalanced data**

If you have a class imbalance (e.g., 95% negative, 5% positive), random splits might give you validation/test sets with very different class distributions.

Solution: Use stratified splits that preserve the class distribution across train, validation, and test sets.

![](https://substackcdn.com/image/fetch/$s_!ZOlB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd529e17d-b0d1-450f-92d3-89971fb3bf28_2160x912.png)   
---  
  
##### **3) Data leakage during preprocessing**

This is one of the most common and subtle mistakes.

Wrong approach:

![](https://substackcdn.com/image/fetch/$s_!DgZh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b2ccc8d-d9ba-4cbe-8902-0c770ba765bc_2336x832.png)   
---  
  
Why it’s wrong: The scaler learned statistics (mean, std) from the test data, leaking information.

Correct approach:

![](https://substackcdn.com/image/fetch/$s_!zY2P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F840ce966-ef05-488d-b3a8-f73b13a25311_3000x928.png)   
---  
  
This applies to:

  * Scaling/normalization
  * Encoding categorical variables
  * Imputing missing values
  * Feature selection
  * Any transformation that learns from data

#### **4) Group-based splits**

If your data has natural groups (e.g., multiple samples from the same patient, multiple transactions from the same user), ensure all samples from one group stay together.

![](https://substackcdn.com/image/fetch/$s_!F32k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61487dcb-ffd9-4d2c-94e9-0ff43cdf021f_1022x507.png)   
---  
  
Why? If one patient’s data is in both the train and test, the model might just memorize patient-specific patterns rather than learning generalizable features.

Solution: Use GroupKFold or GroupShuffleSplit from scikit-learn.

#### **A note on fixed test sets (Benchmarks)**

In academic ML and standardized benchmarks (ImageNet, GLUE, etc.), the test set is fixed and used by everyone.

This is fine because:

  * The test set represents a standard evaluation criterion.
  * You’re not iteratively improving based on test performance.
  * The goal is comparability across methods.

The key principle remains: the test set should not influence your modeling decisions.

Best practices:

  1. Use cross-validation instead of a single validation split when possible
  2. Use nested cross-validation for rigorous hyperparameter tuning
  3. Never let test set performance influence modeling decisions
  4. Use appropriate splitting strategies (temporal, stratified, grouped) based on your data
  5. Fit all preprocessors only on the training data

And that is how you properly use train, validation, and test sets in machine learning.

Further reading:

  * [**We covered 8 Cautionary measures in ML here →**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2m7wzripu4pxp99eu7h64xll/g3hnh5hm975p0khr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vOC1mYXRhbC15ZXQtbm9uLW9idmlvdXMtcGl0ZmFsbHMtYW5kLWNhdXRpb25hcnktbWVhc3VyZXMtaW4tZGF0YS1zY2llbmNlLw==>)
  * [**And 11 powerful techniques to supercharge ML models here →**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2m7wzripu4pxp99eu7h64xll/9qhzhnhdwkm9e2t9/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vMTEtcG93ZXJmdWwtdGVjaG5pcXVlcy10by1zdXBlcmNoYXJnZS15b3VyLW1sLW1vZGVscy8=>)

👉 Over to you: What other data splitting mistakes have you encountered in practice? Drop your experiences by replying!
