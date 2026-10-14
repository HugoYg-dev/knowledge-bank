# 项目交接文档 (HANDOFF.md)

> 生成时间：2026-10-14  
> 目标文件：[`raw/out-blogs/给语言模型装一个动态分类头.md`](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/给语言模型装一个动态分类头.md)  
> 作者署名：`Hugo Yang` | 状态：`draft: true`

---

## 1. 任务目标 (Goal)

对深度技术博客草稿 [《给语言模型装一个动态分类头》](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/给语言模型装一个动态分类头.md) 进行技术审查与深度查漏补缺。
比对库内 5 篇核心原始文献与会话记录，全面补齐因果语言模型 Logits 提取、BPE 分词陷阱、ModernBERT 双向编码器、动态掩码与 `torch.gather` 抽取、RLCD 严格适当评分规则、行动网络 62.5% 成本收益门槛、多查询并发批处理与隔离机制、System 1 / System 2 两模型协作等关键硬核技术要点。

---

## 2. 当前进展 (Current Progress)

### 2.1 原始 4 项遗漏已全部核验落实
1. **多维度问题并发批处理（Multi-Query Batching）**：已写入第 VI 节，涵盖 GPU 显存打包单 Batch、~35ms 单次前向返回多维度概率。
2. **三种结构化决策原语（Primitives）**：已写入第 IV 节，明确定义 choice、score（含连续平滑期望公式 $\mathbb{E}[S] = \sum i \cdot p_i$）与 noul。
3. **多 Token 词元的序列联合对数似然（Sequence Joint Log-Likelihood）**：已写入第 II 节，阐明 $\sum \log P(\text{token}_t \mid \text{token}_{<t})$ 与长度惩罚因子 $|W|^\alpha$。
4. **两模型协作大图景（Two-Model Architecture）**：已写入第 VIII 节，界定 System 1（毫秒级快思考前置网关）与 System 2（慢思考生成推理）边界。

### 2.2 深度审计挖掘出的 3 项高价值遗漏已完成补全
1. **RLCD 校准强化学习的数学本质（第 IV 节）**：
   - 深入解释了传统交叉熵（逼迫 Logit 趋于极值）与二元奖励 RL（非 1 即 0）破坏校准的数学机理。
   - 补齐了决策理论中的**严格适当评分规则（Strictly Proper Scoring Rules）**：组合对数评分（$S_{\log}$）、球面评分（$S_{\text{sph}}$）与排序概率评分（$S_{\text{rps}}$）。
   - 阐明 RLCD 从优化目标根源保证校准，与仅充当“谦虚滤镜”的推理期温度缩放（Temperature Scaling）存在本质区别。
2. **概率校准实测证据（第 V 节）**：
   - 引入 Archer Hume 对 Jev 的 1200 题 MMLU 测谎数据（ECE 仅 0.031）。
   - 引用简单题（86.7% 正确率自报 83% 把握）与难题（32% 正确率主动降至 30% 把握）的实证，为 62.5% 行动门限提供可信度支撑。
3. **问题间物理隔离机制（第 VI 节）**：
   - 详述动态注意力掩码与 KV Cache 冻结分支复用两大工程方案。
   - 引用 Archer Hume 暗号实验（问题间隔离读取概率为 0.00，放入共享 State 跃升至 0.90+）实证并发提问互不串台。

### 2.3 补充的工程细节与边界指引
1. **参数量校准（第 IV 节）**：标明 ModernBERT-large 主干 3.95 亿参数，算上决策头与行动网络全模型约 4.21 亿参数，完全对齐 Laya 论文。
2. **动态模型路由（第 VIII 节）**：将 System 1 应用扩展至 Model Routing——“路由本身也是一次判断，原本就没必要用昂贵的推理模型去推理该不该用推理模型”。
3. **工程适用边界与系统级延迟税（第 VIII 节）**：总结适合标准明确、证据集中、可检查有退路的高频场景；警示盲目在前置堆叠分类头可能反噬系统总延迟（649ms $\to$ 1087ms）。

### 2.4 活人感写作（human-writing）规范净化
1. **中文冒号清零**：全文 20 处提示性/列表冒号全部化解为自然断句或句号，无一处违规。
2. **翻案句拔除**：第 260 行 `并不是……而是……` 及隐蔽翻案变形全部改写为正面立论。
3. **致命概念缝合纠偏**：将双向编码器（ModernBERT）误植“KV Cache 冻结分支”的硬伤准确拆解为动态注意力掩码与因果解码器分支的区别。
4. **抽象借喻与大词剔除**：“引力吸收槽”、“反射神经元”、“架构跃迁”等虚浮词汇全部还原为纯正工程事实。
5. **自动化脚本校验**：`uv run python .agents/skills/human-writing/scripts/check_prose.py` 0 报错，硬禁项全数清零。

### 2.5 工程健康度
- 运行 `uv run scripts/vault_lint.py lint` 100% 校验通过，无任何语法、链接与 Frontmatter 异常。

---

## 3. 经验总结与有效实践 (What Worked)

1. **多文献交叉逆向核验**：对照《一文拆解Jev架构》中的 Archer Hume 黑盒实验与《Laya 开源》白盒公式，将抽象的概念落到了具体的技术机制上（如指针头 vs 候选间注意力、62.5% 阈值的成本矩阵推导）。
2. **可运行的 PyTorch 架构示例**：通过 `DynamicClassificationHead` 完整展示 `decision_layers`、`torch.gather` 掩码提取、归一化香农熵计算以及行动网络的组装。
3. **保持作者文风与叙事节奏**：全篇采用技术散文与硬核推导演进的风格，通俗易懂且逻辑环环相扣。

---

## 4. 警惕事项与避坑指引 (What Didn't Work / Avoid)

1. **避免混淆“格式不出错”与“判断正确”**：严格说明 Schema Matching 只能保证不吐出预设外的 Key，不等于逻辑准确率 100%。
2. **避免将温度缩放与 RLCD 混为一谈**：温度缩放仅是事后全局调节方差与熵，RLCD 是通过严格适当评分规则训练内在诚实度。
3. **严格遵守 `AGENTS.md` 规范**：严禁执行任何自动 `git commit`、`git push` 等写操作。

---

## 5. 后续行动建议 (Next Steps)

1. **终稿通读**：若需正式发布技术博客，可直接在 [`raw/out-blogs/给语言模型装一个动态分类头.md`](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/给语言模型装一个动态分类头.md) 基础上修改 `draft: false` 并校对排版。
2. **协同博客对齐**：库内同主题姊妹篇 [`raw/out-blogs/既然Logits排序与Softmax完全一致_为什么还需要算Softmax.md`](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/既然Logits排序与Softmax完全一致_为什么还需要算Softmax.md) 同样处于草稿状态，若需要可进行概念呼应与联动校对。
