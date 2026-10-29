---
type: "source"
tags: ["RSI", "AI-Agent/coding", "LLM/training"]
summary: "大模型递归自进化（RSI）系统全景：界定三层演进层级，深度拆解模型权重、脚手架、记忆技能库、代码自修改、多智能体协同五大技术路线，并提出落地五步法与选型矩阵"
sources: ["raw/articles/一文读懂_RSI_大模型递归自进化五大技术路线全景解析.md"]
updated: "2026-10-29"
---

# 来源摘要：一文读懂 RSI：大模型递归自进化五大技术路线全景解析

- **来源信息**：公众号 AI-Frontiers（2026-10-28）
- **原文链接**：[微信文章](https://mp.weixin.qq.com/s/shogmWqsWOZ6XfM40CAVLw)
- **核心议题**：突破大模型依赖人工数据调优的天花板，全方位解析大模型递归自进化（Recursive Self-Improvement, RSI）的演进层级、适用场景、五大技术实现路线、落地五步法与开源选型决策。

## 核心要点

1. **RSI 的三层演进递进层级**：
   - **单次自我修正（Self-Refinement）**：学生交卷前自查，仅针对当前单次输出进行反思重写，不持久化，做完即忘；
   - **持续自进化（Persistent Self-Improvement）**：建立错题本，将成功策略或修正规则写入模型权重、外部记忆库、Prompt 模板或工具箱，跨任务持久生效；
   - **递归自进化（Recursive Self-Improvement, RSI）**：系统不仅优化做题能力，**更将“产生改进的机制本身”作为改进对象**，自主重写元提示词、底层源码、优化算法或奖励函数，使改进行为本身越来越高效。
2. **场景适用度与安全避坑判据**：
   - **强烈推荐场景**：拥有客观/可自动验证反馈信号的封闭或模拟环境（代码单元测试、数学定理证明、算法复杂度优化、游戏交互）；人工 Prompt/Workflow 编排陷入瓶颈的复杂多模块系统；垂直领域高质量人工标注数据枯竭；开放式长期伴随任务（OS Agent、长周期助手）；
   - **严禁/不建议场景**：缺乏客观评判标准的纯主观创作（极易陷入自我迎合 Reward Hacking 与多样性坍缩）；对单次响应延迟与 Token 成本极度敏感的实时业务；无安全沙箱隔离的高危生产环境（防死循环与越权）。
3. **RSI 落地标准五步法**：
   - ① **划清能改边界**：遵循渐进暴露原则，从低风险的 Prompt/外部记忆起步，再开放生成/保存 Tool，最后才触及底层源码或权重；
   - ② **配置客观裁判**：以编译器报错、单元测试、沙箱指标为主；若用 LLM 裁判需配多模型投票或明确打分细则；
   - ③ **元智能体对症下药**：诊断上一轮失败日志与代码，针对性提出改写方案；
   - ④ **建立版本档案馆**：引入达尔文进化思想保留多样性分支，防止局部最优；
   - ⑤ **设定安全死线**：限制迭代步数与资源上限，异常时一键回滚。
4. **五大技术路线全景拆解**：
   - **① 模型权重与训练层自进化**：自出题、自答题、自打分与自微调闭环（代表：Meta *Self-Rewarding LMs*、UCLA *SPIN* 自博弈微调、Stanford *Quiet-STaR* 思维链内化、MIT *SEAL* 自生成微调指令）；
   - **② 提示词与脚手架程序自进化**：冻结基座权重，优化控制外壳与调用拓扑（代表：微软 *STOP* 自授优化器、*ADAS* 智能体自动化设计、Stanford *TextGrad* 文本反向传播、Stanford *DSPy* 声明式流水线编译）；
   - **③ 上下文、记忆与技能库自进化**：动态外挂记忆与可执行技能箱（代表：*Voyager* 终身技能库、*Reflexion* 语言强化反思、*A-MEM* 动态卡片盒记忆、*ACE* 上下文剧本演化、*MemEvolve* 记忆架构元进化、*Letta* 状态化 Agent）；
   - **④ 自我指向与代码自修改自进化**：Agent 直接读取、打补丁并重写自身运行代码（代表：*Gödel Agent* 哥德尔自指、*Darwin Gödel Machine (DGM)* 演化树、DeepMind *AlphaEvolve* 算法发现、Sakana AI *ShinkaEvolve* 高样本效率演化、Meta *Hyperagents* 任务与元智能体合一）；
   - **⑤ 多智能体协同与全自动 AI 研发自进化**：出题人 vs 解题人博弈共进化，或全自动科研实验闭环（代表：*R-Zero* 零数据博弈共进化、*EvoAgentX* MAS 工作流动态进化、Sakana AI *The AI Scientist (v1/v2)* 端到端科学研究、Karpathy *autoresearch* 极简自动训练循环）。

## 五大路线选型速查表

| 业务诉求与资源条件 | 推荐路线 | 首选框架 | 预期成本 |
|---|---|---|---|
| 使用闭源 API，希望自动提高业务准确率，免手调 Prompt | 提示词与脚手架 RSI | DSPy, TextGrad | 极低（几十美元 API，数十分钟） |
| 构建长周期 Agent，期望越用越懂业务、记忆教训并沉淀工具 | 上下文、记忆与技能库 RSI | Letta, ACE, A-MEM | 低（随日常交互演进，免训练） |
| 自动搭建并优化复杂的多智能体协同工作流拓扑 | 多智能体协同 RSI | EvoAgentX | 低~中（验证集评测 API 消耗） |
| 面对有确定评测指标的算法/代码优化，希望 AI 进化出最优程序 | 自我指向代码自修改 RSI | OpenEvolve, ShinkaEvolve, DGM | 中（代码沙箱 + 数百次 API 调用） |
| 拥有 GPU 算力，希望让 AI 自主迭代模型或改训练脚本跑实验 | 模型权重层 / 全自动 AI 研发 RSI | autoresearch, SPIN, R-Zero | 中~高（需 GPU 算力支持训练） |

## 关联概念与实体

- 核心概念：[[concepts/概念_RSI递归自我改进]]
- 宿主与编排：[[concepts/概念_Harness_Engineering_宿主编排工程]]、[[concepts/概念_Self_Harness_自主进化宿主系统]]、[[concepts/概念_Agent系统自动优化闭环]]
- 方法与算法：[[concepts/概念_DPO_直接偏好优化]]、[[concepts/概念_卡片盒笔记法]]、[[concepts/概念_GRPO_群组相对策略优化]]、[[concepts/概念_Reward_Hacking_奖励攻陷与作弊]]

---
> 📎 **物理文献**：[[raw/articles/一文读懂_RSI_大模型递归自进化五大技术路线全景解析.md]]
