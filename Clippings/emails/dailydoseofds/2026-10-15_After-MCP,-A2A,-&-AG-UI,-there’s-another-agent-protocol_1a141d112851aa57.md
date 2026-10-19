---
title: " After MCP, A2A, & AG-UI, there’s another agent protocol: "
source_key: "dailydoseofds"
email_subject: "A Full Walkthrough on Multimodal Jev"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Thu, 15 Oct 2026 23:06:22 +0000"
email_id: "1a141d112851aa57"
article_id: "1a141d112851aa57:1"
published: "2026-10-15"
content_tier: "email_fallback"
tags: []
---

#  After MCP, A2A, & AG-UI, there’s another agent protocol: 

- **邮件来源**: dailydoseofds
- **原邮件主题**: A Full Walkthrough on Multimodal Jev
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Thu, 15 Oct 2026 23:06:22 +0000
- **邮件 ID**: 1a141d112851aa57
- **文章 ID**: 1a141d112851aa57:1
- **内容层级**: email_fallback

---

## [**After MCP, A2A, & AG-UI, there’s another agent protocol:**](<https://github.com/HarnessRouter/harnessrouter>)

And this one is built for Agent harnesses:

UHP (Unified Harness Protocol) is a standardized interface for running agent tasks across any agent harness, regardless of which one you use.

[**HarnessRouter**](<https://github.com/HarnessRouter/harnessrouter>) is its open-source server implementation.

[**Here’s the GitHub repo →**](<https://github.com/HarnessRouter/harnessrouter>)

Here’s how it works:

![](https://substackcdn.com/image/fetch/$s_!1AUV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63fd5587-6de9-4c9c-b810-aa0e8fcbcc32_1200x1200.png)   
---  
  
  * Your product backend sends a task + harness_id to HarnessRouter.
  * HarnessRouter routes it to whichever configured harness should run it.
  * The harness streams progress and artifacts back through HarnessRouter.
  * HarnessRouter returns the output to your product.

Three core components handle this:

  * Gateway: Responses API, harness config, your model keys.
  * Runner: Isolated workspaces, one event stream, turn checkpoints.
  * Built-in tools: MCP servers, browser, database, GitHub, media.

This means your agent infrastructure becomes fully interchangeable.

  * Swap Codex for Claude Code without touching your product code.
  * Run the same task across different harnesses and compare outputs.
  * Add new harnesses as they emerge without any rewrites.

Here’s the repo: [**github.com/HarnessRouter/harnessrouter**](<https://github.com/HarnessRouter/harnessrouter>)

(don’t forget to star it ⭐)
