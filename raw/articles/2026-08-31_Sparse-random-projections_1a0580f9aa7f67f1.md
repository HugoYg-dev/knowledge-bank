---
title: " Sparse random projections "
source_key: "dailydoseofds"
email_subject: "WebMCP By Google, Clearly Explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Mon, 31 Aug 2026 13:43:32 +0000"
email_id: "1a0580f9aa7f67f1"
article_id: "1a0580f9aa7f67f1:3"
published: "2026-08-31"
tags: [MachineLearning, DeepLearning]
content_tier: "web_canonical"
canonical_url: "https://www.dailydoseofds.com/p/sparse-random-projections/"
---

#  Sparse random projections 

- **邮件来源**: dailydoseofds
- **原邮件主题**: WebMCP By Google, Clearly Explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 31 Aug 2026 13:43:32 +0000
- **邮件 ID**: 1a0580f9aa7f67f1
- **文章 ID**: 1a0580f9aa7f67f1:3
- **官网长文**: https://www.dailydoseofds.com/p/sparse-random-projections/
- **内容层级**: web_canonical

---

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/08/banner-mail.png)

 

**TODAY'S ISSUE**

## TODAY’S DAILY DOSE OF DATA SCIENCE

### Sparse Random Projections

This is the time complexity of PCA:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f448cca1a-21bd-4b29-99cd-85552a9ea8ef_2673x420-1.png)

The cubic relationship with the number of dimensions makes it impractical on high-dimensional datasets, say, 1000d, 2000d, and more.

I find it quite amusing about PCA.

Think about it: You want to reduce the dimension, but the technique itself isn’t feasible when you have lots of dimensions.

Anyway…

**Sparse random projection** is a pretty fine solution to handle this problem.

Let me walk you through the intuition before formally defining it.

* * *

Consider the following 2000-dimensional dataset:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fc5c3dcd3-51fe-41a3-b6ed-bd42b9b00aac_2480x1016-1.png)

Let’s find the distance between two random points here:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fd044f472-7791-40a2-9ef1-1eeba0f0a8ec_2632x920-1.png)

Now imagine multiplying the above high-dimensional matrix `X` with a random projection matrix M of shape (`m, d`), which results in the projected matrix:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f9d49b775-c097-440e-adbc-476c5e07bd26_2666x1082-1.png)

In this case, I projected X to 1000 dimensions from 2000 dimensions.

Now, if we find the distance between the same two points again, we get this:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fa6e189d0-7bc2-4b35-a9d0-f91a1177e21b_2544x896-1.png)

The two distance values are quite similar, aren’t they?

This hints that if we have a pretty high-dimensional dataset, we can transform it to a lower dimension while almost preserving the distance between any two points.

If you read the [**deep dive on the curse of dimensionality**](<https://www.dailydoseofds.com/a-mathematical-deep-dive-into-the-curse-of-dimensionality/>), we covered the mathematical details behind why distance remains almost preserved.

But let’s not stop there since we also need to check if the projected data is any useful.

Recall that we created a blobs dataset.

So let’s utilize KMeans on both the high-dimensional original data and the projected data, and measure the clustering quality using silhouette score.

  * Clustering `X` is implemented below:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2ffe96289b-3528-4caf-960c-ca333451bfdc_2728x896-1.png)

  * Clustering `X_projected` is implemented below (_for random projection, we make use of SparseRandomProjection from sklearn_):

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f48b7e67a-6c6d-443f-8873-c54e968b6092_3312x1472-1.png)

Look at the silhouette scores:

  * On `X`, we get 0.8267 (_the higher, the better_).
  * On X_projcected, we get 0.8233 (_the higher, the better_).

These two scores are highly similar, which indicates that both datasets produce a similar quality of clustering.

Formally speaking, random projections allow us to project high-dimensional datasets into **relatively** lower-dimensional spaces while almost preserving the distance between the data points.

> _This has a mathematical intuition attached to it as well, which we covered here:_[**_A mathematical deep dive on the curse of dimensionality_**](<https://www.dailydoseofds.com/a-mathematical-deep-dive-into-the-curse-of-dimensionality/>)** _._**

I mentioned “relatively” above since this won’t work if the two spaces significantly differ in their dimensionality.

I ran the above experiment on several dimensions, and the results are shown below:

```
Original:
Silhouette = 0.8267

Projected:
Components = 2000, Silhouette = 0.8244
Components = 1500, Silhouette = 0.8221
Components = 1000, Silhouette = 0.8233
Components = 750,  Silhouette = 0.8232
Components = 500,  Silhouette = 0.8158
Components = 300,  Silhouette = 0.8212
Components = 200,  Silhouette = 0.8207
Components = 100,  Silhouette = 0.8102
Components = 50,   Silhouette = 0.8041
Components = 20,   Silhouette = 0.7783
Components = 10,   Silhouette = 0.6491
Components = 5,    Silhouette = 0.6665
Components = 2,    Silhouette = 0.5108
```

From the above results, it is clear that as the dimension we project the data to decreases, the clustering quality drops, which makes intuitive sense as well.

Thus, the dimension you should project to becomes a hyperparameter you can tune based on your specific use case and dataset.

In my experience, random projections produce highly unstable results when the data you begin with is low-dimensional (<100 dimensions).

Thus, I only recommend it when the number of features is huge, say 700-800+, and PCA’s run-time is causing problems.

That said, random projection is also used in an LLM fine-tuning technique called VeRA:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2ff5502e59-57a6-484c-99d1-fc9cef7108b3_1456x640-1.png)

Recall that in LoRA, every layer has a different pair of low-rank matrices `A` and `B`, and both matrices are trained.

In VeRA, however, matrices `A` and `B` are frozen, **random,** and shared across all model layers. VeRA focuses on learning small, layer-specific scaling **vectors** , denoted as `b` and `d`, which are the only trainable parameters in this setup.

We covered 5 LLM fine-tuning techniques here:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/icon/logo-subsatck2-1-57.svg)
![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/thumbnail/5-llm-fine-tuning-techniques.gif)

Also, we formulated PCA from scratch (with all underlying mathematical details) here:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/icon/logo-subsatck2-1-58.svg)
![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/thumbnail/pca.png)

👉 Over to you: What are some ways to handle high-dimensional datasets when you want to use PCA?

## IN CASE YOU MISSED IT

### [​](<https://www.dailydoseofds.com/p/prompting-vs-rag-vs-fine-tuning/>)[​](<https://www.dailydoseofds.com/p/prompting-vs-rag-vs-fine-tuning/>)[**Traditional RAG vs. HyDE** ​](<https://www.dailydoseofds.com/p/traditional-rag-vs-hyde/>)

One critical problem with the traditional [​​​](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>)[​**RAG system** ​](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>)[​​​](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>) is that questions are not semantically similar to their answers.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f3916541d-ad57-4f26-9df6-80c23399c43b_2821x855-jpeg-16.jpg)

As a result, several irrelevant contexts get retrieved during the retrieval step due to a higher cosine similarity than the documents actually containing the answer.

HyDE solves this.

The following visual depicts how it differs from traditional RAG and HyDE.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2f382191dd-adeb-4328-b656-e556deac6ecb_992x1132-14.gif)

[​**We covered this in detail in a newsletter issue published last week →**](<https://www.dailydoseofds.com/p/traditional-rag-vs-hyde/>)[​](<https://www.dailydoseofds.com/p/prompting-vs-rag-vs-fine-tuning/>)

## IN CASE YOU MISSED IT

### [​](<https://www.dailydoseofds.com/p/prompting-vs-rag-vs-fine-tuning/>)[** _Build a Reasoning Model Like DeepSeek-R1_** ​](<https://www.dailydoseofds.com/p/build-a-reasoning-model-like-deepseek-r1/>)

If you have used DeepSeek-R1 (or any other reasoning model), you must have seen that they autonomously allocate thinking time before producing a response.

Last week, we shared how to embed reasoning capabilities into any LLM.

We trained our own reasoning model like DeepSeek-R1 (with code).

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2026/01/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2faa01f182-6db1-48d8-aa09-1770bbdf55f1_680x555-7.png)

To do this, we used:

  * UnslothAI for efficient fine-tuning.
  * Llama 3.1-8B as the LLM to add reasoning capabilities to.

[​**Find the implementation and detailed walkthrough newsletter here →**](<https://www.dailydoseofds.com/p/build-a-reasoning-model-like-deepseek-r1/>)
