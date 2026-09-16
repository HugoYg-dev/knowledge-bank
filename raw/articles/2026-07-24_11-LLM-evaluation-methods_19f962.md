---
title: 11 LLM evaluation methods
source_key: dailydoseofds
email_subject: 11 LLM Evaluation Methods
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Fri, 24 Jul 2026 22:05:08 +0000
email_id: 19f962933027e3e6
article_id: 19f962933027e3e6:1
published: '2026-07-24'
tags:
- LLM/reasoning
- Infra/platform

---

# 11 LLM evaluation methods

- **原邮件主题**: 11 LLM Evaluation Methods
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Fri, 24 Jul 2026 22:05:08 +0000
- **ID**: 19f962933027e3e6

---

## [**11 LLM evaluation methods**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/reh8hohmgvz5gkb2h6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv>)

A model can answer a question correctly and still score close to zero on BLEU.

That happens whenever the model says the right thing in different words than the reference. BLEU compares n-gram overlap, so a clean paraphrase reads as a total miss.

This one failure is why LLM evaluation is fragmented into several methods, depicted below:

![](https://substackcdn.com/image/fetch/$s_!M5lI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85ad3122-1a70-4308-9e1d-53f7af1c7d7f_1500x1443.jpeg)   
---  
  
Each method encodes a different assumption about what a correct output looks like, and different metrics are useful in different use cases.

Let’s understand the 11 must-know LLM evaluation metrics below.

* * *

**1) BLEU**

Splits output and reference into n-grams and measures how much of the output is supported by the reference, with a brevity penalty so short outputs cannot win by omission.

![](https://substackcdn.com/image/fetch/$s_!_B7a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f0b92db-a176-419a-98d9-082d7c9c2c4b_747x239.png)   
---  
  
It works for translation and constrained generation where the reference wording is close to the only acceptable wording. Report corpus-level BLEU instead of averaging sentence scores, and supply multiple references when more than one phrasing is correct.

**2) ROUGE**

Flips the direction of BLUE and measures recall, meaning how much of the reference is covered by the output.

![](https://substackcdn.com/image/fetch/$s_!Xr9e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfca0cdb-b97b-419a-a090-d105dd10f31b_744x235.png)   
---  
  
It is the default for summarization and extraction, where missing content hurts more than extra content. ROUGE-L uses longest common subsequence and tolerates reordering better than ROUGE-2. Recall alone rewards verbosity, so it needs a precision-side metric next to it.

**3) BERTScore**

Embeds both texts, matches each output token to its most similar reference token, and reports precision, recall, and F1 over those similarities.

![](https://substackcdn.com/image/fetch/$s_!QUtT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71138504-6ef5-40b9-b497-fc2a04eac4a0_747x239.png)   
---  
  
It handles the paraphrase case that causes problems in BLEU and ROUGE. Absolute values lie within a narrow high band, so scores are only meaningful when compared across systems, not read as accuracy. Rescaling the baseline helps, and the embedding model has to match the domain and language.

**4) G-Eval**

It hands a task description and criteria to a judge model to generate chain-of-thought evaluation steps, then scores against those steps with the result weighted by token probabilities.

![](https://substackcdn.com/image/fetch/$s_!LA0p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F785c590d-561b-4e3f-b7f1-37b4fe93ba2e_744x235.png)   
---  
  
It fits subjective criteria with no reference answer, like tone, instruction following, or domain correctness. Criteria written as a concrete checklist score far more consistently than criteria written as adjectives.

Ideally, it is recommended to run the judge at a low [**temperature**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/08hwh9h23wr73vflh5/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcC93aGF0LWlzLXRlbXBlcmF0dXJlLWluLWxsbXMv>) and calibrate against a small human-labeled set before trusting it.

**5) LLM-as-Judge**

The pairwise form feeds two or more outputs to a judge with a rubric, the judge picks the better one:

![](https://substackcdn.com/image/fetch/$s_!opfe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18b17be9-aca9-4659-9237-336f5f960dc1_747x239.png)   
---  
  
It is the practical way to compare two models, two prompts, or two retrieval configs when absolute scores drift between runs.

Make sure to randomize which output appears first, because judges might favor a position. You also need to control for length, since judges reliably prefer longer answers regardless of quality.

**6) Human eval**

Annotators score outputs across defined dimensions, and the aggregate becomes the reference that every automated metric gets calibrated against.

![](https://substackcdn.com/image/fetch/$s_!B6Aj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ee282a4-db22-4bda-a205-f1638836d221_744x235.png)   
---  
  
It belongs in two places, building the calibration set that validates a judge, and the final gate before release.

You must define the rubric before annotation starts and measure inter-annotator agreement. Low agreement means the rubric is ambiguous, not that the annotators are wrong.

**7) LLM juries**

Runs several judges independently over the same output and averages their scores into one verdict.

![](https://substackcdn.com/image/fetch/$s_!BE8l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6996a813-9b4d-4c6f-b568-abc74d6d1195_747x239.png)   
---  
  
It exists because a single judge carries a stable bias, including a preference for outputs from its own model family.

Use different model families rather than the same model three times, since correlated judges average away noise but not bias. Several small models in a jury often beat one large judge at a lower cost.

**8) DAG**

Scores through a decision tree where each node asks one narrow question and the answer routes to the next node, with the final leaf carrying the score.

![](https://substackcdn.com/image/fetch/$s_!1S-0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9b3e70a-70c7-41da-8301-ffc61fc66173_745x234.png)   
---  
  
It fits rubrics with hard requirements and ordering, like format compliance, required sections, or a mandatory disclaimer.

Because branching is deterministic, the same output always gets the same score. Always put cheap deterministic checks near the root so failing outputs exit before any model call.

**9) Trajectory accuracy**

Captures the agent’s full sequence of thoughts, tool calls and observations, then scores that path against the expected one.

![](https://substackcdn.com/image/fetch/$s_!TLR0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc35e124a-3b01-4d25-80db-93a0bf77d534_744x235.png)   
---  
  
It matters because an agent can reach the right answer through the wrong path, burning tokens on redundant calls or touching a tool it should not have.

Score path and outcome separately, otherwise a lucky correct answer hides a broken execution path. This needs tracing in place first, since there is no trajectory to score without it.

**10) Multi-turn eval**

Treats the whole conversation as the unit and scores role adherence, knowledge retention across turns, and coherence.

![](https://substackcdn.com/image/fetch/$s_!4747!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ba2c243-29be-4f26-a9e9-57b8363c57b9_745x234.png)   
---  
  
Per-turn scoring misses the failures that only appear over time, like contradicting an earlier answer or dropping a constraint set five turns ago.

Run it on real conversation logs rather than synthetic two-turn exchanges, because rule retention failures show up at depth.

**11) Safety eval**

Runs bias, toxicity and PII classifiers in parallel over the output and flags violations instead of producing a quality score.

![](https://substackcdn.com/image/fetch/$s_!wFzU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0f81ce9-d3e8-4b5f-b268-980b512b6282_744x235.png)   
---  
  
It belongs as a gate, not as a term inside an average. A single PII leak matters regardless of how good the mean quality score looks, which is how folding safety into an aggregate ends up shipping violations.

* * *

To use them in practice, most of these already ship as built-in metrics in Comet Opik, an open-source LLM evaluation and observability platform, including BLEU, ROUGE, BERTScore, G-Eval, LLM juries, trajectory accuracy, conversation-level metrics, and moderation, all running over traced production data.

Here’s the repo → [**https://github.com/comet-ml/opik**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/8ghqhohompn5mdfkh9/aHR0cHM6Ly9naXRodWIuY29tL2NvbWV0LW1sL29waWs=>)

(don’t forget to star it ⭐️)

Also, to dive deeper into the full LLMOps lifecycle, we have covered every bit of it in the LLMOps course, starting from fundamentals to productions:

  * [**Read Part 1 on fundamentals of LLMOps here →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/reh8hohmgvz5gkb2h6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv>)
  * [**Read Part 2 on understanding the core building blocks of LLMs →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/l2hehmhl8v7k89i6h0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTI=>)
  * [**Read Part 3 on the key components of LLMs, focusing on the attention mechanism, architectures like transformers and mixture-of-experts, and the fundamentals of pretraining and fine-tuning →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/m2h7h5h3d0znd6smhq/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTM=>)
  * [**Read Part 4 on decoding strategies, generation parameters, best practices, and the broader lifecycle of LLM-based applications →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/e0hph7h78won8ra8h2/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTQ=>)
  * [**Read Part 5 on context + prompt engineering from a system perspective, in-context learning, types of prompts, and different prompting techniques →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/7qh7h8h9rp54rxfzh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTU=>)
  * [**Read Part 6 on prompt versioning, defensive prompting, and techniques like verbalized sampling, role prompting, and more →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/owhkhqhw2ld82ehvhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTY=>)
  * [**Read Part 7 on context engineering, covering context types, context construction principles, and retrieval-centric techniques for building high-signal inputs →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/z2hghnheqrxdqgcph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTc=>)
  * [**Read Part 8 on memory, dynamic, and temporal context in LLM systems, covering short and long-term memory, dynamic context injection, and common failure modes in agentic applications →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/p8heh9h4n5o7qkhqh3/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTg=>)
  * [**Read Part 9 on evaluation methods and approaches for LLM-based applications, primarily focusing on building a strong understanding of the fundamental concepts →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/x0hph6he5d07qra5hl/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTk=>)
  * [**Read Part 10 on evaluation benchmarks in LLM applications, with task-specific methodologies, and the core tooling for evaluation of LLM apps →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/dpheh0helwn7pobmh4/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEw>)
  * [**Read Part 11 on evaluation of multi-turn systems, tool use evaluations, tracing, and red teaming →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/7qh7h8h9rp54npuzh6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEx>)
  * [**Read Part 12 on LLM fine-tuning, parameter-efficient methods like LoRA/QLoRA, and alignment techniques like RLHF, DPO, and GRPO →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/owhkhqhw2ld8q7avhr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEyLw==>)
  * [**Read Part 13 on LLM inference optimization, KV caching, PagedAttention, FlashAttention, speculative decoding, and model parallelism →**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/z2hghnheqrxdldfph0/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEzLw==>)
  * [**Read Part 14 on the fundamentals of LLM serving, including API-based access, inference with vLLM, and practical decisions.**](<https://fff97757.click.kit-mail3.com/68ud0dr3k9i8h5927wzuohpzxd0kva9hnlpoo/p8heh9h4n5o7q9sqh3/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTE0>)

👉 Over to you: What else would you add to the master tree?
