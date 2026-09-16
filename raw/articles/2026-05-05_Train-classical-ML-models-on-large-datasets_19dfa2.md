---
title: Train classical ML models on large datasets
source_key: dailydoseofds
email_subject: Train Classical ML Models on Large Datasets
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Tue, 05 May 2026 21:57:27 +0000
email_id: 19dfa25648e2f2cb
article_id: 19dfa25648e2f2cb:1
published: '2026-05-05'
tags:
- MachineLearning

---

# Train classical ML models on large datasets

- **原邮件主题**: Train Classical ML Models on Large Datasets
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 05 May 2026 21:57:27 +0000
- **ID**: 19dfa25648e2f2cb

---

## [**Train classical ML models on large datasets**](<https://fff97757.click.kit-mail3.com/e5unmnq5evf7hlg2xd9f8h855rmmqclhvzgnn/x0hph6he06pvodt5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vd2h5LWJhZ2dpbmctaXMtc28tcmlkaWN1bG91c2x5LWVmZmVjdGl2ZS1hdC12YXJpYW5jZS1yZWR1Y3Rpb24v>)

The list of sklearn implementations that support a batch API is quite small:

![](https://substackcdn.com/image/fetch/$s_!yCUA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7040e7e-d523-4936-bab4-c2cb984e3693_1210x801.png)   
---  
  
This is concerning since, in the enterprise space, the data is primarily tabular.

Classical ML algorithms, such as tree-based ensemble methods, are frequently used for modeling.

However, typical implementations of these models are not “big-data-friendly” because they require the entire dataset to be in memory.

There are two ways to approach this:

  * The first way is to use big-data frameworks like Spark MLlib to train them.[**We covered this in detail →** ](<https://fff97757.click.kit-mail3.com/e5unmnq5evf7hlg2xd9f8h855rmmqclhvzgnn/6qheh8hleg58zdco/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vZG9udC1zdG9wLWF0LXBhbmRhcy1hbmQtc2tsZWFybi1nZXQtc3RhcnRlZC13aXRoLXNwYXJrLWRhdGFmcmFtZXMtYW5kLWJpZy1kYXRhLW1sLXVzaW5nLXB5c3Bhcmsv>)
  * There’s one more way: Random Patches. Let’s learn below.

#### **Random Patches**

_Note: This approach will only work in an ensemble setting. So, you would have to train multiple models._

The idea is to sample random data patches (rows and columns) and train a tree model on each patch.

[![](https://substackcdn.com/image/fetch/$s_!tY2v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F366c02db-f5e4-4d23-97a7-0842b61b3fbb_2752x939.jpeg)](<https://fff97757.click.kit-mail3.com/e5unmnq5evf7hlg2xd9f8h855rmmqclhvzgnn/kkhmh6hnvq50r9sl/aHR0cHM6Ly9zdWJzdGFja2Nkbi5jb20vaW1hZ2UvZmV0Y2gvJHNfIXRZMnYhLGZfYXV0byxxX2F1dG86Z29vZCxmbF9wcm9ncmVzc2l2ZTpzdGVlcC9odHRwcyUzQSUyRiUyRnN1YnN0YWNrLXBvc3QtbWVkaWEuczMuYW1hem9uYXdzLmNvbSUyRnB1YmxpYyUyRmltYWdlcyUyRjM2NmMwMmRiLWY1ZTQtNGQyMy05N2E3LTA4NDJiNjFiM2ZiYl8yNzUyeDkzOS5qcGVn>)  
---  
  
Repeat this step multiple times by randomly generating different data patches to obtain the entire random forest model.

These are the results mentioned in the thesis (check pages 174 and 178) on 13 datasets:

![](https://substackcdn.com/image/fetch/$s_!7yQd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91621f82-b337-4b67-809e-628db6db2774_2268x676.jpeg) From left to right → Cifar10, mnist3v8, mnist4v9, mnist, isolet, arcene, breast2, madelon, marti, reged, second, this, and sido.  
---  
  
  * In most cases, the random patches approach performs better than the traditional random forest.
  * In other cases, there is a marginal difference in performance.

And this is how we can train a random forest model on large datasets that do not fit into memory.

#### **Why does it work?**

The idea is similar to what we discussed when we covered Bagging, which eventually allowed us to build our own variant of the Bagging algorithm: [**Why Bagging is so ridiculously effective at variance reduction?** ](<https://fff97757.click.kit-mail3.com/e5unmnq5evf7hlg2xd9f8h855rmmqclhvzgnn/x0hph6he06pvodt5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vd2h5LWJhZ2dpbmctaXMtc28tcmlkaWN1bG91c2x5LWVmZmVjdGl2ZS1hdC12YXJpYW5jZS1yZWR1Y3Rpb24v>)

In a gist, building trees that are as different as possible guarantees a greater reduction in variance.

In this case, the dataset overlap between two trees will be **less** than that in a typical random forest. This aids in the Bagging objective and leads to a more robust model.

To understand this mathematically, read this: [**** **Why Bagging is so ridiculously effective at variance reduction?**](<https://fff97757.click.kit-mail3.com/e5unmnq5evf7hlg2xd9f8h855rmmqclhvzgnn/x0hph6he06pvodt5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vd2h5LWJhZ2dpbmctaXMtc28tcmlkaWN1bG91c2x5LWVmZmVjdGl2ZS1hdC12YXJpYW5jZS1yZWR1Y3Rpb24v>)
