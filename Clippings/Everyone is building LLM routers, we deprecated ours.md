---
title: "Everyone is building LLM routers, we deprecated ours"
source: "https://manifest.build/blog/why-we-deprecated-our-llm-router/"
author:
  - "[[Bruno Perez]]"
published: 2026-07-31
created: 2026-09-20
description: "We don't believe in model routing anymore. For most use cases, sticking to a single battle-tested model is the best thing you can do."
tags:
  - "clippings"
---
**We don’t believe in model routing anymore.** For most use cases, sticking to a single battle-tested model is the best thing you can do.

Recently, there’s been huge hype around AI model routers that select the model that will respond to your request on the fly. There have been many launches in recent weeks with similar promises of reducing inference costs. We had our LLM router too, and decided to remove it.

Some context first: we launched the Manifest LLM router in March as a key feature in our [LLM gateway](https://manifest.build/), and we [deprecated it in June](https://manifest.build/blog/deprecating-rule-based-routing/), shutting it down for good on September 1st. Our router was classifying each request into one of four different tiers of complexity: simple, standard, complex and reasoning.

![LLM router diagram: a single agent request fanning out to Anthropic, DeepSeek, OpenAI and Mistral models](https://manifest.build/images/blog/what-is-an-llm-router.png)

Like most LLM routers, ours was made for cost reduction. Why call a powerful, and therefore expensive, model for a simple task? Routing to the most cost-effective model seems like a natural solution, right? Not that simple. After four months of usage across 7000 cloud users, we saw mixed results and a lot of GitHub issues and discussions about it. Let’s dive into the main problems.

## Complexity cannot be deduced from the prompt alone

==The prompt alone does not contain the whole task; it is just the trigger. A lot of the context that determines complexity is only discovered later through tool calls, web searches, and so on.==

Let’s take an example: *“evaluate the tests for the repo $GIT\_REPO and improve them”* can be a very simple task if you mention a personal website written in plain HTML5; or an incredibly complex task if you target the [Linux kernel repo](https://github.com/torvalds/linux).

## Cache is more effective than routing for reducing costs

**Cache reads are between 75% and 90% cheaper than uncached inputs.** System prompts and conversation history often represent a lot of tokens. Prefix cache works extremely well for those because they sit at the beginning of the prompt.

A cache-aware model router will take that into account by adding stickiness to the initially chosen model and keeps querying it. In other words, the router will do its job by, ironically, *not doing it*.

## LLM routers break behavior consistency

Some say that “engineers should not be concerned about choosing the best LLM for their task”. Well, **we strongly disagree**.

Just as a painter knows exactly what brush they need to use, and the craftsman carefully chooses their tools, engineers should understand trade-offs and subtleties of the different models. At Manifest, every engineer selects models and effort parameters based on their intent.

Jumping from a model to another during working sessions results in lower quality of the overall work, and detaches the people from mastering their tools.

## Unpredictability has a cost

No one likes unpredictability, especially software engineers.

==In automated agentic workflows or autonomous agents, **managing that extra layer of uncertainty can cost more than it saves**. Think of evals, system prompts, observability and so on. Everything suddenly becomes harder to maintain.==

Isolating different requests and setting up the right models, params and prompts for it seems naturally superior in most cases.

## Conclusion

There are probably many use cases where LLM routing can be useful, and the companies that launched those have probably good reasons.

However, based on our experience, we’ve concluded that in most of the use cases we saw, it was not worth it. **The amount saved is paid somewhere else**, and that cost is harder to estimate.