# 项目交接文档 (HANDOFF.md)

> 生成时间：2026-10-14  
> 目标文件：
> 1. [`raw/out-blogs/给语言模型装一个动态分类头.md`](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/给语言模型装一个动态分类头.md)
> 2. [`raw/out-blogs/既然Logits排序与Softmax完全一致_为什么还需要算Softmax.md`](file:///Users/ZHao/WorkSpace/knowledge-bank/raw/out-blogs/既然Logits排序与Softmax完全一致_为什么还需要算Softmax.md)  
> 作者署名：`Hugo Yang` | 状态：两篇技术博客均已完成多维度审查与改写定稿

---

## 1. 任务目标 (Goal)

对两篇深度技术博客草稿进行技术事实核验与 `human-writing`（活人感写作规范）全面重构：
1. **第一篇《给语言模型装一个动态分类头》**：比对库内 5 篇核心原始文献与会话记录，全面补齐因果语言模型 Logits 提取、BPE 分词陷阱、ModernBERT 双向编码器、动态掩码与 `torch.gather` 抽取、RLCD 严格适当评分规则、行动网络 62.5% 成本收益门槛、多查询并发批处理与隔离机制、System 1 / System 2 两模型协作等硬核技术要点。
2. **第二篇《既然 Logits 排序与 Softmax 完全一致，为什么我们还需要算 Softmax？》**：拆除 LLM 草稿脚手架（大纲构思元文本与戏剧化五幕剧外壳），消除全部中文冒号、破折号与翻案句，修正交叉熵梯度在离谱错误时“指数级放大”的严重数学错误，修复 Top-p 采样的 Batch 掩码展平崩溃 Bug，并补齐 GLM 规范链接函数、最大熵原理与 FlashAttention 在线安全 Softmax 的工程原理解析。

---

## 2. 当前进展 (Current Progress)

### 2.1 第一篇《给语言模型装一个动态分类头》已全部落实
1. **多维度问题并发批处理（Multi-Query Batching）**：涵盖 GPU 显存打包单 Batch、~35ms 单次前向返回多维度概率。
2. **三种结构化决策原语（Primitives）**：明确定义 choice、score（含连续平滑期望公式 $\mathbb{E}[S] = \sum i \cdot p_i$）与 noul。
3. **多 Token 词元的序列联合对数似然（Sequence Joint Log-Likelihood）**：阐明 $\sum \log P(\text{token}_t \mid \text{token}_{<t})$ 与长度惩罚因子 $|W|^\alpha$。
4. **两模型协作大图景（Two-Model Architecture）**：界定 System 1（毫秒级快思考前置网关）与 System 2（慢思考生成推理）边界。
5. **RLCD 严格适当评分规则**：补充组合对数评分、球面评分与排序概率评分数学原理。
6. **概率校准实测证据**：引入 Archer Hume 对 Jev 的 1200 题 MMLU 测谎数据（ECE 0.031）。
7. **技术概念纠偏**：准确拆解双向编码器的动态注意力掩码与因果解码器分支的区别，纠正 KV Cache 冻结分支的概念缝合。
8. **文风审查**：通过 `check_prose.py` 自动化检测，0 冒号、0 破折号、0 翻案句。

### 2.2 第二篇《既然 Logits 排序与 Softmax 完全一致，为什么还需要算 Softmax？》已全部落实
1. **草稿脚手架与戏剧戏服彻底拆除**：
   - 彻底删除第 0、1 节的大纲构思、灵感说明及写作技巧元文本；
   - 拆除“第一幕”至“第五幕”的舞台剧小标题，重组为平实自然的工程师实战随笔结构；
   - 剔除“外交辞令与内心独白”等机械拟人金句，采用克制扎实的工程结语收束；
   - 将原孤立的代码示例自然嵌入到 Greedy 验证与 Top-p 采样原理段落中。
2. **重大数学事实纠正**：
   - 纠正原文声称 Hinge Loss 无法“像指数函数那样在面对离谱错误时产生强烈的回传动力”的严重错误；
   - 明确证明 Softmax + 交叉熵损失的梯度 $\nabla_z \mathcal{L} = \mathbf{p} - \mathbf{y}$ 模长严格有界在 $[-1, 1]$ 之间，绝非指数放大（否则将导致梯度爆炸）；其真正优势在于无梯度死区、持续推动特征分离（隐式最大边距正则化）以及多类别概率加权全局抑制。
3. **核心工程实现与前沿演进补全**：
   - 区分 llama.cpp（基于堆/局部排序截断）与 GPU/vLLM（基于 Radix 选择或无排序拒绝采样）在 Logits 阶段局部 Softmax 的工程差异；
   - 梳理从 PyTorch 算子融合到 Fused Linear Cross-Entropy（SRAM 分块在线更新 Log-Sum-Exp 并立即丢弃 Logits）的演进；
   - 深入阐述 FlashAttention 中 Online Safe Softmax 动态维护最大值与分母重缩放累加和的机制。
4. **代码致命 Bug 修复**：
   - 修复示例 2 中多批次布尔掩码展平导致跨样本词表全被置为 `-inf`、进而引发 Softmax 输出 `NaN` 导致 `torch.multinomial` 崩溃的致命 Bug；
   - 引入标准 `.scatter()` 与 `masked_fill` 映射，并通过单调性预排序避免重复计算全量 Softmax。代码已在本地 PyTorch 单元测试通过。
5. **活人感写作（human-writing）规范净化**：
   - 运行 `uv run python .agents/skills/human-writing/scripts/check_prose.py` 校验：
     - 中文冒号：0 处（原本 82 处，全部清除）
     - 破折号：0 处（原本 18 处，全部清除）
     - 翻案句：0 处（原本 3 处，全部清除）
     - 洞察路标：0 处（原 5 处，全部清除）
     - 动词名词化：0 处（“进行优化”等全部清除）

### 2.3 全库健康度
- 运行 `uv run scripts/vault_lint.py lint` 100% 校验通过，无任何语法、死链与 Frontmatter 异常。

---

## 3. 经验总结与有效实践 (What Worked)

1. **三维并发审查（Subagents Fan-out）**：
   - 硬禁令检查员（`check_prose.py` + 人工逐行禁词、冒号、破折号清查）；
   - 材料真实度审核员（数学推导严谨性、梯度边界、算法细节与代码 Bug 捕获）；
   - 说话位置与白话韵律审查员（拆除大纲元说明、相声捧哏腔与假深刻拟人金句，重构段落推进）。
2. **严防数学与代码硬伤**：大模型生成的草稿常伴随虚浮的修辞推断（如“指数级放大梯度”）和未经多 Batch 测试的示例代码（如布尔张量索引展平 Bug），深度技术审核必须经受公式推导与单元测试实测检验。
3. **把代码融入论据**：工程文章的代码应当紧随原理段落作为实证，而不是孤立地放在文末当代码仓库。

---

## 4. Git 提交指令（由用户执行）

根据 `AGENTS.md` 绝对红线，Agent 不自动执行 git 写操作。请用户核对修改后在终端中执行：

```bash
git add "raw/out-blogs/既然Logits排序与Softmax完全一致_为什么还需要算Softmax.md" "HANDOFF.md"
git commit -m "docs(out-blogs): 重构Logits与Softmax博文草稿并符合human-writing规范

- 拆除大纲构思元文本与戏剧化五幕剧脚手架，重构成平实自然的工程师随笔
- 消除全部中文冒号、破折号、翻案句、洞察路标与拟人化金句，check_prose 0报错
- 纠正交叉熵梯度在离谱错误时'指数放大'的数学硬伤，证明其严格有界在[-1, 1]及无死区特性
- 修复Top-p采样代码中多Batch布尔掩码展平的致命Bug，引入scatter映射并本地验证
- 补齐GLM规范链接函数、最大熵原理与FlashAttention在线安全Softmax工程细节
- 校验通过vault_lint并更新HANDOFF文档"
```
