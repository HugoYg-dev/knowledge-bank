---
title: How LLM inference works internally
source_key: dailydoseofds
email_subject: Markov Decision Processes and Value Functions in RL
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Sun, 03 May 2026 17:38:08 +0000
email_id: 19deeeb458239986
article_id: 19deeeb458239986:1
published: '2026-05-03'
tags:
- LLM/inference
- Infra/serving

---

# How LLM inference works internally

- **原邮件主题**: Markov Decision Processes and Value Functions in RL
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Sun, 03 May 2026 17:38:08 +0000
- **ID**: 19deeeb458239986

---

## [**How LLM inference works internally**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/qvh8h7hdpw0lpxil/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv>)

Every generate() call to an LLM runs two distinct computational phases on the same GPU:

  * prefill (processing the prompt) is compute-bound
  * while decode (generating tokens one at a time) is memory-bound.

Most inference optimizations target one phase or the other, and diagnosing which phase is the bottleneck is the first step in making a deployment faster.

Today, let's walk through the full pipeline, from tokenized input to streamed output, and look at where the time goes in each phase.

[**To master the full LLMOps cycle with code, start here →**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/qvh8h7hdpw0lpxil/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv>)

We published the above LLMOps course, which covers the fundamentals of AI engineering & LLMs, Building blocks of LLMs like tokenization, embeddings, attention, architectural designs and training, decoding, generation parameters, the LLM Application Lifecycle, context engineering, prompt management, defense, control, memory, temporal context, evaluation, tool use, red teaming, Adaptive LLMs, and Serving.

* * *

#### Tokenization and embedding

Tokenizers like Byte Pair Encoding (BPE) convert raw text into integer IDs from a vocabulary of roughly 50,000 tokens.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/vyHLNUt52NkKJYtZaFPbH1/email)   
---  
  
Each ID maps to a row in the embedding table, a learned matrix of shape `[vocab_size, hidden_dim]`. For a model with a hidden dimension of 4,096, each token becomes a 4,096-dimensional vector.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/aFfe5iiJBJ3qm2GcDD71UU/email)   
---  
![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/kpSVSPt6SsMT3VnKC68n1K/email)   
---  
  
Position information gets injected at this stage.

Most modern architectures use Rotary Position Embeddings (RoPE), which encode position by rotating the embedding vectors rather than adding a separate positional vector.

#### Transformer layers

The embedded sequence passes through a stack of transformer layers (typically 32 to 80+, depending on model size).

Each layer applies two operations in sequence:

**1) Self-attention** computes three projections per token (query Q, key K, value V) via learned weight matrices.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/7iKDQ4FLPcKtNLyUBzwBDp/email)   
---  
  
Each token's query is scored against every other token's key, and those scores (after scaling and softmax) determine how much of each token's value gets mixed in.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/8DfQ6wDDZGwStc3uA7TPVh/email)   
---  
  
2) **Feed-forward network (FFN)** processes each token's vector independently through a two-layer MLP. Attention moves information between positions. The FFN transforms it.

After the final layer, the model projects the last token's hidden state back to vocabulary size (`[hidden_dim, vocab_size]`), applies softmax, and samples from the resulting distribution to produce the first output token.

#### Prefill: the compute-bound phase

Processing the input prompt is the first phase. All tokens are processed in parallel: Q, K, and V are computed for every token simultaneously, and attention runs as a large matrix-matrix multiplication.

This is compute-bound work. The GPU's arithmetic throughput is the bottleneck, and utilization is high. The metric that captures this phase is Time to First Token (TTFT), the latency before the first output token appears.

During prefill, the model also populates the KV cache: the K and V tensors for every layer get stored in GPU memory for reuse.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/sXFnfJuhce32EmvH7Wfedx/email)   
---  
  
#### Decode: the memory-bound phase

Once the first token is generated, the model switches to generating one token at a time. For each new token, it only computes Q, K, and V for that single token. The K and V from all previous tokens are already in the cache.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/4boYz3rDN5N1coTQEAFV4y/email)   
---  
![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/uTTPZ3n1Z7cU5jeCk5zS29/email)   
---  
  
The arithmetic per step is tiny (one query vector against the cached key matrix instead of a full matrix-matrix multiply). But the GPU still loads every weight matrix and the entire cached K/V from memory for that small computation. The bottleneck flips from compute to memory bandwidth.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/x2BpP362VmxuUtNEjcdCYB/email)  
---  
  
The metric for this phase is Inter-Token Latency (ITL): the time between consecutive output tokens. Low ITL is what makes a model feel responsive.

#### The KV cache

Without caching, generating a 1,000-token response would require recomputing attention over the entire growing sequence at every step, giving quadratic complexity.

The KV cache stores each layer's K and V tensors once and appends new entries incrementally.

The video below depicts LLM inference speed with vs. without KV caching:

[ ](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/g3hnh5hmw9k057cr/aHR0cHM6Ly9hcGkuZmlsZWtpdGNkbi5jb20vZS9rN1lIUE4yNFNveHlNOG5HS1puRHhhL3ZjbjQ5OVo5NGN6OXFGZHNwbUNQUEUvcGxheWVy>)

The speedup is roughly 5x or more for long generations.

The cost is that the cache grows linearly with sequence length and exists per-layer. For a 13B-parameter model, the cache consumes roughly 1 MB per token. A 4K-token context burns through 4 GB of VRAM on the cache alone.

This is why long contexts get expensive. The cache competes directly with batch size for GPU memory, i.e., more cache per request means fewer concurrent requests per GPU.

Standard mitigations include quantizing the cache to INT8 or INT4, sliding window attention (dropping tokens outside a fixed window), grouped-query attention (GQA, sharing K/V across attention heads to reduce the number of cached tensors), and PagedAttention (the memory management trick behind vLLM that pages the cache like an OS pages virtual memory, eliminating fragmentation).

#### Frontier: redesigning attention around the cache

Quantization and paging treat the KV cache as a fixed cost to manage. DeepSeek's V4 series (released April 2025) takes a different approach: redesign attention so the cache is structurally smaller from the start.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/tefTCiy8P3oydWz9mSM7a7/email)   
---  
  
V4 uses a hybrid of two compressed attention mechanisms.

Compressed Sparse Attention (CSA) compresses KV entries by 4x using softmax-gated pooling, then applies sparse attention over the compressed tokens.

Heavily Compressed Attention (HCA) is more aggressive. It consolidates KV entries across 128 tokens into a single compressed entry and applies dense attention over those representations.

At a 1M-token context, V4-Pro requires 27% of the single-token inference FLOPs and 10% of the KV cache compared to DeepSeek-V3.2.

In absolute terms, that's 9.62 GiB of KV cache per sequence at 1M context in bf16, compared to an estimated 83.9 GiB for a V3.2-style architecture. With fp4/fp8 quantization on top, the cache shrinks by another 2x.

The KV cache has become the constraint the field is optimizing the model architecture around. When attention itself gets redesigned to minimize cache footprint, the bottleneck has shifted from "how to serve the model" to "how to design the model for serving."

#### [Quantization](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/9qhzhnhdrwlemqt9/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcXVhbnRpemF0aW9uLW9wdGltaXplLW1sLW1vZGVscy10by1ydW4tdGhlbS1vbi10aW55LWhhcmR3YXJlLw==>)

Training uses FP32 or BF16 for gradient stability. Inference doesn't need that precision. The memory savings from reducing bit width are linear:

  * 7B parameters at FP32: 28 GB
  * 7B parameters at FP16/BF16: 14 GB
  * 7B parameters at INT8: 7 GB
  * 7B parameters at INT4: 3.5 GB

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/s3EjgFRiQidmC1838vz4Z4/email)   
---  
  
INT4 is why 7B models run on laptop GPUs with 4-6 GB of VRAM. Methods like GPTQ and AWQ use per-channel scaling factors to minimize quality degradation from the lossy compression.

Done well, INT4 lands within 1-2 percentage points of the full-precision model on standard benchmarks.

Going from FP16 to INT8 often cuts inference latency in half with negligible quality loss, making quantization the single highest-leverage optimization for most deployments.

#### Serving infrastructure

Modern inference servers wrap the prefill-decode loop with several optimizations:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/b9eRjHJtYoz4Rbs5pJYfJJ/email)   
---  
  
  * [**Continuous batching**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/3ohphkh3gmnkl2cr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEzLw==>) interleaves tokens from multiple requests on the same GPU step, keeping utilization high even during memory-bound decode phases.
  * [**Speculative decoding**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/3ohphkh3gmnkl2cr/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEzLw==>) uses a small draft model to propose multiple tokens, then the large model verifies them in a single forward pass. When the draft model's acceptance rate is high, this effectively converts multiple sequential decode steps into one parallel verification.
  * [**PagedAttention**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/n2hohvhv0qklpgi6/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vcC9wYWdlZC1hdHRlbnRpb24taW4tbGxtcy8=>) (vLLM) manages KV cache memory in fixed-size blocks, eliminating fragmentation and enabling more concurrent requests per GPU.

Frameworks like vLLM, TensorRT-LLM, and Text Generation Inference (TGI) combine these techniques. A single GPU can serve dozens of concurrent users because decode leaves most of the arithmetic capacity idle, and continuous batching fills that idle capacity with other requests.

#### Putting it together

The full inference path:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/dtxELTqvJbdv9XUHpTsvdQ/email)   
---  
  
  1. **Tokenize:** Text becomes integer IDs via BPE.
  2. **Embed:** IDs become vectors. RoPE encodes position.
  3. **Prefill:** All input tokens processed in parallel through every layer. Compute-bound. KV cache populated. First token emitted.
  4. **Decode loop:** One token per step: project Q for the new token, attend over cached K/V, run FFN, sample. Append new K/V to cache. Memory-bound.
  5. **Detokenize:** Token IDs mapped back to text and streamed.

Some practical implications:

  * long prompts are expensive in TTFT (prefill)
  * long outputs are expensive in ITL (decode)
  * and they stress different hardware resources.
  * Context length isn't free because it bloats the KV cache and directly reduces batch capacity.
  * GPU utilization during decode can drop to 30% even on a fully loaded server, because the bottleneck is memory bandwidth, not arithmetic.
  * The fix isn't more compute, it's faster memory, a smaller cache, or better batching.

When someone tells you their model is slow, the first diagnostic is whether it's slow to start (prefill-bound, optimize TTFT) or slow to stream (decode-bound, optimize ITL).

[**To master the full LLMOps cycle with code, start here →**](<https://fff97757.click.kit-mail3.com/mvug5g3q6xt5hqp9zrkbmhrx206kpi3h5ed66/qvh8h7hdpw0lpxil/aHR0cHM6Ly93d3cuZGFpbHlkb3Nlb2Zkcy5jb20vbGxtb3BzLWNyYXNoLWNvdXJzZS1wYXJ0LTEv>)

We published the above LLMOps course, which covers the fundamentals of AI engineering & LLMs, Building blocks of LLMs like tokenization, embeddings, attention, architectural designs and training, decoding, generation parameters, the LLM Application Lifecycle, context engineering, prompt management, defense, control, memory, temporal context, evaluation, tool use, red teaming, Adaptive LLMs, and Serving.

👉 Over to you: are you running into TTFT or ITL bottlenecks in your deployments, and what's worked for you?
