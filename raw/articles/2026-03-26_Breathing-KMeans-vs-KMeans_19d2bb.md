---
title: Breathing KMeans vs KMeans
source_key: dailydoseofds
email_subject: CPU vs GPU vs TPU vs NPU vs LPU
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Thu, 26 Mar 2026 20:01:11 +0000
email_id: 19d2bbc9492d99c6
article_id: 19d2bbc9492d99c6:1
published: '2026-03-26'
tags:
- MachineLearning

---

# Breathing KMeans vs KMeans

- **原邮件主题**: CPU vs GPU vs TPU vs NPU vs LPU
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 26 Mar 2026 20:01:11 +0000
- **ID**: 19d2bbc9492d99c6

---

## **Breathing KMeans vs KMeans**

Since KMeans’ performance heavily depends on the centroid initialization step, it is always advised to run the algorithm multiple times with different initializations.

![](https://substackcdn.com/image/fetch/$s_!Dfnl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7136ebe2-9d8f-47aa-a26b-fc33632c8aeb_1456x695.png)   
---  
  
But this repetition introduces an unnecessary run-time overhead.

The **Breathing KMeans** algorithm solves this issue while providing better clustering results than KMeans.

![](https://substackcdn.com/image/fetch/$s_!I9oY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F029b775a-2e7c-413f-b9f6-a1e03b588359_1456x1028.png)   
---  
  
There is also an open-source implementation of Breathing KMeans with a sklearn-like API.

To get started, install the `bkmeans` library and run the algorithm as follows:

![](https://substackcdn.com/image/fetch/$s_!P8Oh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f9d131f-0ad5-45d7-abb8-c662e30bca0b_1456x729.png)   
---  
  
Done!

If you are curious, we have covered how Breathing KMeans works in the next section.

On a side note, data conformity is another big issue with KMeans, which makes it highly inapplicable in many data situations.

These three detailed guides cover distribution-based and density-based clustering, which address KMeans’ limitations in specific data situations:

**-**[**Gaussian Mixture Models (GMMs) [derived and implemented from scratch using NumPy]**](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/l2hehmhl26lzx2h6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZ2F1c3NpYW4tbWl4dHVyZS1tb2RlbHMtZ21tLw==>).

**-**[**DBSCAN++: The Faster and Scalable Alternative to DBSCAN Clustering** **[with implementation]**](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/m2h7h5h35m374zum/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZGJzY2FuLXRoZS1mYXN0ZXItYW5kLXNjYWxhYmxlLWFsdGVybmF0aXZlLXRvLWRic2Nhbi1jbHVzdGVyaW5nLw==>).

**-**[**HDBSCAN: An Algorithmic Deep Dive [with implementation]**](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/dpheh0he68empgam/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vaGRic2Nhbi10aGUtc3VwZXJjaGFyZ2VkLXZlcnNpb24tb2YtZGJzY2FuLWFuLWFsZ29yaXRobWljLWRlZXAtZGl2ZS8=>).

#### **Step 1: Run Kmeans**

First, run the usual KMeans clustering only once, i.e., **without rerunning it with a different initialization.**

![](https://substackcdn.com/image/fetch/$s_!ywoI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6b5f988-be73-4339-afb8-34bb5da2585f_1456x553.png)   
---  
  
This gives us the location of “k” centroids, which may be inaccurate.

#### **Step 2: Breathe in step**

Add “`m`” new centroids to the “`k`” centroids obtained above (usually m=5).

Where to place them?

This is decided based on the error associated with the “`k`” existing centroids. A centroid’s error is the sum of the squared distance to its associated points.

![](https://substackcdn.com/image/fetch/$s_!EvrQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3643bce8-f04c-4076-8ccf-282a710fd109_1448x740.png)   
---  
  
Thus, we add “m” centroids near centroids with high error.

To understand this intuitively, consider these clustering results:

![](https://substackcdn.com/image/fetch/$s_!BK8p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9802b5a-64ca-48c8-a773-17a94c871d3c_1456x620.png)   
---  
  
  * The centroid at the top has a high error.
  * All other centroids have relatively low error.

Intuitively speaking, if a centroid has a very high error, multiple clusters may be associated with it.

Thus, we must split this cluster by adding new centroids near centroids with high error.

This gives us a total of “k+m” centroids.

Next, rerun KMeans with “k+m” centroids**only once**.

#### **Step 3: Breathe out step**

Next, we should remove “m” centroids from the “k+m” centroids obtained above.

**Which “**`m`**” centroids should we remove?**

This is determined using the “utility” of a centroid.

A centroid’s utility is proportional to its distance from all other centroids.

The greater the distance, the more isolated it will be; hence, the more the utility.

![](https://substackcdn.com/image/fetch/$s_!-BgN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46f80218-5d12-474d-9525-268449848361_1456x757.png)   
---  
  
In other words, if two centroids are close, they may lie in the same cluster.

Thus, we must remove one of them, as demonstrated below (in the top right cluster):

![](https://substackcdn.com/image/fetch/$s_!vGib!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46320b04-6fd1-47f3-b98c-3b87283661ee_1456x544.png)   
---  
  
This is repeated until all “m” low-utility centroids have been removed.

This gives back “k” centroids.

Finally, we run KMeans with these “k” centroids **only once**.

####  **Step 4:** Decrease `m` by `1`.

####  **Step 5:** Repeat Steps 2 to 4 until `m=0`.

Done!

**Why does Breathing Kmeans work?**

These repeated breathing cycles (breathe-in and breathe-out steps) **almost always** provide a faster and better solution than standard KMeans with repetitions.

In each cycle:

  * New centroids are added at “good” locations. This helps in splitting clusters occupied by a single centroid.
  * Low-utility centroids are removed. This helps eliminate centroids that are likely in the same cluster.

As a result, it is expected to converge to the optimal solution faster.

The effectiveness of Breathing KMeans over KMeans is evident from the image below:

![](https://substackcdn.com/image/fetch/$s_!I9oY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F029b775a-2e7c-413f-b9f6-a1e03b588359_1456x1028.png)   
---  
  
  * KMeans produced two misplaced centroids.
  * Breathing KMeans accurately clustered the data with a 50% run-time improvement.

Isn’t that a significant upgrade to KMeans?

That said, data conformity is another big issue with KMeans, which makes it highly inapplicable in many data situations.

These three guides cover distribution-based and density-based clustering, which address KMeans’ limitations in specific data situations:

  * [**Gaussian Mixture Models (GMMs)** ](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/l2hehmhl26lzx2h6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZ2F1c3NpYW4tbWl4dHVyZS1tb2RlbHMtZ21tLw==>)**[derived and implemented from scratch using NumPy].**
  * [**DBSCAN++: The Faster and Scalable Alternative to DBSCAN Clustering** ](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/m2h7h5h35m374zum/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZGJzY2FuLXRoZS1mYXN0ZXItYW5kLXNjYWxhYmxlLWFsdGVybmF0aXZlLXRvLWRic2Nhbi1jbHVzdGVyaW5nLw==>)**[with implementation].**
  * [**HDBSCAN: An Algorithmic Deep Dive** ](<https://fff97757.click.kit-mail3.com/8ku7d7v34kboh2dmoo2ckhkgxq4dnb3hoqxnn/dpheh0he68empgam/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vaGRic2Nhbi10aGUtc3VwZXJjaGFyZ2VkLXZlcnNpb24tb2YtZGJzY2FuLWFuLWFsZ29yaXRobWljLWRlZXAtZGl2ZS8=>)**[with implementation].**

**👉** Over to you: What are some other ways to improve KMeans’ clustering and its run-time?
