---
title: Cyclical feature encoding
source_key: dailydoseofds
email_subject: Top AI Labs Share an Agent Memory Trick Most Miss
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Thu, 23 Apr 2026 23:20:49 +0000
email_id: 19dbca56ab454b95
article_id: 19dbca56ab454b95:1
published: '2026-04-23'
tags:
- MachineLearning

---

# Cyclical feature encoding

- **原邮件主题**: Top AI Labs Share an Agent Memory Trick Most Miss
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 23 Apr 2026 23:20:49 +0000
- **ID**: 19dbca56ab454b95

---

## [**Cyclical feature encoding**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2geol4urh4m798r9i7h64xll/48hvhehm8r5zmrux/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vMTEtcG93ZXJmdWwtdGVjaG5pcXVlcy10by1zdXBlcmNoYXJnZS15b3VyLW1sLW1vZGVscy8=>)

Features in typical ML datasets include:

  * Numerical features like age, income, transaction amt, etc.
  * Categorical features like t-shirt size, income groups, age groups, etc.

In addition to this, datasets also have cyclical features, i.e., features with a recurring pattern.

![](https://substackcdn.com/image/fetch/$s_!LPyq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff16aaeef-cc0f-41be-83ec-f77965162e38_3382x1385.png)   
---  
  
Unlike other features that progress continuously (or have no inherent order), cyclical features exhibit periodic behavior.

For instance, here are some common examples of cyclical features.

  * hour of a day (0 -> 1 -> .. -> 23 -> repeats from 0)
  * day of the week (M -> T -> .... -> S -> S -> repeats from M)
  * month of the year

If we don’t utilize appropriate feature engineering techniques for such features, we will lose some really critical information.

To understand better, consider the ‘hour of the day’ feature.

Realistically speaking, the ideal feature representation must satisfy two properties:

  * 
  * Moreover, the distance between “0” and “1” must be the same as that between “23” and “0”.

![](https://substackcdn.com/image/fetch/$s_!Lo8x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47d7bea5-44cc-4137-bed1-f27da92f6211_500x195.png)   
---  
  
However, the standard linear representation does not fulfill these properties because:

  * The value “23” is far from “0”
  * And the distance property isn’t satisfied either.

One of the most common techniques to encode such a feature is using trigonometric functions, specifically, `sine` and `cosine`.

They are helpful because both are periodic, bounded, and defined for all real values.

For instance, when representing the linear ‘hour of a day’ feature as a cyclical feature, the central angle (2π) will denote 24 hours.

![](https://substackcdn.com/image/fetch/$s_!Iza1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b2419f9-fc5a-48e1-9649-a9122ac56d7d_1067x395.png)   
---  
  
And the feature can be encoded as shown in the image below:

![](https://substackcdn.com/image/fetch/$s_!piJC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d6d3485-68c9-4656-afe7-ae709acae6b3_2248x856.png)   
---  
  
This way, the engineered feature satisfies both the properties we discussed earlier.

  * The value “23” is close to “0”
  * The distance between “0” and “1” is the same as that between “23” and “0”

![](https://substackcdn.com/image/fetch/$s_!lEZK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59d84359-59e7-4cc0-9d53-2ed768782c16_2901x644.png)   
---  
  
As depicted above, the distance between the cyclical feature representation of “23” and “0” is the same as the distance between “0” and “1”.

Had it been the day-of-the-week instead, the central angle (2π) must have represented 7 days.

![](https://substackcdn.com/image/fetch/$s_!5pPj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe776f1aa-3d7f-4170-b439-aad8c3fdad46_608x325.png)   
---  
  
* * *

The same idea can be extended to all sorts of cyclical features you may find in your datasets, like:

  * **Wind direction** : N, NE, E, SE, S, SW, W, NW, and then back to N.
  * **Phases of the moon** : new moon, first quarter, full moon, and last quarter, can be represented as categories with a cyclical order.
  * **Seasons** : spring, summer, fall, and winter, are categorical features with a cyclical pattern since they repeat annually.

This way, the model will find it easier to utilize the engineered features for modeling.

[**We covered 11 more techniques to supercharge ML models here →**](<https://fff97757.click.kit-mail3.com/38u030zrokckh2geol4urh4m798r9i7h64xll/48hvhehm8r5zmrux/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vMTEtcG93ZXJmdWwtdGVjaG5pcXVlcy10by1zdXBlcmNoYXJnZS15b3VyLW1sLW1vZGVscy8=>)

**👉** Over to you: What are some other ways to handle such features?
