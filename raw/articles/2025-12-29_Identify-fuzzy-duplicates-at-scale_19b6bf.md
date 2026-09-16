---
title: Identify fuzzy duplicates at scale
source_key: dailydoseofds
email_subject: 6 Steps to Build an ML Model
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 29 Dec 2025 21:22:53 +0000
email_id: 19b6bfe2074ca987
article_id: 19b6bfe2074ca987:1
published: '2025-12-29'
tags:
- Skill/data-analysis
- Infra/storage

---

# Identify fuzzy duplicates at scale

- **原邮件主题**: 6 Steps to Build an ML Model
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 29 Dec 2025 21:22:53 +0000
- **ID**: 19b6bfe2074ca987

---

## [**Identify fuzzy duplicates at scale**](<https://www.dailydoseofds.com/bi-encoders-and-cross-encoders-for-sentence-pair-similarity-scoring-part-1/>)

Data duplication is a big problem that many organizations face.

Methods like `df.drop_duplicates()` in Pandas work well when you have exact duplicates.

![](https://substackcdn.com/image/fetch/$s_!QfzD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f6a7d0e-4386-48d4-9247-eab026fecc8d_649x398.png) Using Pandas to remove duplicate records  
---  
  
**But what if the data has fuzzy duplicates?**

Fuzzy duplicates are those records that are not exact copies of each other but appear to be the same:

![](https://substackcdn.com/image/fetch/$s_!E6Mq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffae0a6b7-9dfe-48ea-b15a-86ab1fc652b7_1010x308.png) The records have the same first name, a similar address, and almost the same phone number.  
---  
  
The Pandas method will be ineffective since it will only remove exact duplicates.

So what can we do here?

* * *

# A naive solution

Let’s imagine that your data has 1M records. One way could be to naively compare every pair of records:

![](https://substackcdn.com/image/fetch/$s_!9w5T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2b3ed0f-710c-4328-ab10-29a544266d6e_644x492.png) Compare every pair of records  
---  
  
We can formulate a distance metric for each field and generate a similarity score for each pair of records.

But this approach is infeasible at scale.

For instance, on a dataset with just a million records, comparing every pair of records will result in 10^12 comparisons (n^2).

![](https://substackcdn.com/image/fetch/$s_!YDba!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24cd453f-7733-469c-8d22-40b0f69db7cf_1863x847.png) Complexity of naive approach  
---  
  
Even if we assume a decent speed of 10,000 comparisons per second, this approach will take ~3 years to complete.

Can we do better?

* * *

# A special property of duplicates

If two records are duplicates, they will certainly possess some lexical (or textual) overlap.

For instance, consider the dataset below:

![](https://substackcdn.com/image/fetch/$s_!thcP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F477867f9-0cdd-4d0a-91cb-29fd452cce7e_792x287.png)   
---  
  
Here, comparing the name “Daniel” to “Philip” or “Shannon” to “Julia” makes no sense since there is no lexical overlap.

Thus, they are guaranteed to be distinct records.

Yet, the naive approach will still compare them.

We can utilize this property of duplicates to cleverly reduce the total comparisons.

* * *

# Bucketing duplicates

Segregating the data into smaller buckets by applying some rules can help.

For instance, consider the above dataset again. One rule could be to create buckets based on the first three letters of the first name.

![](https://substackcdn.com/image/fetch/$s_!F4Po!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cdc671d-efea-4898-a2c0-e62b1f80b97b_887x335.png) Group data based on rules  
---  
  
Thus, we will only compare two records if they are in the same bucket.

If the first three letters are different, the records will fall into different buckets. Thus, they won’t be compared at all.

Segregating the records will eliminate about 98-99% of unnecessary comparisons that would have happened otherwise.

Finally, we can use our naive comparison algorithm on each bucket.

![](https://substackcdn.com/image/fetch/$s_!gQKE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4779a838-5502-4bb9-aa73-de84fda569da_848x441.png) Group records based on rules  
---  
  
In fact, once the data has been bucketed, you can also build an LLM-driven approach.

The optimized approach can run in just a few hours instead of taking years.

This way, we can drastically reduce the run time and still achieve great deduplication accuracy.

Of course, we would have to analyze the data thoroughly to come up with the above data split rules.

But what is a wiser thing to do:

  * Using the naive approach, which takes three years to run, OR,
  * Spending some time analyzing the data, devising rules, and running the deduplication approach in a few hours?

* * *

That said, duplicate detection engines are also needed in NLP systems, which assess whether two contexts convey the same meaning.

This is especially observed in community-driven platforms (Stackoverflow, Medium, Quora, etc.). For instance, Quora shows you questions related to the question you are reading answers for.

Pairwise context similarity scoring is a fundamental building block in several NLP applications, not just duplicate detection—RAGs, for instance.

We recently released a 2-part series on this.

It goes through the entire background in a beginner-friendly way, the challenges with traditional approaches, optimal approaches, and implementations.

Read part 1 here: [**Bi-encoders and Cross-encoders for Sentence Pair Similarity Scoring – Part 1**](<https://www.dailydoseofds.com/bi-encoders-and-cross-encoders-for-sentence-pair-similarity-scoring-part-1/>).

Read part 2 here: [**AugSBERT: Bi-encoders + Cross-encoders for Sentence Pair Similarity Scoring – Part 2**](<https://www.dailydoseofds.com/augsbert-bi-encoders-cross-encoders-for-sentence-pair-similarity-scoring-part-2/>).

**👉** Over to you: Can you further optimize the fuzzy duplicate detection approach?
