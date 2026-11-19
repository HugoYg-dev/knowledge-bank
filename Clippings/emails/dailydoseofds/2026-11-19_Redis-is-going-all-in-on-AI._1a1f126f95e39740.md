---
title: " Redis is going all in on AI. "
source_key: "dailydoseofds"
email_subject: "GPU architecture, clearly explained"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Thu, 19 Nov 2026 00:13:45 +0000"
email_id: "1a1f126f95e39740"
article_id: "1a1f126f95e39740:1"
published: "2026-11-19"
content_tier: "email_fallback"
tags: []
---

#  Redis is going all in on AI. 

- **邮件来源**: dailydoseofds
- **原邮件主题**: GPU architecture, clearly explained
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 19 Nov 2026 00:13:45 +0000
- **邮件 ID**: 1a1f126f95e39740
- **文章 ID**: 1a1f126f95e39740:1
- **内容层级**: email_fallback

---

## [**Redis is going all in on AI.**](<https://fandf.co/4kjC0b6>)

They just built [**Redis Iris**](<https://fandf.co/4kjC0b6>), a real-time engine that delivers relevant and accurate context for production agents.

In production, support agents receive the same intent in many phrasings:

  * “What’s the status of my refund?” 
  * “Has my refund gone through yet?” 

A semantic cache matches these paraphrases and returns the stored response, which works well when the answer is static.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/oVuSUNaJ8y6cSNmyoBKdHL/email)  
---  
  
But, at times, context is not static over time (like refund status). The stored response might indicate “processing” even after the refund has gone through, so the cache returns a stale answer.

A plain agent avoids this by running the full reasoning loop on every request, which gives the right answer but spends tokens re-deriving the same steps each time.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/q7zw11cHwWvWCPmo9WN2FR/email)  
---  
  
Here’s what happens when a request comes in:

  * The Intent Router recognizes similar requests. 
  * It then pulls the Agent Playbook for that request. The Playbook doesn’t store an answer. It stores the steps to produce one, like “look up the order, check the refund status, reply using this template.” 
  * The agent follows those steps, so it skips re-planning, and the app fetches the current refund status before the reply goes out. 

In short, semantic cache reuses the answer while Iris reuses the steps, so the answer is always computed on live data.

This lets the workflow avoid any additional reasoning while still working on the live data.

You can try Redis Iris here: [**https://redis.io/iris**](<https://fandf.co/4kjC0b6>)

To test this, we built a small app to compare all three setups (plain agent, Semantic cache, and Iris-backed agent).

We asked about the refund while it was processing, then updated the status to refunded and asked again with a paraphrase.

The video below shows this in action:

[ ](<https://api.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/7JACXYBX1ewySZtrsadgfM/player>)



Question 1 (status: processing):

  * Plain agent: 2 LLM calls, 9.4s, correct 
  * Semantic cache: cache miss, so 2 LLM calls, 10.2s, correct 
  * Iris: 1 LLM call, 5.9s, correct 

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/nNKFeZW2PmLuf9Q6kRZ6ki/email)  
---  
  
Question 2 (status: refunded, paraphrased):

  * Plain agent: 2 LLM calls, 12.7s, and the reply didn’t confirm status 
  * Semantic cache: cache hit, 0.5s, but it returned the stale “processing” answer 
  * Iris: 1 LLM call, 5.6s, correct 

Iris skips the planning call because the procedure is already stored, so it ran about 2x faster than the plain agent and was the only setup that was right on both turns.

You can try Redis Iris here: [**https://redis.io/iris**](<https://fandf.co/4kjC0b6>)

_Thanks to the Redis team for partnering today!_
