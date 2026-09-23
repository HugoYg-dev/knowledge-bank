---
title: " Finally, an OpenRouter for agent harnesses "
source_key: "dailydoseofds"
email_subject: "Build your own Jev (100% local)"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Tue, 22 Sep 2026 19:10:31 +0000"
email_id: "1a0ca86e233289fe"
article_id: "1a0ca86e233289fe:1"
published: "2026-09-22"
content_tier: "email_fallback"
tags: []
---

#  Finally, an OpenRouter for agent harnesses 

- **邮件来源**: dailydoseofds
- **原邮件主题**: Build your own Jev (100% local)
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 22 Sep 2026 19:10:31 +0000
- **邮件 ID**: 1a0ca86e233289fe
- **文章 ID**: 1a0ca86e233289fe:1
- **内容层级**: email_fallback

---

## [**Finally, an OpenRouter for agent harnesses**](<http://github.com/HarnessRouter/harnessrouter>)

Devs just [**open-sourced**](<http://github.com/HarnessRouter/harnessrouter>) a plug-and-play infrastructure layer that lets you run any harness under a single interface, like:

  * Codex
  * Hermes
  * Claude code
  * DeepSeek Harness
  * System One, powered by Jev
  * And 9 more agent harnesses

![](https://substackcdn.com/image/fetch/$s_!kvoS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8258f69-ebdb-415c-b370-bcb48aa9b3c1_650x587.png)   
---  
  
This means you can bring Jev into the same product that already uses Codex, Claude Code, or another supported harness, without writing another implementation for sessions, streaming, files, cancellation, and failure handling.

Here’s the repo: [**github.com/HarnessRouter/harnessrouter**](<http://github.com/HarnessRouter/harnessrouter>)

(don’t forget to star it ⭐ )

The harnesses run locally, and the Unified Harness Protocol (UHP) defines the common task interface with an OpenAI Responses-compatible API.
