---
title: Avoid Using PCA for Visualization Unless...
source_key: dailydoseofds
email_subject: Avoid Using PCA for Visualization Unless...
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Sat, 18 Oct 2025 20:59:57 +0000
email_id: 199f91f3eaa6509e
article_id: 199f91f3eaa6509e:1
published: '2025-10-18'
tags:
- Skill/data-analysis
content_tier: "web_canonical"
canonical_url: "https://www.dailydoseofds.com/p/avoid-using-pca-for-visualization-unless/"
---

# Avoid Using PCA for Visualization Unless...

- **原邮件主题**: Avoid Using PCA for Visualization Unless...
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 18 Oct 2025 20:59:57 +0000
- **ID**: 199f91f3eaa6509e
- **官网长文**: https://www.dailydoseofds.com/p/avoid-using-pca-for-visualization-unless/
- **内容层级**: web_canonical

---

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/08/banner-mail.png)

 

**TODAY'S ISSUE**

## TODAY’S DAILY DOSE OF DATA SCIENCE

### Avoid Using PCA for Visualization Unless...

[​**PCA** ​](<https://www.dailydoseofds.com/formulating-the-principal-component-analysis-algorithm-from-scratch/>), by its very nature, is a dimensionality reduction technique.

Yet, at times, it is used to visualize high-dimensional datasets by projecting the data into two dimensions.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-50.png)

Here's the problem with it.

After applying PCA, each new feature (PC1, PC2, ..., PC-N) captures a fraction of the original data variance:

PC1 may capture 40%.PC2 may capture 25%.And so on.

Thus, using PCA for visualization by projecting the data to 2-dimensions only makes sense if the first two principal components collectively capture most of the original data variance.

This is rarely true in practice.

But it is possible to verify if PCA's visualization is useful by creating a cumulative explained variance (CEV) plot.

It plots the cumulative variance explained by principal components.

In sklearn, the explained variance fraction is available in the explained_variance_ratio_ attribute:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-51.png)

Create a cumulative plot of explained variance and check whether the first two components explain the majority of variance.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-52.png)

If the plot looks the following, your PCA visualizations are misleading since the first two components only explain 55% of the variance:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-53.png)

But if the plot looks like the following, it is safe to use PCA:

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-54.png)

As a takeaway, use PCA for 2D visualization only when the above plot suggests so.

That said, use the CEV plot only for dimensionality reduction to determine how many dimensions to project the data to when using PCA.

For instance, in the following plot, projecting to 5 dimensions could be good (depending on how much information loss you can tolerate):

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/image-55.png)

For visualization, however, use techniques specifically designed for it, like t-SNE, UMAP, etc.

​We formulated and implemented (in NumPy) t-SNE from scratch here​.

​We discussed the mathematical details of PCA and derived it from scratch here​.

👉 Over to you: What are some other problems with using PCA for visualization?

[**We formulated and implemented (in NumPy) t-SNE from scratch here** ​](<https://www.dailydoseofds.com/formulating-and-implementing-the-t-sne-algorithm-from-scratch/>).

[​**We discussed the mathematical details of PCA and derived it from scratch here** ​](<https://www.dailydoseofds.com/formulating-the-principal-component-analysis-algorithm-from-scratch/>).

## TRULY REPRODUCIBLE ML

### [​** _Data Version Control_**](<https://www.dailydoseofds.com/you-cannot-build-large-data-projects-until-you-learn-data-version-control/>)

Versioning **GBs of datasets** is practically impossible with GitHub because it imposes an upper limit on the file size we can push to its remote repositories.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/tqGpPvCoEUzicpx6j4pFEd/email)

That is why Git is best suited for versioning codebase, which is primarily composed of lightweight files.

However, ML projects are not solely driven by code.

**Instead, they also involve large data files, and across experiments, these datasets can vastly vary.**

To ensure proper reproducibility and experiment traceability, it is also necessary to [​** _version datasets_** ​](<https://www.dailydoseofds.com/you-cannot-build-large-data-projects-until-you-learn-data-version-control/>).

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2023/10/image-237.png)

Data version control (DVC) solves this problem.

The core idea is to integrate another version controlling system with Git, specifically used for large files.

[​** _̱Here's everything you need to know_** ​](<https://www.dailydoseofds.com/you-cannot-build-large-data-projects-until-you-learn-data-version-control/>)[​** _(with implementation)_** ​](<https://www.dailydoseofds.com/you-cannot-build-large-data-projects-until-you-learn-data-version-control/>)[​** _about building 100% reproducible ML projects →​_**](<https://www.dailydoseofds.com/you-cannot-build-large-data-projects-until-you-learn-data-version-control/>)

## MODEL OPTIMIZATION

### [** _Model compression to optimize models for production_**](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>)

Model accuracy alone (or an equivalent performance metric) rarely determines which model will be deployed.

Much of the engineering effort goes into making the model production-friendly.

Because typically, the model that gets shipped is NEVER solely determined by performance — a misconception that many have.

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2023/09/image-134.png)

Instead, we also consider several operational and feasibility metrics, such as:

  * **Inference Latency** : Time taken by the model to return a prediction.
  * **Model size** : The memory occupied by the model.
  * **Ease of scalability** , etc.

For instance, consider the image below. It compares the accuracy and size of a large neural network I developed to its pruned (or reduced/compressed) version:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/ke2q6PEqtY6Jh4f1rGho36/email)

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/11/clipboard-image-1731013306.png)

Looking at these results, don’t you strongly prefer deploying the model that is 72% smaller, but is still (almost) as accurate as the large model?

Of course, this depends on the task but in most cases, it might not make any sense to deploy the large model when one of its largely pruned versions performs equally well.

We discussed and implemented 6 model compression techniques in the article [​** _here_** ​](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>), which ML teams regularly use to save 1000s of dollars in running ML models in production.

[​** _Learn how to compress models before deployment with implementation →_**](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>)
