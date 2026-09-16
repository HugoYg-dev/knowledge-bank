---
title: PyTorch Dataloader has two terrible default settings
source_key: dailydoseofds
email_subject: 4 Layers of Agentic AI Systems
email_sender: Daily Dose of DS <avi@dailydoseofds.com>
email_date: Mon, 25 Aug 2025 20:26:25 +0000
email_id: 198e2e9234d8b09f
article_id: 198e2e9234d8b09f:1
published: '2025-08-25'
tags:
- DeepLearning
- Skill/python
- Infra/training

---

# PyTorch Dataloader has two terrible default settings

- **原邮件主题**: 4 Layers of Agentic AI Systems
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 25 Aug 2025 20:26:25 +0000
- **ID**: 198e2e9234d8b09f

---

## [**PyTorch Dataloader has two terrible default settings**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>)

Consider the model training loop in PyTorch shown below:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/dr5AG5M8WL9EDANA3K2dRA/email)   
---  
  
  * Line 5 transfers the data to the GPU from the CPU.
  * Everything executes on the GPU after the data transfer, i.e., lines 7-15.

This means when the GPU is working, the CPU is idle, and when the CPU is working, the GPU is idle, as depicted below:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/qGeRCLjW9jUVErHJcAej9r/email)   
---  
  
Ideally, you can transfer batch 2 when the GPU is training the model on batch 1.

Enabling this is quite simple in PyTorch.

First, define the DataLoader object with `pin_memory=True` and `num_workers`.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/5phRh3uW6Wgj5gk3EmNFsX/email)   
---  
  
Next, during the data transfer step in the training loop, specify `non_blocking=True`:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/a2CsSDdySt1LMnJWGauAcr/email)   
---  
  
Done!

Here's the speed comparison on MNIST:

  * Under normal settings, the model takes 43 seconds to train on 5 epochs.

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/rpgLweXF9r1KQr7DvST1Xx/email)   
---  
  
  * But with updated settings, the same model trains in 9 seconds:

![](https://embed.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/bsSrmTpSzHrquVM19xev46/email)   
---  
  
Of course, this isn't the only technique to accelerate model training.

[**We covered 15 techniques (with code) to optimize model training here →**](<https://www.dailydoseofds.com/15-ways-to-optimize-neural-network-training-with-implementation/>)
