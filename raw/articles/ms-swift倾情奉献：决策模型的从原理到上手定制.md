---
title: "ms-swift倾情奉献：决策模型的从原理到上手定制"
source: "https://mp.weixin.qq.com/s/tXsB41r725D8iIX6K5nuCQ"
author:
  - "[[魔搭ModelScope社区]]"
published:
created: 2026-10-26
description: "ms-swift 最近新增了对决策模型的支持，覆盖多样化的开源决策模型的训练与推理，包含JEV-27B-VL、Clef 和 OmniJev 等"
tags:
  - "clippings"
---
ms-swift 魔搭ModelScope社区 *2026年10月26日 19:04*

**00**

**引言**

为支持开源决策模型生态的发展，ms-swift 最近新增了对决策模型的支持，覆盖多样化的开源决策模型的训练与推理，包含JEV-27B-VL、Clef 和 OmniJev 等。框架内置了决策语料、专属损失函数和两级温度标定机制，可自动处理评分头精度与权重加载。  
  
于此同时，ms-swift 还提供 generic\_decision 转换路径，支持通过 LoRA 微调将通用生成模型转换为输出候选选项概率的决策模型。在 JEV 温度标定实验中，期望校准误差（ECE）降低 46.7%，预测准确率保持不变。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZQicUQHWjpgssoGekvERAENgyibBOCnLGRspbZkWpvEoCqh9ZZianSwQYhqk1JsUiaaWhIX2Lnrsegic5AZicWgjAaAibZpQaYd66QyEU/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

这里我们对决策模型的发展、技术原理等做了全方位的介绍，以及如何使用ms-swift来真正上手决策模型，实现针对实际应用场景的决策模型定制训练与优化。希望和开源社区一起，共同促进决策模型开源生态的健康蓬勃发展。  
  
代码仓库：

https://github.com/modelscope/ms-swift

**01**

**决策模型的兴起**

### 1.1 生态发展

2026 年 9 月，TypeSafe AI 发布了首个规模化落地的决策模型产品 Jev。其 定位为 System One 决策模型，不生成任何自由文本；给定上下文 x 与预先给定的候选选项集合，它直接为每个选项输出一个校准概率。  
  
在实现上，这通常由“打分 + 归一化”两步构成：编码器将上下文与选项联合编码为隐向量，打分头给出每个选项的标量分数，再经温度 τ 的 Softmax 归一化。  
  
这里所说的校准，是指预测置信度与真实正确频率相一致，通常以期望校准误差（ECE）度量：把样本按置信度分桶，ECE 即各桶“平均置信度与实际正确率之差”按桶内样本数加权的绝对值总和。  
  
由于省去了自回归解码，一次前向即可完成整组选项的打分。Jev 以托管服务交付，主打机器速度的判断，覆盖分类、路由、打分三类需求。  
  
由于 Jev 具有不需要预先设定分类数量、泛化性强、置信度可用的优势，短时间内这条赛道迅速成形。不同的决策模型在技术路线上，对于不同维度上各有侧重：模型层面，判别式打分与生成式概率截取并存；  
  
解码层面，逐题独立调用与多问题联合解码互补。  
  
**生成式路线：OpenAI Decisions**  
Jev发布一个月后，10月份OpenAI 推出 Decisions 服务。它构建在自家生成模型之上，把决策能力单独开放为一个接口：调用方给出选项集合，接口在生成分布上截取各选项对应起始 token 的 logits，经温度 Softmax 归一化后返回每个选项的概率。  
  
换言之，它不训练新的判别头，而是把生成模型已有的知识收拢进一个单独开放的接口。对已经在使用 OpenAI 的用户，这是一条接入成本较低的路径。  
  
第三方研究显示，这一接口的概率在错误检出能力上优于底座生成模型输出的字母概率。后者是让生成模型直接读出选项字母时，首 token 分布中对应字母那一项的裸概率。  
  
若以置信度区分“模型答对或答错”的能力，对应的度量是 AUROC：令 c⁺ 与 c⁻ 分别为随机抽取一条答对与一条答错样本时模型对其所选答案给出的置信度，则：  
![AUROC = P(c⁺ > c⁻)](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZTTibCh5qpYKCPmAW3rhzXvZWGXgtibZjLYv1KTSEEePibS1OwCZR2lQ3NOo8vSAD7nKlZc4qUsiczyuY7LXdzWnvJ1CW78OnsyM3c/640?wx_fmt=png&from=appmsg#imgIndex=1)

AUROC = P(c⁺ > c⁻)

  
  
**联合解码路线：Clef**  
与此同时，Cloudflare 开源了 Clef，展示了另一条解码技术路线。Clef 使用多问题联合解码：一次前向同时回答一整组结构化问题，直接建模全部问题答案的联合分布，而不是独立调用多次、分别计算边缘分布。  
  
除了省下多次前向与上下文的重复编码，联合建模还能捕捉问题之间的相关性，因此适合表单式和清单式的批量判定。由于权重和配置全部开放，Clef 既可以私有化部署，也可以深度定制。  
  
**开源社区的不同规模实现**  
开源社区对于决策模型展示出了极大的热情。探索不同技术路线的决策模型在短时间层出不穷，在魔搭上我们观察到了来自各家的不同决策模型开源：其中由autotrust 开源的 JEV-27B-VL 面向多模态决策，通过保留通用多模态编码器与输出层，在输出分布上按 verbalizer 读出各选项的对数概率，加偏置、除以两级温度后进行 Softmax，几乎不引入新参数，可以直接使用 LoRA 微调，并有效利用社区已有的 vLLM 等部署方案。  
  
而 OmniJev 则基于 Qwen3.5-4B 混合架构，覆盖图像和视频评分，部署门槛较低。此外，配套的 Open-Jev 语料也在同期开源。  
  
在更轻量的尺度上，来自NanoJev 基于 Qwen3-0.6B，保留了逐候选交互的结构设计：每个选项与上下文拼接后独立送入模型编码打分，再对打分做归一化，常用于研究和教学。NeoHorse 则探索智能体原生场景下的决策能力，在魔搭社区下载量较多。

### 1.2 决策模型与传统分类、生成式任务的比较

传统分类方法通常需要为每个任务定制专属分类头，更换任务时往往需要重新训练。相比之下，决策模型以语言模型为基座，将评分类任务统一为是非判断、多选一、有序打分三种题型。这种架构不仅继承了基座的语义理解能力，也具备对未见任务进行零样本泛化的潜力。  
  
在处理选择题时，生成式模型通常先输出文本，再解析答案；决策模型则通过一次前向直接计算各选项概率。由于不需要逐 Token 采样，决策模型在这类结构化输出任务中通常具有更低的推理延迟。  
  
此外，其概率分布基于当前题目的选项集合进行 Softmax 归一化，使同一道题内不同选项的置信度具有可比性。  
  
我们可以通过下图来对比生成式路径与决策模型路径：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZRr0gbGZwObIjIdMrjQmSdlxZ7dBLda90d1yNkrwX6KTFGanUdy0icCEWrOXQicK21HMfPrzgOMGee1p802ZG9GMyOib9dxiaXfovw/640?wx_fmt=png&from=appmsg#imgIndex=2)

2026 年 10 月的一项研究对比了 Jev、OpenAI Decisions、Clef 及传统生成模型在韩美医学执照考试中的表现。结果显示，生成式模型的预测概率普遍饱和于 1.0，表现出明显的过度自信偏差。  
  
对比之下，三款决策模型不仅保持了韩文 83.4%–92.0%、英文 84.8%–87.7% 的高准确率，其校准后的概率也更能有效识别错误：错误检出能力（AUROC）：韩文题达到 0.856–0.935，英文题达到 0.864–0.903。  
  
低置信度覆盖：置信度最低的 20% 答案覆盖了超过一半的错误案例，其中韩文题为 56%–91%，英文题为 62%–72%。  
  
若将这些低置信度样本路由至更强的大模型复核，整体准确率可提升 6–9 个百分点，而总成本仅为全量大模型推理方案的 25%–33%。  
  
低置信度样本覆盖错误的效果：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZT8Zst5CiaG1Llne38pjBAwm7kO7drCzniaRXs8gBwE90Thn9eicia8GqvajPvFGFWxOjlqupIgHemVCymaDJicMqmo70cojTcuFj6E/640?wx_fmt=png&from=appmsg#imgIndex=3)

这体现了决策模型与常规生成式调用的一项重要差异：当置信度本身是产品的一部分时，不能直接把未经验证的生成概率当作可靠置信度。

### 1.3 使用场景

只要输出需要从一个固定选项集合中做选择，就是决策模型的目标场景。常见场景有五类：内容审核与审批授权：允许、驳回还是搁置，并附带可信概率。  

- 意图与路由分类：把请求路由到正确的处理方，低置信度时升级人工。
- 质量与偏好评分：对回答、翻译、生成内容进行有序打分。
- 数据管线中的偏好过滤：使用概率阈值筛选合成数据。
- 置信度级联：决策模型先回答，低置信度样本再交给大模型，以较低成本提升整体效果。

**02**

**技术版图**

### 2.1 决策模型的类型划分

决策模型的架构差异主要体现在四个维度：评分头的信号来源、候选项的序列化方式、候选间的交互机制，以及多问题的联合建模策略。依据这些维度，开源社区公开结构的模型可以归纳为五种类型。  
  
决策模型类型划分：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZSFaNthhMSkibp8IAg8uSUicibBM2bVUzzsKicKXfS36ibBUzhyL6sUOucNXbkX2MmiclpfdQf1KVibS9ASMibaIicMPyTyeJvJl08Ql3XY/640?wx_fmt=png&from=appmsg#imgIndex=4)

五种类型各有不同的设计意图。token 读出型几乎不引入新参数，可以直接使用 LoRA 微调，适合从既有生成模型迁移；隐状态读出型对骨干选择自由，适合没有语言输出层的轻量底座；联合解码器型用较重的头换取问题间的信息交互，适合一组问题需要联合判定的结构化场景；  
  
逐候选显式交互型用计算量换取候选间的精确建模，适合候选数量适中、关系复杂的任务；多模态专用型面向视觉和有序打分进行端到端设计，适合图像和视频评分。  
  
这些类型强调的设计维度并不完全相同，彼此之间可能存在重叠。例如，多模态模型也可以采用 token 读出。类型之间没有绝对优劣，选哪种方案取决于任务形态、部署条件和定制深度。

### 2.2 损失函数谱系与训练方案

决策模型的类型不同，loss 和训练方案也有所差异，但思想是统一的：本文涉及的损失函数都属于适当评分规则，即在真实分布处取得最优值的评分函数；在这些实现中，可以将它们组织为一个共享基础项与若干校准项。  
  
整体谱系如下：

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZSQTJDI8IibynmbNJ0P8gscZaLqibdYYAOzPmYfXRJM1B96v4ZUr0Nk2UlQEwibLhoTxVhHFhGSSjIyDpJwITZQtgDibUbzNCE5E0A/640?wx_fmt=png&from=appmsg#imgIndex=5)

所有模型都包含一个共享的基础项：掩码软交叉熵（Masked Soft Cross-Entropy）。其数学本质是对数得分（Log Score）。当标签为独热分布时，它退化为标准交叉熵；  
  
当标签为软分布时，则等价于最小化 KL 散度。该机制采用单精度掩码计算，不截断概率，使高置信度的错误预测仍能保留梯度信息。  
  
校准项有三种。RPS 即有序概率得分，衡量预测分布与目标分布的累积分布差距，作用于有序打分题型；Brier 得分计算全部题型的均方概率误差；序数交叉熵则为有序打分保留档位顺序。  
  
基础项和校准项的组合分为两条路线。一条路线使用统一 loss 覆盖全部题型，把题型差异交给结构处理：JEV 依靠 verbalizer 设计，把三类题型统一到温度感知的软交叉熵中；  
  
Clef 依靠类型嵌入向量把题型编码进表示，loss 公式不区分题型。  
  
另一条路线按题型选择 loss：NanoJev 对多选一使用交叉熵，对是非判断使用二元交叉熵，对有序打分使用序数交叉熵，每种题型采用对应的训练目标。前者强调统一，后者强调针对性。

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZTocVvYqokf1CMQR6ydDt3frF1iazeqribgFTCVUgnwH8Rh4krib0iaPic8mV0pEOZ8EmwqIQibCsLWibQpgtiaQuHFWV0tfECsicAD40Bk/640?wx_fmt=png&from=appmsg#imgIndex=6)

训练方案相应有四种：方案一的校准参数在训练后固定；方案二先训练评分头，再解冻全量参数；方案三把校准作为奖励信号直接优化；方案四不让校准参数参与梯度，而是在训练结束后使用验证集单独拟合温度。

**03**

**ms-swift 的支持体系**

ms-swift 是 来自 ModelScope 团队开源训练框架。决策模型发布后，针对这一新的模型范式，ms-swift 迅速支持了多个开源决策模型的训练和推理，并内置配套语料。

### 3.1 支持的模型与训练方式

通过ms-swift训练决策模型，只需添加 --task\_type decision 参数启用决策模式。ms-swift 为不同的开源决策模型预设了专属损失函数：例如JEV-27B-VL 采用结合蒸馏目标与 RPS 的 distill\_rps；  
  
Clef 采用结合标签平滑交叉熵与 Brier 得分的 smooth\_brier；OmniJev 则采用结合纯对数评分与 RPS 的 ce\_rps。此外，框架还提供不含额外校准项的通用 scoring 模式。  
  
Open-Jev 语料已内置注册，使用 --dataset open\_jev\_jev:all 即可直接训练，无需自备数据。  
  
在训练器层面，ms-swift 实现了以下自动化处理：精度管理：自动激活评分头参数并将其提升至全精度训练，偏置和温度参数始终保持单精度。  
  
指标监控：同时计算“每题准确率”和“每记录准确率”。前者逐题统计，后者要求整条记录中的所有问题均正确，适用于联合解码场景。  
  
权重隔离：评分头权重独立保存，推理时通过自动钩子机制加载。

### 3.2 温度标定机制

温度标定由训练后的回调自动完成，使用 task\_type=decision 时会自动挂载，全程不需要额外配置。整体流水线如下：

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZSV6picHlBt4UazIAph7ibKPw2WzP87vibLTJBN0Ru3V4OEmOMVWwsnlujwvZpntyfNuQicfibB8gIfRpBj03zs7q0BQQDiaWON5uyNE/640?wx_fmt=png&from=appmsg#imgIndex=7)

两级温度相乘得到生效温度：全局温度捕捉模型整体的置信度偏差，每题型相对温度捕捉题型特有的偏差。是非题欠自信、打分题过自信的情况可以同时纠正。  
  
汇报指标使用两折交叉验证得到样本外数值：记录按奇偶对半拆分，每一半的温度在另一半上拟合。训练开始时，框架先使用原始温度评估一次基线，使日志能够分清微调和校准各自的增益。温度只是 logits 的单调变换，不改变预测答案，只修正概率分布的尖锐程度。  
  
实测中，在 JEV 官方工厂温度下，ECE 从 0.00268 降至 0.00143，降幅为 46.7%。另一组 80 条留出数据的温度消融显示，ECE 从 0.165 降至 0.121，Brier 得分下降 9.5%，准确率严格不变。

![图片](https://mmbiz.qpic.cn/mmbiz_png/ia2awwZLWFZRjsAicVWEjZBXwMfCibhsIiaNy4gE1ickW5icOCywjDeu7X8q11E928g1YJiamVmpq8EtHLO8WaTicBHKvNe5rkibLHyUEl0wSUia0x46A/640?wx_fmt=png&from=appmsg#imgIndex=8)

### 3.3 通用转换路径：生成模型到决策模型

除了三个官方模型，ms-swift 还提供 generic\_decision 路径：能把因果语言模型转换为 JEV 风格的决策模型，不更换底座，不改动原有架构。转换流水线如下：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZQOfsNh7ugQcUxadUbz6Y4NVz1wWkpyBIm6iccBIxibw1YpzvODSeqlCOMFMZNEqmibWMib8tNbXeQvLt9LZlmSWxLPyAjViaq3PoTg/640?wx_fmt=png&from=appmsg#imgIndex=9)

训练命令如下：

```
swift sft \
    --model Qwen/Qwen3.5-4B \
    --model_type generic_decision \
    --task_type decision \
    --loss_type distill_rps \
    --tuner_type lora --target_modules all-linear \
    --dataset open_jev_jev:all \
    --output_dir output
```

训练完成后，可以直接使用 swift infer 执行推理。模型输出每道题的预测下标和各选项概率，不生成自由文本。增加 --metric acc 后，可以在决策数据集上自动计算准确率。

### 3.4 训练结果

四个模型分别执行了完整流水线，包括训练前推理、本地数据集训练和训练后推理，结果如下：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ia2awwZLWFZQjNnRHZmNNjvQjnbr8EYnffQhGcJ1D7NQhH5M4sfYCgnCddOIeibxz3gjtGliaMRWiatlfG57rJ7VRy7G4qVOoWwRNFaK9mn3vWU/640?wx_fmt=png&from=appmsg#imgIndex=10)

三个官方模型经 ms-swift 微调后，准确率均有提升。通用转换路径也体现出可行性：一个未经决策任务训练的普通对话模型，仅通过 generic\_decision 完成一轮微调，准确率便从随机水平提升至 0.6667。

**05**

**小结**

ms-swift 已构建起支持决策模型范式的工程闭环。用户只需通过 --task\_type decision 即可启用专属损失函数与内置语料支持。框架底层自动处理评分头精度、两级温度标定及权重加载，并通过 generic\_decision 路径实现生成模型到决策模型的转换。  
  
本次实验中，四个模型微调后的准确率提升为 37%–300%，其中通用对话模型经一轮训练后从随机水平提升至 0.6667。在 JEV 温度标定实验中，ECE 降低 46.7%，预测准确率保持不变。  
  
两组结果分别反映了任务微调和概率校准的作用。  
  
未来，ms-swift 将持续跟进新的模型结构，扩展评分头的灵活训练与支持，同时探索将 RLCD 强化学习引入开源生态，以完善置信度级联能力。对于分类、路由或打分等依赖可信概率的业务场景，ms-swift 已提供标准化的训练、推理与评估方案。

---

```
👇点击关注ModelScope公众号获取更多技术信息~
 魔搭ModelScope社区  模型开源社区魔搭社区ModelScope官方账号 183篇原创内容  
          公众号
```

闪记

复制 LaTeX 公式