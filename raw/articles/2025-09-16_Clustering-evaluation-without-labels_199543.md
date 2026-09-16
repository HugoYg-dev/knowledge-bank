---
title: Clustering evaluation without labels
source_key: dailydoseofds
email_subject: Clustering Evaluation Without Labels
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 16 Sep 2025 20:26:12 +0000
email_id: 1995434d669b06de
article_id: 1995434d669b06de:1
published: '2025-09-16'
tags:
- MachineLearning

---

# Clustering evaluation without labels

- **原邮件主题**: Clustering Evaluation Without Labels
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 16 Sep 2025 20:26:12 +0000
- **ID**: 1995434d669b06de

---

## **Clustering evaluation without labels**  
  
Continuing the discussion on evaluation...

Evaluating clustering quality is usually difficult since we have no labels. Thus, we must rely on intrinsic measures to determine clustering quality.

Here are three metrics I commonly use:

# **1) Silhouette coefficient:**

Here's the core idea:

If the average distance to all data points in the same cluster is small...

...but that to another cluster is large...

...this indicates that the clusters are well separated and somewhat "reliable."

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/93rq54cRqVMrRNXA4nu75/email)  
---  
  
It is measured as follows:

For every data point:

  * `A` → average distance to all other points within its cluster.
  * `B` → average distance to all points in the nearest cluster.
  * score `= (B-A)/max(B, A)`

Next, compute the average of all scores to get the overall clustering score.

If B is much greater than A, then `score=1` and it indicates the clusters are well separated.

Measuring it across a range of centroids (`k`) can reveal which clustering results are most promising:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/3dWV7mD9v6CdxfrDXtpL9i/email)   
---  
  
# [**2) Calinski-Harabasz Index**](<https://click.kit-mail1.com/mvug5g3q6xt5hq3o9k4amhrp67qqqb3h5ed66/08hwh9h2ddlg98sl/aHR0cHM6Ly9zY2lraXQtbGVhcm4ub3JnL3N0YWJsZS9tb2R1bGVzL2NsdXN0ZXJpbmcuaHRtbCNjYWxpbnNraS1oYXJhYmFzei1pbmRleA==>)

The run-time of Silhouette score grows quadratically with total data points.

Calinski-Harabasz Index handles this, while being similar to Silhouette score.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/tyJZ49SXtVW9Mwsz8AKkws/email)   
---  
  
Here’s how it is measured:

  * `A` → sum of squared distance between centroids and the dataset's center.
  * `B` → sum of squared distance between all points and their specific centroid.
  * Metric is computed as `A/B` (with an additional scaling factor).

If A is much greater than B, then `score>>1` and it indicates the clusters are well separated.

Calinski-Harabasz Index makes the same intuitive sense as the Silhouette Coefficient while being much faster to compute.

# [**3) DBCV**](<https://click.kit-mail1.com/mvug5g3q6xt5hq3o9k4amhrp67qqqb3h5ed66/8ghqhohollrq3ehk/aHR0cHM6Ly9naXRodWIuY29tL2NocmlzdG9waGVyamVubmVzcy9EQkNW>)

Silhouette score and Calinski-Harabasz index are typically higher for globular (spherical in the case of 3D) clusters.

Thus, using them on density-based clustering can produce misleading results.

DBCV (density-based clustering validation) solves this, and it computes two values:

  * The density **within** a cluster.
  * The density overlap **between** clusters.

A high density within a cluster and a low density overlap between clusters indicate good clustering results. The effectiveness of DBCV is evident from the image below:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/cziG2qkaK6DDCqENkoXG9c/email)   
---  
  
As depicted above:

  * The clustering output of KMeans is worse, but its Silhouette score is still higher than that of Density-based clustering.
  * With DBCV, the score for the clustering output of KMeans is worse, and that of density-based clustering is higher.

That said, here, we covered centroid-based and density-based evaluation.

  * You can read about Distributed-based clustering and its evaluation here: [**Gaussian Mixture Models (GMMs)**](<https://click.kit-mail1.com/mvug5g3q6xt5hq3o9k4amhrp67qqqb3h5ed66/vqh3hrhoppwe4xug/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZ2F1c3NpYW4tbWl4dHVyZS1tb2RlbHMtZ21tLw==>).
  * Also, you can read about DBSCAN++ here: [**DBSCAN++: The Faster and Scalable Alternative to DBSCAN Clustering**](<https://click.kit-mail1.com/mvug5g3q6xt5hq3o9k4amhrp67qqqb3h5ed66/l2hehmhl33x64nc6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZGJzY2FuLXRoZS1mYXN0ZXItYW5kLXNjYWxhYmxlLWFsdGVybmF0aXZlLXRvLWRic2Nhbi1jbHVzdGVyaW5nLw==>).

👉 Over to you: What are some other ways to evaluate clustering performance in such situations?
