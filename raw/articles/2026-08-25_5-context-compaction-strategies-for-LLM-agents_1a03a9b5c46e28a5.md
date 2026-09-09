---
title: "5 context compaction strategies for LLM agents"
source_key: "dailydoseofds"
email_subject: "Build a Multi-Agent GTM Intelligence System"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Tue, 25 Aug 2026 20:27:32 +0000"
email_id: "1a03a9b5c46e28a5"
article_id: "1a03a9b5c46e28a5:2"
published: "2026-08-25"
tags: ["AI-Agent/context-engineering", "LLM/inference"]
---

# 5 context compaction strategies for LLM agents

- **邮件来源**: dailydoseofds
- **原邮件主题**: Build a Multi-Agent GTM Intelligence System
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 25 Aug 2026 20:27:32 +0000
- **邮件 ID**: 1a03a9b5c46e28a5
- **文章 ID**: 1a03a9b5c46e28a5:2

---

## [**5 context compaction strategies for LLM agents**](<https://github.com/LMCache/LMCache>)

Compacting your agent's context can cut its tokens and still raise costs.

This sounds counterintuitive, but token count and billed amount are two different quantities in how prefix caching works.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/dznrwqpdwSgYXfHV3vzPEB/email)   
---  
  
A long agent session resends its entire history on every call, appending the model's reply and the tool output to the transcript each turn.

This stays affordable because the leading span of each request is byte-identical to the previous one.

Providers bill that span as a cache read, which on Anthropic is 10% of base input, so a context that grows only at the tail stays cheap no matter how large it gets.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/8vRNb3pWSro9EXqK5frhW7/email)  
---  
  
Compaction edits the front of the transcript rather than the tail. The harness replaces the original turns with a summary, so everything from the edit point onward stops matching what was cached.

Consider a session having 100K tokens of history.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/shJUftkxqGe1bSPunoqpr5/email)   
---  
  
  * Normally, the next call reads that history from cache at a tenth of base rate, which works out to 10K tokens at full price.
  * But compact it down to a 10K summary, and there is nothing left to match, so those 10K bill as a cache write at 1.25x base input, which comes to 12.5K. The context is ten times smaller, and the call costs more.

To be fair, that cost is recovered over the turns that follow. But harnesses trigger compaction on a token threshold, so a long session compacts repeatedly and each event resets it.

None of this makes compaction wrong. Context windows are finite, and there are five strategies used in practice.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/iLZwT5dhKKt1QMVwx8mcyq/email)   
---  
  
> Truncation drops the oldest tokens once the limit is close. It is the cheapest to implement and the only one that permanently loses early decisions.

> Rolling summarization merges each new summary into a persistent state instead of regenerating from scratch, and still moves the cache boundary every time.

> Prompt compression scores each token with a small model and drops the low-relevance ones. LLMLingua reports up to 20x compression at small accuracy loss, and LLMLingua-2 does the same scoring with a BERT-sized encoder.

> RAG-based retrieval moves the history into a vector DB and injects back only what matches the current query, so retrieval precision becomes the failure mode instead.

The first three delete text outright, and RAG moves it into a store the agent only sees again if retrieval fetches it.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/8W9H3QktCsdRoqCEJDzj5b/email)   
---  
  
> KV cache eviction runs at the serving layer and drops the entries least likely to be needed, either by attention score, as in H2O and SnapKV, or by position, as in StreamingLLM.

The full history still goes to the model, and what gets dropped is the KV tensors the GPU computed for those tokens. Since those tensors are derived from the tokens, eviction costs prefill work rather than information.

They can always be recomputed. KV blocks that no longer fit in GPU memory can move to CPU DRAM, local NVMe, or a remote store, then load back on the next request instead of being recomputed during prefill.

LMCache implements this as an open-source layer for vLLM, SGLang, and Dynamo. Through CacheBlend, it reuses cached blocks at any position in the prompt rather than only the leading span.

Repo: [**https://github.com/LMCache/LMCache**](<https://github.com/LMCache/LMCache>)

(don't forget to star it ⭐)
