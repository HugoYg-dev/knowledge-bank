---
title: How to use kNNs for imbalanced datasets
source_key: dailydoseofds
email_subject: How to Use kNNs for Imbalanced Datasets
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 28 Nov 2025 20:46:01 +0000
email_id: 19acc373a89bc8c4
article_id: 19acc373a89bc8c4:1
published: '2025-11-28'
tags:
- MachineLearning

---

# How to use kNNs for imbalanced datasets

- **原邮件主题**: How to Use kNNs for Imbalanced Datasets
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 28 Nov 2025 20:46:01 +0000
- **ID**: 19acc373a89bc8c4

---

## [**How to use kNNs for imbalanced datasets**](<https://www.dailydoseofds.com/8-fatal-yet-non-obvious-pitfalls-and-cautionary-measures-in-data-science/>)  
  
kNN is highly sensitive to the parameter `k`.

To understand this, consider this dummy 2D dataset below (the red data point is a test instance we want to generate a prediction for using kNN and k=7):

![](https://substackcdn.com/image/fetch/$s_!RF1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b360269-f208-4d82-a539-625cd8deda17_1456x699.png)   
---  
  
Generating a prediction will involve:

![](https://substackcdn.com/image/fetch/$s_!Ego7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa60b3e8e-ece3-4bc1-a6c5-7c6f4791023a_1456x708.png)   
---  
  
  1. counting its `7` nearest neighbors
  2. assigning it to the class with the highest count among those 7 neighbors.

The problem with Step 2 is that it is entirely based on class contribution. So the class that maximally contributes to the `k` nearest neighbors is picked.

But this fails when you have imbalanced datasets.

For instance, with `k=7`, the red data point below can NEVER be assigned to the yellow class, no matter how close it is:

![](https://substackcdn.com/image/fetch/$s_!svLi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdb2357e-8717-421f-9b50-24dfa43a3b74_1456x708.png)   
---  
  
There are two ways to address this.

* * *

# **Solution #1: Used distance-weighed kNN**

Distance-weighted kNNs are a robust alternative to traditional kNNs, that consider distance to the nearest neighbor for classification.

For instance, below, the green data point gets classified as red with traditional kNN (k=7), despite being closer to the blue cluster:

![](https://substackcdn.com/image/fetch/$s_!KZlp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9924e4f5-7a87-488a-b255-c9b92bfe591d_1432x654.png)   
---  
  
But the same data point gets classified as blue with distance-weighed kNN:

![](https://substackcdn.com/image/fetch/$s_!89cv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99785e04-cdce-4ead-a333-d0423794db31_1432x654.png)   
---  
  
That said, it is not the default option in implementations like sklearn, so make sure to enable it:

![](https://substackcdn.com/image/fetch/$s_!yFCr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33ac222e-129e-423e-b7a7-c7f64947b722_989x498.png)   
---  
  
* * *

# **Solution #2: Dynamically update the hyperparameter k**

Recall the above dataset again:

![](https://substackcdn.com/image/fetch/$s_!svLi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdb2357e-8717-421f-9b50-24dfa43a3b74_1456x708.png)   
---  
  
Here, you may argue that one must refrain from setting the hyperparameter `k` to any value greater than the minimum number of samples across all classes. 

But there’s a problem with it.

Setting a super low value of `k` is usually not ideal in extremely imbalanced datasets:

![](https://substackcdn.com/image/fetch/$s_!8ULy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c2ed832-98fd-4d97-883a-094bb75719f1_1456x592.png)   
---  
  
Setting a globally low value of `k` (say, 1 or 2) leads to suboptimal performance since it does not holistically evaluate the nearest neighbor patterns compared to what a large value of `k` can do.

But we just discussed above that setting a large value of `k`, also leads to the domination problem.

Both problems can be solved by dynamically updating the hyperparameter `k` based on the situation.

More specifically, there are three steps in this approach.

For every test instance:

  1. Set a standard value of `k` as we usually would and find the `k` nearest neighbors.
  2. Next, for all classes that appear in the `k` nearest neighbors, find the total number of training instances they have.

![](https://substackcdn.com/image/fetch/$s_!wBwj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a0214c7-85de-480f-8d02-6e8cd1c1eec9_2840x700.png) Here, we found blue and yellow classes in the 7 nearest neighbors, with a total of 40 and 3 samples respectively.  
---  
  
  1. Update the value of k to:

![](https://substackcdn.com/image/fetch/$s_!PYN9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70e7336-f577-4644-913c-0ab093c6f94a_347x105.png)   
---  
  
Now perform majority voting only on the first `k’` neighbors only.

Here’s why this makes sense:

  * If a minority class appears in the top `k` nearest neighbor, the update rule will reduce the value of `k` so that the majority class does not dominate.
  * If a minority class DOES NOT appear in the top `k` nearest neighbor, it will likely not update the value of `k` (_because k would be the smallest value during the update process_) and do a holistic classification.

The only shortcoming is that you wouldn’t find this approach in any open-source implementations.

Some further reading:

  * [**We covered 8 fatal (yet non-obvious) pitfalls and cautionary measures in data science here**](<https://www.dailydoseofds.com/8-fatal-yet-non-obvious-pitfalls-and-cautionary-measures-in-data-science/>)**.**
  * [**We discussed 11 uncommon yet powerful techniques to supercharge your ML models here**](<https://www.dailydoseofds.com/11-powerful-techniques-to-supercharge-your-ml-models/>)**.**

👉 Over to you: What are some other ways to make kNNs more robust when a class has few samples?
