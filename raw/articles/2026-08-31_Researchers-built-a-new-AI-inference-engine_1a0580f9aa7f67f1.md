---
title: " Researchers built a new AI inference engine "
source_key: "dailydoseofds"
email_subject: "WebMCP By Google, Clearly Explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Mon, 31 Aug 2026 13:43:32 +0000"
email_id: "1a0580f9aa7f67f1"
article_id: "1a0580f9aa7f67f1:1"
published: "2026-08-31"
tags: []
---

#  Researchers built a new AI inference engine 

- **邮件来源**: dailydoseofds
- **原邮件主题**: WebMCP By Google, Clearly Explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 31 Aug 2026 13:43:32 +0000
- **邮件 ID**: 1a0580f9aa7f67f1
- **文章 ID**: 1a0580f9aa7f67f1:1

---

## [**Researchers built a new AI inference engine**](<https://github.com/superlinked/sie>)

Researchers built a new AI inference engine that:

  * reduces self-hosting costs by ~4x
  * runs a full agentic pipeline on one GPU
  * is a drop-in for the OpenAI API

And it serves 20+ model architectures, not just LLMs.

Here’s the problem with engines like vLLM that it solves.

Most agent pipelines today run 4-5 small models under the hood:

![](https://substackcdn.com/image/fetch/$s_!glWz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faca0a3c9-88c8-4a07-8b50-3d1c361607bd_680x340.png)   
---  
  
  * an embedder for retrieval
  * a reranker for precision
  * an extractor for entities
  * and an LLM for generation

The standard way to serve them is one server per model.

vLLM serves the LLM, TEI serves the embedder, and everything else gets a custom FastAPI wrapper.

Each server reserves its own slice of GPU memory and holds it whether traffic arrives or not. GPUs are billed by the hour, so idle time costs the same as busy time.

![](https://substackcdn.com/image/fetch/$s_!yB74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faabc12da-c4f9-4ad6-a03f-2cae31668924_680x274.png)   
---  
  
This is why switching to small models rarely reduces the bill. The cost is never in the calls but rather in maintaining the servers.

The structural fix is serving every model from one process that loads and evicts models based on traffic.

Superlinked open-sourced a new inference engine that does exactly that.

[**SIE (Superlinked Inference Engine)** ](<https://github.com/superlinked/sie>) is an Apache 2.0 server that runs 85+ models behind one API.

![](https://substackcdn.com/image/fetch/$s_!hjYK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd71c0c84-15d4-48e3-8c90-78055720b16c_1350x1030.png)   
---  
  
Four calls cover the whole pipeline:

  * `encode()` returns vectors
  * `score()` returns relevance scores
  * `extract()` returns entity spans
  * and `generate()` runs small open LLMs.

Models load on first request and are evicted least-recently-used, so one GPU serves a rotating set of models instead of sitting siloed behind one.

It runs anywhere from a laptop to a Kubernetes cluster, and it plugs into Qdrant, Weaviate, Chroma, LanceDB, LangChain, and LlamaIndex.

You can find the repo here: [**https://github.com/superlinked/sie** ](<https://github.com/superlinked/sie>)

(don’t forget to star 🌟)
