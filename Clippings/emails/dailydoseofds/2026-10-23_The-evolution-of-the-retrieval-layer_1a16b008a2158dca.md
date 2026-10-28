---
title: " The evolution of the retrieval layer "
source_key: "dailydoseofds"
email_subject: "6 KV Cache Quantization Approaches"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Fri, 23 Oct 2026 23:02:39 +0000"
email_id: "1a16b008a2158dca"
article_id: "1a16b008a2158dca:3"
published: "2026-10-23"
content_tier: "email_fallback"
tags: []
---

#  The evolution of the retrieval layer 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 6 KV Cache Quantization Approaches
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 23 Oct 2026 23:02:39 +0000
- **邮件 ID**: 1a16b008a2158dca
- **文章 ID**: 1a16b008a2158dca:3
- **内容层级**: email_fallback

---

## [**The evolution of the retrieval layer**](<https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/>)

![](https://substackcdn.com/image/fetch/$s_!G0O7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb910477-7646-4e90-b793-be43f2f34445_960x628.gif)   
---  
  
Google and Anthropic agree on one thing about RAG that retrieval is no longer a pipeline you build once.

Instead, it is a tool that something else calls.

  * Anthropic’s MCP exposes retrieval as a tool an agent can call.
  * Google now ships retrieval the same way, with its RAG Engine sitting under the Gemini agent platform alongside MCP servers.

That shift sounds small, but it changes the entire architecture underneath.

Today, let’s break down why classical RAG isn’t ideal in production, what a standing retrieval layer looks like, and how agents consume it.

* * *

#### Classical/Naive RAG

Naive RAG runs as a one-time pipeline inside a single app. A knowledge base gets chunked, embedded, and written to a vector DB.

At query time, the user’s query hits that vector DB for a similarity search, and the retrieved chunks go to the LLM.

![](https://substackcdn.com/image/fetch/$s_!B7Gj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F095e3b9e-1735-4db9-bbde-70460cf208cf_942x393.gif)   
---  
  
This works when the answer lives in one corpus that rarely changes. It breaks on two fronts that show up immediately at scale.

The first is staleness. The embeddings reflect the source at the moment of indexing. When a doc changes in Notion or a row updates in Postgres, the vectors still point at the old content until someone reruns the pipeline.

The second is duplication. The retrieval logic is welded to one application. A second app, or an agent, that needs the same data has to rebuild the same connectors, chunking, and embedding from scratch.

* * *

#### Retrieval as a standing layer

The fix is to stop treating retrieval as a step inside the app and start treating it as a standing layer underneath it. A retrieval layer separates ingestion from query, and runs ingestion continuously instead of once.

On the ingest side, connectors pull from many sources, handle auth and extraction, chunk into entities, embed, and write to a vector store with a metadata store alongside it for source links and versions.

![](https://substackcdn.com/image/fetch/$s_!39tF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41044f5e-5029-42fc-943a-06e11d3dce9e_1080x1080.gif)   
---  
  
A sync process watches for changes and updates only what changed, using content hashing so unchanged data is not re-embedded.

On the query side, a request gets expanded, run through hybrid search that combines neural and keyword retrieval, then reranked before results come back with their source attribution.

The key property is that this layer is owned by no single app. It is exposed over an API, so a RAG chatbot and an autonomous agent can both query the same index.

* * *

#### How agents alter this scenario

An agent does not run retrieval once at the start.

It reasons, decides it needs context, calls search, reads the result, and decides whether to search again with a refined query. Retrieval becomes a tool inside a loop, not a fixed first step.

And the tool the agent calls is the retrieval layer.

![](https://substackcdn.com/image/fetch/$s_!G0O7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb910477-7646-4e90-b793-be43f2f34445_960x628.gif)   
---  
  
The agent’s search function and the RAG app’s retrieval are the same query path into the same synced store.

They were never separate systems. Instead, one was just drawn inside the app, and the other was pulled out and shared.

👉 Over to you: Is moving retrieval out of the app and into a shared layer the right call for your stack?
