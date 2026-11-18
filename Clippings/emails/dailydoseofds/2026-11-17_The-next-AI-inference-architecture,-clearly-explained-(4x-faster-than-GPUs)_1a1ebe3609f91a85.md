---
title: " The next AI inference architecture, clearly explained (4x faster than GPUs) "
source_key: "dailydoseofds"
email_subject: "The next AI inference architecture, clearly explained (4x faster than GPUs)"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Tue, 17 Nov 2026 23:41:49 +0000"
email_id: "1a1ebe3609f91a85"
article_id: "1a1ebe3609f91a85:1"
published: "2026-11-17"
content_tier: "email_fallback"
tags: []
---

#  The next AI inference architecture, clearly explained (4x faster than GPUs) 

- **邮件来源**: dailydoseofds
- **原邮件主题**: The next AI inference architecture, clearly explained (4x faster than GPUs)
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Tue, 17 Nov 2026 23:41:49 +0000
- **邮件 ID**: 1a1ebe3609f91a85
- **文章 ID**: 1a1ebe3609f91a85:1
- **内容层级**: email_fallback

---

## [**The next AI inference architecture, clearly explained (4x faster than GPUs)**](<https://fandf.co/4ezjhEu>)

_Everything you need to understand why LLM decode waits on memory, and how a dataflow chip removes that wait. It covers the memory-bandwidth ceiling, kernel boundaries, the limits of kernel fusion, spatial mapping, memory tiers, disaggregated prefill and decode, and a hands-on speed test of GLM-5.3, a Mixture-of-Experts model on SambaNova Cloud._

A GPU runs an LLM as a long chain of small programs called kernels.

Even for a small Llama model, that chain has about a hundred kernels for every token the model generates.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/7DTkPY1T3x1p8pPhTYXKpy/email) With one request, the GPU spends much of each step waiting on HBM, not doing math.  
---  
  
Each kernel writes its result to HBM, the GPU's main memory, and the next kernel reads it back. With one request at a time, the chip spends much of each step waiting on memory instead of doing math.

AI agents suffer the most due to this. Anthropic reports that its agents use about 4x the tokens of a chat, and multi-agent systems use about 15x.

A dataflow chip, like SambaNova's RDU, is a processor designed to pass each result straight to the next step on the chip, which minimizes trips to main memory. On 16 of SambaNova's SN40L chips, this approach runs Llama 3.1 8B at about 1,100 tokens/s.

The visual below shows how this differs from a GPU:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/2NuMkRsUmPgDA885A51i74/email) A GPU runs decode as a chain of kernels that bounce through HBM, while a dataflow chip keeps the same operations in one on-chip pipeline.  
---  
  
So today, let's understand why a GPU leaves much of its memory bandwidth unused during decode, why kernel fusion only goes so far, and how [**SambaNova's RDU**](<https://fandf.co/4ezjhEu>) runs a whole decoder layer as one pipeline that keeps results in on-chip SRAM.

We'll end with a hands-on speed test of GLM-5.3, a Mixture-of-Experts model now running on SambaNova Cloud.

* * *

#### **Prefill vs. decode in agent workloads**

An agent works in a loop. It asks the model for the next action, runs a tool, adds the result to its context, and repeats.

Every model call has two phases.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/qDnw6JtcXtX3viSrGD5AaL/email) Prefill handles the prompt in parallel, and decode then writes the answer one token at a time.  
---  
  
  * Prefill reads the whole prompt in parallel and builds the KV cache, 
  * And decode then writes the answer one token at a time. 

A recent study traced this loop on benchmarks like SWE-bench Pro and Terminal-Bench. Model inference took 71% to 98% of the total runtime.

Each turn reuses almost all of the last turn's context, so prefix caching skips most of the prefill work.

* * *

#### **Memory-bandwidth ceiling for decode**

With one request, the model reads every weight once for each new token. That works out to about 1 FLOP of compute for every byte it reads.

An H100 SXM can do about 989 trillion BF16 FLOPs per second, but its HBM delivers only 3.35 TB/s. So decode sits about 300x below the point where compute power becomes the limit.

This gives one request a hard speed ceiling, as the formula below shows:

tokens/s <= memory bandwidth / bytes of weights



H100, GLM-5.3 in BF16, ~40B active:



3.35e12 / (40e9 * 2) = ~42 tokens/s

The same calculation gives 1,351 tokens/s for Llama-3.2-1B and 209 for an 8B model.

The chart below shows how far decode sits from the compute limit:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/fAn6Yt63dVGN43is3xEcdp/email) One-request decode sits at about 1 FLOP per byte, far below the H100 compute ridge.  
---  
  
* * *

#### **Kernel boundaries and issues with fusion**

Each GPU kernel handles one or a few operations, such as RMSNorm, attention or the MLP.

Stanford Hazy Research found that vLLM and SGLang use at most 50% of an H100's bandwidth on Llama-3.2-1B.

At each boundary, the next kernel waits for the last one to finish, then stalls while its weights load from HBM.

The visual below shows these gaps between kernels:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/6p7eG8hJYnKFkfgCn1cMHz/email) Each GPU kernel writes to HBM and the next reads it back, with a launch gap between them.  
---  
  
Kernel fusion, which merges several operations into one kernel, is the standard fix. Hazy's hand-built megakernel fused the whole 1B forward pass this way and reached 78% of bandwidth.

GPU fusion still stops at a few operations. Large intermediate results spill out of the small on-chip SRAM, and the programming model cannot run back-to-back operations as a pipeline.

* * *

#### **Dataflow execution and memory tiers on an RDU**

An RDU, or Reconfigurable Dataflow Unit, is SambaNova's AI chip.

Unlike a GPU, it doesn't run a model one kernel at a time. Instead, its compiler spreads the steps of a decoder layer across the chip, so every step runs in its own spot.

Here's how that differs from a GPU:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/tE8aYbFbJ6rNG3wCpyBmhk/email) A GPU runs RMSNorm, attention, and the MLP one after another, while an RDU gives each operation its own group of compute units.  
---  
  
  * A GPU runs RMSNorm, then attention, then the MLP, one after another. The RDU gives each of these operations its own group of compute units on the chip. 
  * On a GPU, each kernel writes its output to HBM and the next one reads it back. On the RDU, each result passes straight to the next group through on-chip SRAM, so it never leaves the chip. 
  * A GPU kernel stalls while its weights load from HBM. The RDU loads the next step's weights while the current step is still computing, so no step waits. 

Here's how this layout looks on the chip:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/2A9GdX1MEBGc44C48MYov/email) An RDU tile runs a whole decoder layer as one kernel, and activations stay in on-chip SRAM.  
---  
  
The RDU keeps data in three memory tiers. On-chip SRAM holds activations, 64 GB of HBM holds active weights and KV cache, and up to 512 GB of DDR holds other models.

That DDR sits on the chip itself, so the RDU can switch models without going through the host CPU's memory.

* * *

#### **Whole-decoder kernels and loop conversion**

SambaNova applied this to Llama 3.1 8B, which has 32 identical decoder layers. The RDU runs each whole layer as one kernel call, and a compiler pass called loop conversion folds the 32 calls into one loop.

On 16 SN40L chips, the baseline ran at 100 tokens/s. The single-kernel decoder reached 500, and loop conversion reached 1,100.

The visual below compares the GPU and RDU layouts:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/qAKVW5fTAebMGfcVExP8g6/email) On 16 SN40L chips, loop conversion took Llama 3.1 8B from a 100 tokens/s baseline to 1,100 tokens/s.  
---  
  
Per the SN40L paper, HBM bandwidth then goes only to weights and KV cache, and loading weights during compute uses over 85% of it.

* * *

#### **Multi-chip dataflow through the AGCU**

A model like GLM-5.3 does not fit on one chip, so its 753B parameters are split across many. Every token then has to move data from chip to chip, and that movement often costs more time than the math.

On a GPU cluster, each GPU writes its result to memory, sends it over the network to the next GPU, and the next GPU reads it back. Each hop adds a wait.

SambaNova's RDU handles this with the AGCU (Address Generation and Coalescing Unit). The AGCU streams data directly from one RDU to the next, so the dataflow pipeline from the previous section keeps running across chips instead of stopping at every boundary, as shown below.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/Tda38CjTVQQWf7xWhipMh/email) A GPU cluster stops at every chip hop, while the AGCU streams data directly from one RDU to the next.  
---  
  
This matters even more for Mixture-of-Experts models. GLM-5.3 activates only about 40B parameters per token, spread across experts on different chips, so tokens hop between chips all the time.

* * *

#### **Measuring decode speed on SambaNova Cloud**

SambaNova Cloud has an OpenAI-compatible API, so the OpenAI SDK works with a different base URL. The script below streams one request to GLM-5.3 and prints the server's own timings:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/fDA5JNS9a1N1zV1wivjKMf/email)   
---  
  
The screenshot below shows this request, plus a ten-step agent loop built on the same call:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/kWLgsaehv8BnuTZK8USEEm/email) The GLM-5.3 run decoded at 179 tokens/s, and a ten-step agent loop used 16.85 s of server time.  
---  
  
As the screenshot above shows, the run decoded at 179 tokens/s, and prefill finished in 0.211 s.

That is about 4x the ~42 tokens/s ceiling of one H100, since the deployment spreads GLM-5.3's experts across many chips. In the agent loop, decode took 83% of the 16.85 s of server time.

* * *

#### **Disaggregated prefill and decode**

Prefill and decode stress hardware differently, so disaggregated inference runs them on different chips.

In a live demo with an NVIDIA B200 for prefill and an SN40 RDU for decode, SambaNova reported 2x the speed of a B200-only setup, verified by Artificial Analysis.

The visual below shows the split:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/vDEh2uH3NnYhyjdTGqMfEh/email) Disaggregated inference runs prefill on a GPU and decode on an RDU, and SambaNova reported 2x the speed of a B200-only setup.  
---  
  
#### **Takeaways**

Decode with one request is limited by memory bandwidth, and GPU kernel boundaries waste part of it.

A dataflow chip lays the decoder out in space and keeps activations in SRAM, so HBM bandwidth goes to weights and KV cache.

The trade-off is flexibility, since the compiler maps a fixed graph ahead of time.

If your agent is slow, its prefill and decode split is the first thing to measure.

👉 Over to you: what share of your agent's model time goes to decode?

SambaNova's page on its dataflow architecture goes deeper [**here**](<https://fandf.co/4ezjhEu>).

If you will be at NeurIPS, you can find SambaNova at the booth in Sydney (December 6-12) and Atlanta (December 8-13), or [r**egister for SambaHouse AI Night in Sydney on December 9 here**](<https://sambanova.ai/events>).

_Thanks to SambaNova for working with us on this article!_
