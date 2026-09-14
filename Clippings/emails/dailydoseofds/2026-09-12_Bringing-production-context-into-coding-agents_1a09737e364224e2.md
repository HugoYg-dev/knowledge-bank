---
title: " Bringing production context into coding agents "
source_key: "dailydoseofds"
email_subject: "4 Speculative Decoding Variants"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Sat, 12 Sep 2026 20:03:35 +0000"
email_id: "1a09737e364224e2"
article_id: "1a09737e364224e2:1"
published: "2026-09-12"
tags: []
---

#  Bringing production context into coding agents 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 4 Speculative Decoding Variants
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 12 Sep 2026 20:03:35 +0000
- **邮件 ID**: 1a09737e364224e2
- **文章 ID**: 1a09737e364224e2:1

---

## [**Bringing production context into coding agents**](<https://fandf.co/4zViirr>)

One limitation of coding agents does not get discussed enough.

They can inspect every file in your repository, but they cannot see how that code behaves after deployment. So when an endpoint slows down, or errors spike, the agent suggests fixes from static code while the useful evidence sits in production traces and logs.

Dynatrace has [**open-sourced a repository**](<https://fandf.co/4zViirr>) that brings this runtime context into coding agents.

![](https://substackcdn.com/image/fetch/$s_!ydzx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ed39111-f624-4c42-94af-d7b9d0b5029e_1203x747.png)   
---  
  
The MCP server provides access to live Dynatrace data. The included skills teach agents how to query and interpret that data, while reusable prompts define complete investigations.

For instance, its performance regression prompt compares P95 latency, error rate, and throughput before and after a deployment. It then finds the slowest trace, maps the bottleneck span back to the relevant workspace code, and recommends either a rollback or a targeted hotfix.

![](https://substackcdn.com/image/fetch/$s_!G4vF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb34fd0a3-58eb-46ac-bf66-bdd1b1256b1f_1376x446.jpeg)   
---  
  
The skills work with Claude Code, Cursor, GitHub Copilot, OpenCode, Gemini CLI, and other compatible agents.

[**Find the GitHub repo here →**](<https://fandf.co/4zViirr>)

(don’t forget to star 🌟)

_Thanks to Dynatrace for partnering today!_
