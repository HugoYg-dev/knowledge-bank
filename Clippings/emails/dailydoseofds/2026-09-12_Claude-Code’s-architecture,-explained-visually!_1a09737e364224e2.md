---
title: " Claude Code’s architecture, explained visually! "
source_key: "dailydoseofds"
email_subject: "4 Speculative Decoding Variants"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Sat, 12 Sep 2026 20:03:35 +0000"
email_id: "1a09737e364224e2"
article_id: "1a09737e364224e2:3"
published: "2026-09-12"
tags: []
---

#  Claude Code’s architecture, explained visually! 

- **邮件来源**: dailydoseofds
- **原邮件主题**: 4 Speculative Decoding Variants
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sat, 12 Sep 2026 20:03:35 +0000
- **邮件 ID**: 1a09737e364224e2
- **文章 ID**: 1a09737e364224e2:3

---

## [**Claude Code’s architecture, explained visually!**](<https://www.dailydoseofds.com/p/the-anatomy-of-an-agent-harness/>)

Claude Code is a lot more than a CLI that invokes the Claude models.

The actual system has six layers, and the model is just one node inside the loop. The diagram breaks down every component:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/oBBTQTH61rQDVTddUnbFVv/email)   
---  
  
𝗜𝗻𝗽𝘂𝘁 𝗟𝗮𝘆𝗲𝗿 handles session management, permission gating, and YAML-based trust tiers before anything reaches the model.

𝗞𝗻𝗼𝘄𝗹𝗲𝗱𝗴𝗲 𝗟𝗮𝘆𝗲𝗿 holds the skill registry, context compressor, task graph, and cross-session memory store. This is where harness intelligence lives outside the weights.

The context compressor is a 5-layer cascade that kicks in when the context window hits roughly 95% capacity. It doesn’t summarize your conversation the way ChatGPT does. Instead, it runs structured extraction on file paths, code snippets, and error histories while pruning redundant tool outputs. The goal is to keep the context usable, not just smaller.

𝗘𝘅𝗲𝗰𝘂𝘁𝗶𝗼𝗻 𝗟𝗮𝘆𝗲𝗿 runs tool dispatch through a typed registry with one handler per tool, like bash, read, write, grep, glob, and revert.

The streaming runtime handles parallel execution, and the prompt cache reuses stable prefixes at roughly 10% of the original cost.

𝗜𝗻𝘁𝗲𝗴𝗿𝗮𝘁𝗶𝗼𝗻 𝗟𝗮𝘆𝗲𝗿 connects the MCP runtime to external servers (filesystem, git, custom). Tools register inward, and memory writes outward to a markdown file (agent_memory.md) that persists across sessions.

𝗠𝘂𝗹𝘁𝗶-𝗔𝗴𝗲𝗻𝘁 𝗟𝗮𝘆𝗲𝗿 is the most underappreciated piece, and it works very differently from what most people assume.

Claude Code supports two levels of parallelism: subagents and agent teams ([covered here in detail](<https://www.dailydoseofds.com/p/claude-subagents-vs-agent-teams/>)).

![](https://substackcdn.com/image/fetch/$s_!Tr4p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce26004a-0a9c-4088-a5ed-ec7572b6aeaa_1200x480.png)   
---  
  
  * Subagents are lightweight workers that run inside your session. They get their own context window, do a focused task (search the codebase, explore a file tree), and return results to the parent. They can’t talk to each other, and they can’t spawn their own subagents. It’s a strict parent-child hierarchy.
  * Agent teams go further. One session acts as a team lead, and it spawns independent teammates, each running as a full Claude Code instance with its own context window. The team lead breaks a task into subtasks, assigns them, and monitors progress.

The coordination happens through two mechanisms → a shared task list (JSON files on disk) and a mailbox system for peer-to-peer messaging.

Each teammate gets git worktree isolation. It’s a separate working directory with its own branch, sharing the same repository history.

This means agents can write to overlapping parts of the codebase without file conflicts. When they finish, worktrees with no changes are cleaned up automatically. Worktrees with changes persist for human review before merging.

𝗢𝗯𝘀𝗲𝗿𝘃𝗮𝗯𝗶𝗹𝗶𝘁𝘆 𝗟𝗮𝘆𝗲𝗿 wraps everything. An event bus with lifecycle hooks logs all tool calls and messages, creating a complete audit trail of the agent’s actions and decisions.

Background executors run daemon threads non-blocking, so observability never stalls the main loop.

* * *

The master agent loop sits at the center of all six layers, and it’s deliberately simple. It assembles context, calls the model, receives a tool request, executes it, feeds the result back in, and repeats. Every iteration is one turn.

Within a turn, the model might request a tool call. That request flows through the permission system, gets executed, and the output feeds back into the loop as the next input.

The loop itself is single-threaded on purpose. All the intelligence lives in the layers around it, not in the loop logic. Anthropic calls it a “dumb loop” because the model reasons, and the harness mediates.

This is the architecture behind Claude Code.

[**We recently wrote this article, which is a deep dive on how Anthropic, OpenAI, LangChain, and others build this pattern from the ground up →**](<https://www.dailydoseofds.com/p/the-anatomy-of-an-agent-harness/>)

That’s a wrap!
