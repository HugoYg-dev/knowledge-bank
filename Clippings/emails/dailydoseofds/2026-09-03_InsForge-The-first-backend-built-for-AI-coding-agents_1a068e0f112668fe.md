---
title: " InsForge: The first backend built for AI coding agents "
source_key: "dailydoseofds"
email_subject: "Attention Mechanisms in LLMs, clearly explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Thu, 03 Sep 2026 20:06:06 +0000"
email_id: "1a068e0f112668fe"
article_id: "1a068e0f112668fe:1"
published: "2026-09-03"
tags: []
---

#  InsForge: The first backend built for AI coding agents 

- **邮件来源**: dailydoseofds
- **原邮件主题**: Attention Mechanisms in LLMs, clearly explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 03 Sep 2026 20:06:06 +0000
- **邮件 ID**: 1a068e0f112668fe
- **文章 ID**: 1a068e0f112668fe:1

---

## [**InsForge: The first backend built for AI coding agents**](<https://github.com/InsForge/InsForge>)

Agents can build a beautiful frontend in minutes, set up API routes, and lay out the component architecture. But the moment it needs to enable auth or configure a database, it completely falls apart.

The reason is that every backend platform today (Firebase, Supabase, AWS) was designed for humans clicking through dashboards. When agents try to interact with these platforms through MCP servers, they get fragmented context like table names without schema details or auth endpoints without security configs. So agents end up guessing, hallucinating, and generating broken code.

[**InsForge** ](<https://github.com/InsForge/InsForge>) fixes this at the infrastructure level rather than the tooling level. It introduces a semantic layer where every backend primitive (auth, database, storage, AI features) is exposed as structured, machine-readable capabilities with metadata, constraints, and documentation baked in.

[**InsForge GitHub Repo**](<https://github.com/InsForge/InsForge>)  
---  
![](https://substackcdn.com/image/fetch/$s_!BF2k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ec3ea28-3650-44d1-992c-dbd18b407e8c_1080x1080.png)   
---  
  
Primitives are also aware of each other, so auth knows about database permissions and storage understands access policies.

Because agents get a complete, structured context instead of inferring what’s missing, InsForge delivers:

  * Roughly 2x more accuracy than Supabase MCP
  * 1.6x faster task completion
  * 30% better token efficiency

To test this out, we built a full ChatGPT clone with auth, database, storage, and AI integration, built entirely with Claude Code using InsForge as the backend. No manual configuration was needed, not because of any magic, but because the agent could reason about the entire backend as one coherent system.

InsForge works with any AI coding agent, including Cursor, Claude Code, Windsurf, and Codex. You can use all the primitives together or just pick what you need, like database only or auth only.

It’s fully open-source under Apache 2.0.

[**Find the GitHub repo here →** ](<https://github.com/InsForge/InsForge>) (don’t forget to star it ⭐️)
