---
title: Categorization of clustering algorithms
source_key: dailydoseofds
email_subject: '[Hands-on] Build a 3D Weather Globe with Claude Code'
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 01 Jun 2026 20:49:47 +0000
email_id: 19e84f32570b4582
article_id: 19e84f32570b4582:1
published: '2026-06-01'
tags:
- Skill/data-analysis
content_tier: "web_canonical"
canonical_url: "https://www.dailydoseofds.com/p/categorization-of-clustering-algorithms/"
---

# Categorization of clustering algorithms

- **原邮件主题**: [Hands-on] Build a 3D Weather Globe with Claude Code
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 01 Jun 2026 20:49:47 +0000
- **ID**: 19e84f32570b4582
- **官网长文**: https://www.dailydoseofds.com/p/categorization-of-clustering-algorithms/
- **内容层级**: web_canonical

---

![](https://storage.ghost.io/c/3f/df/3fdf6ed2-17ac-4b12-a693-8078bd13e748/content/images/2024/08/banner-mail.png)

 

**TODAY'S ISSUE**

## TOGETHER WITH DYNAMIQ

### 🤖 [​**Develop Agentic AI/LLM apps 10x faster [open-source]** ​](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>)

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/gtEQvtG4z53nj9THagzVd9/email)

[​**Dynamiq** ​](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>) is a completely **open-source, low-code, and all-in-one** Gen AI framework for developing LLM applications with AI Agents and RAGs.

Here’s what stood out for me about [​**Dynamiq** ​](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>):

  * It seamlessly orchestrates multiple AI agents.
  * It facilitates RAG applications.
  * It easily manages complex LLM workflows.
  * It has a highly intuitive API.

All this makes it 10x easier to build production-ready AI applications.

If you're an AI Engineer, [​**Dynamiq** ​](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>) will save you hours of tedious orchestrations!

[Dynamiq GitHub](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>)

[​**Start building agentic AI/LLM apps today →** ​](<https://github.com/dynamiq-ai/dynamiq?ref=dailydoseofds.com>)

## TODAY’S DAILY DOSE OF DATA SCIENCE

### Categorization of clustering algorithms

There’s a whole world of clustering algorithms beyond KMeans, which a data scientist must be familiar with.

In the following visual, we have summarized 6 different types of clustering algorithms:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/6aQyZNuvAyroWi5NrMvqTR/email)

**1) Centroid-based:** Cluster data points based on proximity to centroids.

**2) Connectivity-based:** Cluster points based on proximity between clusters.

**3) Density-based:** Cluster points based on their density. It is more robust to clusters with varying densities and shapes than centroid-based clustering.

  * DBSCAN is a popular algorithm here, but it has high run-time.
  * [​**DBSCAN++** ​](<https://www.dailydoseofds.com/dbscan-the-faster-and-scalable-alternative-to-dbscan-clustering/>) solves this.
  * It is a faster and more scalable alternative to DBSCAN.
  * We covered both DBSCAN and DBSCAN++ in detail [​**here** ​](<https://www.dailydoseofds.com/dbscan-the-faster-and-scalable-alternative-to-dbscan-clustering/>).

**4) Graph-based:** Cluster points based on graph distance.

**5) Distribution-based:** Cluster points based on their likelihood of belonging to the same distribution.

  * [​**Gaussian Mixture Models** ​](<https://www.dailydoseofds.com/gaussian-mixture-models-gmm/>) in one example.
  * We discussed it in detail and implemented it from scratch (only NumPy) here: [​**Gaussian Mixture Models** ​](<https://www.dailydoseofds.com/gaussian-mixture-models-gmm/>).

**6) Compression-based:** Transform data to a lower dimensional space and then perform clustering.

👉 Over to you: What other clustering algorithms will you include here?

## CRASH COURSE (30 MINS)

### [**_Build robust decision-making systems with causal inference_** ​](<https://www.dailydoseofds.com/a-crash-course-on-causality-part-1/>)[​](<https://www.dailydoseofds.com/formulating-and-implementing-xgboost-from-scratch/>)

“Because” is possibly one of the most powerful words in business decision-making.

  * Our customer satisfaction improved **because** we introduced personalized recommendations.
  * The energy consumption dropped **because** of the new efficiency standards implemented.

Backing any observation/insights with causality gives so much ability to confidently use the word “because” in business/regular discussions.

Identifying these causal relationships is vital because these relationships typically require an additional inspection and statistical analysis that goes beyond the typical correlation analysis (which anyone can do).

[​**Learn how to develop causal inference-driven systems →** ​](<https://www.dailydoseofds.com/a-crash-course-on-causality-part-1/>)

It uncovers:

  * the details of causality
  * why it is difficult
  * what is counterfactual learning
  * four common techniques to determine causal impacts
  * learn some of the most widely used techniques in causal inference
  * and more about my personal experience using it in my projects

## MODEL OPTIMIZATION

### [Model compression to optimize models for production](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>)

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

Looking at these results, don’t you strongly prefer deploying the model that is 72% smaller, but is still (almost) as accurate as the large model?

Of course, this depends on the task but in most cases, it might not make any sense to deploy the large model when one of its largely pruned versions performs equally well.

We discussed and implemented 6 model compression techniques in the article [​** _here_** ​](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>), which ML teams regularly use to save 1000s of dollars in running ML models in production.

[​** _Learn how to compress models before deployment with implementation →_**](<https://www.dailydoseofds.com/model-compression-a-critical-step-towards-efficient-machine-learning/>)
