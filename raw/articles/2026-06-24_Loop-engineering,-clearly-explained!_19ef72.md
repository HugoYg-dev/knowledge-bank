---
title: Loop engineering, clearly explained!
source_key: dailydoseofds
email_subject: Loop Engineering, Clearly Explained!
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Wed, 24 Jun 2026 00:59:02 +0000
email_id: 19ef7234678feae5
article_id: 19ef7234678feae5:1
published: '2026-06-24'
tags:
- AI-Agent/coding
- AI-Agent/context-engineering
- AI-Agent/multi-agent
content_tier: "web_canonical"
canonical_url: "https://www.dailydoseofds.com/p/loop-engineering-clearly-explained/"
---

# Loop engineering, clearly explained!

- **原邮件主题**: Loop Engineering, Clearly Explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Wed, 24 Jun 2026 00:59:02 +0000
- **ID**: 19ef7234678feae5
- **官网长文**: https://www.dailydoseofds.com/p/loop-engineering-clearly-explained/
- **内容层级**: web_canonical

---

Every agent, underneath whatever framework you’re using, runs the same loop.

```Python
while True:
    response = model(context)
    if response.has_tool_calls():
        context += run_tools(response.tool_calls)
    else:
        break
```

  * Send the context to the model
  * It responds with tool calls
  * Run those tools
  * Append the results to the context
  * And send it back.

It keeps going until the model replies without asking for a tool.

That loop is short, and it’s nearly identical across LangGraph, the OpenAI Agents SDK, and Claude Code, so nobody competes on the while statement.

This is exactly why the engineering effort moved somewhere else.

More specifically, the model and the loop are the parts you don’t write.

![](https://substackcdn.com/image/fetch/$s_!IXQ_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe73db735-ddb7-4ca2-a88c-8594ca858a52_1341x644.jpeg)

What you write is everything around it, like when the loop stops, what stays in the context, which tools the model can reach, and how you check the result.

So let’s go through the loop itself, then the four parts of it that are hard to get right.

#### Where the engineering actually moved

It moved outward, into the layers that wrap the model.

![](https://substackcdn.com/image/fetch/$s_!__Zs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86e114e0-5516-4951-b39f-c6c6131ab27b_2752x1536.jpeg)

  * Prompt engineering is the words you send.
  * Context engineering is everything the model sees on a turn, not just your instructions.
  * Harness engineering is the code around the model that runs tools, tracks state, and recovers from errors.
  * Loop engineering is the outer cycle that decides what the agent works on and when it’s done.

Each layer wraps the one before it, so your prompt is now one input to a much larger system.

Here’s how these systems break today.

* * *

#### 1) Ending a turn is not finishing the job

The loop stops on exactly one condition, when the model replies without a tool call. So it ends the moment the model decides it’s finished, which means the model is judging its own completion.

```Python
while True:
    response = model(context)
    if response.has_tool_calls():
        context += run_tools(response.tool_calls)
    else:
        break
```

That judgment is often wrong. A coding agent makes an edit, returns a confident summary with no further tool call, and the loop exits even though it never ran the tests, or ran them and they failed. The turn ended, but the task wasn’t done.

Since you can’t trust the model’s own stop signal, you add conditions it doesn’t control:

![](https://substackcdn.com/image/fetch/$s_!aAgw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dfbc748-ab50-4347-a37b-6397e810f731_1376x768.jpeg)

Max iterations, a hard cap so a stuck agent can’t run forever.

  * Budget and time limits, a ceiling on tokens, money, and wall-clock seconds.
  * No-progress detection, which catches the agent repeating the same call with the same arguments.
  * A real completion check, an automated condition that proves the job is done.

The completion check is super important, because it’s the only brake that replaces the model’s self-assessment with an objective signal.

“Done” should mean the tests pass, not the model reporting that it’s done. Claude Code’s `/goal` command works this way, running the loop until a verifiable condition holds and using a separate model to confirm it.

![](https://substackcdn.com/image/fetch/$s_!SaiS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe116ef60-a7e0-4e18-9870-33053eeb8ee7_2335x2208.png)

#### 2) Context rot and the doom loop

The longer a loop runs, the more its context fills with junk, like old tool outputs, abandoned dead ends, and stale reasoning. Model quality drops as that pile grows, which the field calls context rot.

The loop turns rot into a spiral, where a rotted context produces a worse decision, which adds more noise, which rots the context further.

![](https://substackcdn.com/image/fetch/$s_!EraS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03decd6c-f31e-484d-bd90-bdedb100e8d7_1376x768.jpeg)

The community calls this the doom loop, and the agent gets less useful the longer it runs. LangChain added middleware specifically to detect doom loops in their harness.

You solve this by treating context as a budget, not a bucket:

  * Compaction, summarizing the conversation once it gets long, and continuing from the summary.
  * Offloading, pushing large outputs to a file, and keeping only the slice you need.
  * Sub-agents, handing a messy subtask to a separate agent so that only its clean result returns.

The instinct is to keep everything in case it matters later. The skill is knowing what to throw away.

* * *

#### 3) Tool design changes inside a loop

Adding tools makes selection harder, not easier.

Give the agent a hundred overlapping tools and it loses track of which one to call, so a small set of focused, non-overlapping tools works better.

Anthropic’s rule of thumb is that if a human engineer can’t say for certain which tool fits, neither can the agent.

![](https://substackcdn.com/image/fetch/$s_!3yn8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c2152e3-6ffc-4a9f-9cf6-f5ec8af0c7da_2752x1317.jpeg)

Vercel found that cutting an agent’s available tools raised its success rate.

Two more properties matter specifically because this is a loop, not a single call:

  * Writes have to be safe to repeat, since the loop retries a failed step, and a retried “create customer” that makes a second customer leaves you with duplicate records and double billing.
  * Error messages have to tell the agent what to do next, not just what went wrong, because in a loop, that message becomes the input to the next turn, so a vague error wastes a turn and a precise one fixes the bug.

#### 4) Put something in the loop that can say no

The completion check from earlier is one case of a wider rule.

Whatever decides if the work is good can’t be the same model that produced it. A model asked to grade its own output will usually pass it, so a loop with no outside check is just an agent agreeing with itself.

![](https://substackcdn.com/image/fetch/$s_!trPx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F800ce59d-2bf5-453a-a3f4-73c2dfc34153_1376x768.jpeg)

So you separate the maker from the checker. One agent writes the code, and a separate signal grades it, either something hard like a failing test or type error, or a second model running with different instructions.

That check is what lets you actually leave the loop alone, because now something other than the author decides when it’s right.

#### What is user’s job now?

Prompting steers the agent move by move.

Loop engineering involves building the system that steers it, and then stepping back. The work becomes three artifacts:

  * The goal is written as a success criterion that the agent can check itself against.
  * The loop, with brakes, so it stops for the right reasons.
  * The verifier, so “done” is proven, not claimed.

Karpathy said something along these lines too.

“Don’t tell it what to do, give it success criteria and watch it go.”

His AutoResearch project runs exactly this, an agent that tweaks a training script, measures the result, keeps what works, and discards what doesn’t, with no human editing the code between rounds. He arranges it once and lets it run.

* * *

You don’t need an overnight autonomous agent on day one. Build up to it:

  1. Start with the basic loop and add a max-iteration cap, a timeout, and a cost ceiling immediately.
  2. Define “done” as an automated check before you start, not a vibe afterward.
  3. Protect the context, compacting long runs, offloading big outputs, and isolating messy subtasks.
  4. Audit your tools, keeping them few and focused, making writes safe to repeat, and rewriting errors so an agent can act on them.
  5. Put a critic in the loop, and only go fully hands-off once you trust the thing that says no.

#### The takeaway

Loop engineering isn’t a framework you install but rather a shift in where you spend effort.

The model is becoming a commodity, and the loop around it is where the engineering now lives.

![](https://substackcdn.com/image/fetch/$s_!f3sp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18e5ea0c-2a3b-4f0d-9705-7cf90edf3256_1200x1105.png)

The builders getting value this year stopped asking what to tell the agent and started asking what system would do the work without them.

👉 Over to you: what’s the first brake you’d add to a loop you already run, a completion check, a budget cap, or a separate verifier?

​[**To dive deeper into harness engineering, we covered it in detail here →**](<https://www.dailydoseofds.com/p/the-anatomy-of-an-agent-harness/>)

Thanks for reading!
