---
title: " 5 embedding compression techniques "
source_key: "dailydoseofds"
email_subject: "5 Embedding Compression Techniques"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Fri, 04 Sep 2026 20:53:29 +0000"
email_id: "1a06e32ac6088201"
article_id: "1a06e32ac6088201:2"
published: "2026-09-04"
tags: []
---

#  5 embedding compression techniques 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 5 Embedding Compression Techniques
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 04 Sep 2026 20:53:29 +0000
- **邮件 ID**: 1a06e32ac6088201
- **文章 ID**: 1a06e32ac6088201:2

---

## [**5 embedding compression techniques**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>)

Ten million 1,536-dimensional embeddings will occupy:

  * 62 GB in float32
  * 15 GB in int8
  * 2 GB as packed bits

This only covers the raw vector payload, and an in-memory system also needs space for the ANN index, metadata, and allocator overhead.

Embedding compression works along two axes:

  * the number of dimensions stored
  * the number of bits used for each dimension

The five techniques in the visual reduce different parts of the payload.

![](https://substackcdn.com/image/fetch/$s_!3rqE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F779d21d5-1e83-49cf-863f-c6957b39c53a_1200x1141.png)   
---  
  
1) PCA applies a post-training transform:

It learns the directions with the most variance from a representative sample, then projects existing embeddings into a smaller space.

![](https://substackcdn.com/image/fetch/$s_!r9pK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d3481d-d73f-4304-8677-c5148e2de12d_1376x768.jpeg)   
---  
  
It works with any embedding model, although the projection must be fitted and applied consistently to indexed vectors and queries.

2) MRL alters the training objective:

The model is trained so that selected prefixes (say, the first `<n>` dimensions) of the embedding remain useful independently.

![](https://substackcdn.com/image/fetch/$s_!id-R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6af7f2c-6f32-43b8-b9b6-df2dd2a2fff2_1376x768.jpeg)   
---  
  
You can therefore truncate an MRL embedding at inference without training a separate model for every target dimension.

OpenAI reports that text-embedding-3-large at 256 dimensions still outperforms the 1,536-dimensional text-embedding-ada-002 on MTEB.

3-4) Scalar and binary quantization keep the dimension count fixed and reduce the representation used for each value.

Scalar quantization typically maps float32 values to int8, giving a 4x reduction in the raw vector payload.

![](https://substackcdn.com/image/fetch/$s_!feFC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5e0b54b-4b59-4eb6-a0a5-26d01a0d7a8a_1376x587.jpeg)   
---  
  
The scale and offset add a small amount of metadata.

Binary quantization keeps one bit per dimension, which gives a 32x reduction.

![](https://substackcdn.com/image/fetch/$s_!e_uw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40f89702-bb03-4b80-938d-ce2e2399f1f2_1376x552.jpeg)   
---  
  
Similarity search can then use XOR and a population count instead of floating-point distance calculations.

5) Product Quantization encodes subvectors as centroid IDs:

It splits a vector into subvectors and replaces each subvector with the ID of its nearest centroid.

Query distances are then approximated through centroid lookup tables.

![](https://substackcdn.com/image/fetch/$s_!sTOF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24c64f2d-607e-447b-b64d-a8ccba8ee318_1376x768.jpeg)   
---  
  
In all of these setups, the compressed representation does not need to produce the final ranking.

Usually, you retrieve extra candidates from the compressed index, then recompute similarity using higher-precision document embeddings.

This is especially useful with binary quantization. One bit can preserve enough coarse structure but loses magnitude information.

![](https://substackcdn.com/image/fetch/$s_!MDiu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee810874-a11f-4248-adfb-c95a1a893fdf_1376x768.jpeg)   
---  
  
Rescoring improves the ordering, but it cannot recover an item missed by the initial compressed-retrieval stage.

Also, these methods can work together. An MRL embedding can be truncated first and quantized afterward, reducing both dimension and precision.

All of these techniques reduce the memory and compute a retriever uses once the index holds millions of vectors.

But it is a small part of building a retriever that works in production, which is what the RAG Systems course goes through. Here is the full series in order.

  * [**Part 1 covers the foundations of a RAG system, including vector search, chunking, and embeddings →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>)
  * [**Part 2 shows how to evaluate a RAG system and which metrics tell you whether it actually works →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-2-with-implementations/>)
  * [**Part 3 works on making retrieval faster and lighter on memory →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-3-with-implementation/>)
  * [**Part 4 extends RAG to multimodal data like images and tables, not just text →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-4-with-implementation/>)
  * [**Part 5 explains CLIP embeddings and multimodal prompting that put text and images in one space →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-5-with-implementation/>)
  * [**Part 6 builds a full multimodal RAG system on real-world data →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-6-with-implementation/>)
  * [**Part 7 brings in Graph RAG to use the relationships between entities during retrieval →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-7-with-implementation/>)
  * [**Part 8 introduces late interaction with ColBERT for token-level matching between the query and the document →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-8-with-implementation/>)
  * [**Part 9 builds vision-driven retrieval with ColPali that searches over document images directly →**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-9-with-implementation/>)
  * [**Part 10 walks through the first set of 16 practical techniques for production RAG →**](<https://www.dailydoseofds.com/16-techniques-to-supercharge-and-build-real-world-rag-systems-part-1/>)
  * [**Part 11 continues with the remaining techniques from that set →**](<https://www.dailydoseofds.com/16-techniques-to-supercharge-and-build-real-world-rag-systems-part-2/>)
  * [**Part 12 explains why RAG latency is really a prefill problem, the model reading the chunks rather than finding them →**](<https://www.dailydoseofds.com/building-rag-systems-course-part-12-with-implementation/>)
  * [**Part 13 starts the preloading arc by loading a corpus into cache before any query arrives →**](<https://www.dailydoseofds.com/building-rag-systems-course-part-13-with-implementation/>)
  * [**Part 14 compresses that cache and covers why most published methods still need a query first →**](<https://www.dailydoseofds.com/building-rag-systems-course-part-14-with-implementation/>)
  * [**Part 15 closes the preloading arc with the training-based methods and what running them in production takes →**](<https://www.dailydoseofds.com/building-rag-systems-course-part-15-with-implementation/>)

