---
title: Loss Function of 16 ML Algos
source_key: dailydoseofds
email_subject: RAG & Fine-tuning in LLMs
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 26 Dec 2025 21:00:07 +0000
email_id: 19b5c7637722a2ba
article_id: 19b5c7637722a2ba:1
published: '2025-12-26'
tags:
- MachineLearning
- DeepLearning

---

# Loss Function of 16 ML Algos

- **原邮件主题**: RAG & Fine-tuning in LLMs
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 26 Dec 2025 21:00:07 +0000
- **ID**: 19b5c7637722a2ba

---

## **Loss Function of 16 ML Algos**

We prepared this visual, which depicts the most commonly used loss functions by various ML algorithms.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/4RYUzDQgMkUzRte1dnTcXw/email)   
---  
  
Since loss functions are a vital component of ML algorithms, knowing which loss functions are (typically) best suited for specific ML algorithms is extremely crucial.

**1) Linear Regression:** Mean squared error (MSE). This can be used with and without regularization, depending on the situation.

**2) Logistic regression:** Cross-entropy loss or Log Loss, with and without regularization.

  * Why log loss? We covered its origin here: [**Why Do We Use log-loss to Train Logistic Regression?**](<https://www.dailydoseofds.com/why-do-we-use-log-loss-to-train-logistic-regression/>)
  * Also, do you know Logistic regression can be trained without specifying a learning rate? We covered it here: [**Why Sklearn’s Logistic Regression Has No Learning Rate Hyperparameter?**](<https://www.dailydoseofds.com/why-sklearns-logistic-regression-has-no-learning-rate-hyperparameter/>)

**3) Decision Tree and Random Forest:**

  * Classification: Gini impurity or information gain.
  * Regressor: Mean squared error (MSE).
  * Further reading on Random Forest: [**Why Bagging is So Ridiculously Effective at Variance Reduction?**](<https://www.dailydoseofds.com/why-bagging-is-so-ridiculously-effective-at-variance-reduction/>)

**4) Support Vector Machines (SVMs):** Hinge loss. It penalizes both wrong and right (but less confident) predictions. Best suited for creating max-margin classifiers, like in SVMs.

**5) k-Nearest Neighbors (kNN):** No loss function. kNN is a non-parametric lazy learning algorithm. It works by retrieving instances from the training data, and making predictions based on the k nearest neighbors to the test data instance.

**6) Naive Bayes:** No loss function. Can you answer why?

**7) Neural Networks:** They can use a variety of loss functions depending on the type of problem. The most common ones are:

  * Regression: Mean squared error (MSE).
  * Classification: Cross-Entropy Loss.
  * Here are [**15 ways to optimize neural network training (with implementation) →**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>)

**8) AdaBoost:** Exponential loss function. AdaBoost is an ensemble learning algorithm. It combines multiple weak classifiers to form a strong classifier. In each iteration of the algorithm, AdaBoost assigns weights to the misclassified instances from the previous iteration. Next, it trains a new weak classifier and minimizes the weighted exponential loss.

**9) Other Boosting Algorithms:**

  * Regression: Mean squared error (MSE).
  * Classification: Cross-Entropy Loss.

