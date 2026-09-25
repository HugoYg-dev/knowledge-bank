# Wiki Index

> 内容索引，每次 ingest 后更新。按类型分组。

## Sources

- [[Agent时代，RAG怎么选？这份指南一次讲清！]] — 系统梳理面向 Agent 的 RAG 技术选型指南：解构 Naive/Advanced/Modular 演进脉络，对比 GraphRAG、Agentic RAG、LLM Wiki 与上下文压缩，并建立检索与生成解耦的评估闭环及非 RAG 适用边界（RAG/retrieval, RAG/eval, AI-Agent/context-engineering）
- [[Laya开源_421M参数33毫秒System1决策]] — Convai Innovations 开源 421M 非自回归 System 1 决策模型 Laya，基于 ModernBERT 与 RLCD 强化学习实现 33ms 极低延迟与严格概率校准（LLM/inference, AI-Agent/tool-calling, LLM/training/RL）
- [[更好的替代品早已存在，Jev 留给研究的只剩时机]] — 深度剖析 TypeSafe 推出的无生成判断接口 Jev，对比开源小模型本地提取 Logits 的工程表现，梳理判断 API 的五次浪潮演进史与智能体高频状态机解耦动因（LLM/inference, AI-Agent/tool-calling）
- [[Everyone is building LLM routers, we deprecated ours]] — Manifest 团队反思并废弃其 LLM 模型路由器的实践经验：复杂度无法单凭 Prompt 判断、前缀缓存收益远高于路由分流，且不可预测性增加了 Agent 系统的维护代价（LLM/inference, Infra/serving）
- [[新模型Jev_爆红一周_不生成文字只输出概率却被玩出了花]] — TypeSafe AI 推出非自回归概率决策模型 Jev 与 RLCD 范式（AI-Agent/tool-calling, LLM/inference）
- [[这是一篇把RSI讲明白的科普级综述]] — 递归自我改进（RSI）从 EURISKO 到元研究系统的四层标准与四大安全门禁（RSI）

- [[RAG夺命10连问，你能抗住第几问？]] — 全面总结大厂大模型应用方向高频考点：RAG核心原理、与SFT选型对比、切块与检索优化、评估指标体系、高阶纠错机制及Spring AI Alibaba工程落地方案（面试, RAG/retrieval）
- [[Loop Engineering 详解：从管理执行到设计自收敛的循环]] — 深度剖析 Loop Engineering 从一阶 AI Manager 到二阶 Senior Manager 的范式升维：将 evaluation harness、observability、SOP、maker/checker 与 data flywheel 固化为系统组件，并阐明边界约束优于 TDD 路径约束以及任务自动发现的发散性局限（AI-Agent/coding, AI-Agent/context-engineering, AI-Agent/tool-calling）
- [[再见RAG！AI知识库还得是SAG，又快又准～]] — 介绍开源检索架构 SAG（基于查询时动态超边的 SQL 检索增强生成）：将文档提炼为事项卡片与实体存入 SQL 数据库，查询时利用 SQL JOIN 动态激活局部多跳关联网，实现高召回率多跳推理、极低维护成本与确定性排障调优（RAG/retrieval, RAG/query, RAG/chunking）

- [[How_a_GPU_Actually_Works]] — 深入剖析现代 GPU 底层硬件架构（SIMT、Warp 调度、多级存储阶梯）与算力强度/Roofline 性能模型，揭示 LLM 自回归生成受限于内存带宽的根本原因，并将批处理、算子融合、SRAM 分块及量化等优化统一归纳为算存比移动法则（Infra/gpu, Infra/gpu, Infra/serving, LLM/inference）
- [[KV_Cache_Engineering_for_LLM_Serving]] — 系统性解构 LLM 推理生产中管理与压缩 KV Cache 的 12 项工程技术，涵盖模型架构共享、局部与稀疏截断、潜空间压缩、固定状态替换、数值量化、块分页、前缀复用与跨层卸载，并建立按削减目标分类的选型决策框架（LLM/inference, Infra/serving, LLM/arch/attention）

- [[A_guide_to_the_anatomy_of_effective_commerce_agents]] — Anthropic 官方电商智能体系统工程指南：深入剖析单模型 Skills 架构、Presentation Tools、Prompt Caching 与端到端/感知延迟优化，以及 Harness 硬件安全控制与快照评测实践（AI-Agent/tool-calling, AI-Agent/context-engineering, AI-Agent/UI）
- [[AI原生思维_像训练大模型一样训练自己]] — 宝玉腾讯内部分享：深度阐述找需求、判边界、最小验证与重设计的一线 AI 原生产品方法论，提出将 App 降级为 Agent 插件、开发瓶颈向代码两侧迁移，以及个体像训练大模型一样推翻旧权重持续进化（AI-Agent/coding, AI-Agent/skill）

- [[2026-09-12_4-speculative-decoding-variants_1a09737e364224e2]] — 系统解构推测解码（Speculative Decoding）四大主流变体：双模型独立草稿、EAGLE 隐层特征外推、Medusa 多头并行树状解码与 LayerSkip 浅层早退，对比其机制原理、显存开销与工程权衡（LLM/inference）
- [[2026-09-03_Attention-Mechanisms-in-LLMs,-clearly-explained_1a068e0f112668fe]] — 系统解析 LLM 注意力机制演化与 KV Cache 显存优化：涵盖 MHA、MQA、GQA、MLA 的架构压缩取舍，FlashAttention 计算访存优化，SWA 与 NSA 稀疏机制，以及 PagedAttention 与 RadixAttention 服务引擎管理（LLM/arch/attention, LLM/inference）
- [[2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201]] — 系统梳理 5 种 Embedding 向量压缩技术：PCA 投影、MRL 前缀截断、SQ 标量量化、BQ 二值量化与 PQ 乘积量化，以及 Over-fetch 粗排配合 Rescoring 精排的两阶段检索范式（RAG/embedding）

- [[2026-08-31_Sparse-random-projections_1a0580f9aa7f67f1]] — 稀疏随机投影（Sparse Random Projection）原理解析：突破 PCA 在超高维空间的三次方复杂度瓶颈，近乎保距压缩与在 VeRA 中的应用（Skill/data-analysis, DeepLearning）
- [[2026-08-31_Researchers-built-a-new-AI-inference-engine_1a0580f9aa7f67f1]] — Superlinked 开源推理服务引擎 SIE 解析：通过多模型单进程共享 GPU 与 LRU 置换机制将自托管推理成本降低约 4 倍（Infra/serving, LLM/inference）
- [[2026-08-31_WebMCP-by-Google,-clearly-explained!_1a0580f9aa7f67f1]] — Google Chrome 与 Edge 团队推出的 WebMCP 协议解析：将网站能力以类型化工具直接暴露给 Agent，对比六种 Agent 应用交互范式（AI-Agent/tool-calling, AI-Agent/UI）
- [[2026-08-13_Continuous-batching-in-LLMs_19ffcb7da4673b07]] — 解构 LLM 连续批处理的核心调度机理：迭代级调度、选择性批处理、vLLM V1 调度器四步预算算法与抢占重算治理（Infra/serving, LLM/inference）
- [[2026-08-27_KV-vs-Prefix-vs-Prompt-vs-Semantic-Caching_1a044d0b132124de]] — 系统解构 LLM 技术栈四种缓存机制（KV Cache、Prefix、Prompt、Semantic）所存底层对象、正确性影响与五大静默失效陷阱（Infra/serving, LLM/inference）

- [[阿里高德 LongHorizon-Harness 框架：使用审计状态机重构Agent执行流程]] — 阿里高德开源长时 Agent 编排框架 LongHorizon-Harness，提出 Manage-Execute-Audit（MEA）三角色循环，将长任务从会话与轨迹中心重构为经审计的环境状态转换（AI-Agent/coding, AI-Agent/context-engineering）
- [[2026-08-25_5-context-compaction-strategies-for-LLM-agents_1a03a9b5c46e28a5]] — 揭示 Agent 上下文压缩因破坏 Prefix Caching 导致成本倒挂的物理机制，系统对比 5 种上下文压缩策略与 LMCache 分层解耦复用方案（AI-Agent/context-engineering, LLM/inference）

- [[Manus团队测模型一点微小的经验]] — Manus 团队针对深度研究 (Deep Research) 场景构建的评测基准 Research Bench，提出信息量与隐喻率两大可量化信号，揭示中间过程研究笔记格式对最终信息量的关键影响并指导 Harness 迭代（AI-Agent/deep-research）
- [[模型答错事实题，先分清是没存进去，还是这次没取出来]] — Google Research 基于 WikiProfile 数据集研究发现前沿模型已将 95–98% 维基事实存入权重但闭卷提问失败率达 26–34%，系统论证存储缺失与访问受阻两种错误根因并提出四阶排查阶梯（LLM/hallucination, LLM/reasoning）

- [[Anthropic 重磅发布：AI Native 软件开发方法论]] — Anthropic 发布 AI-Native SDLC 手册，以版本控制产物驱动的闭环循环（Loop）重构软件生命周期，通过 CLAUDE.md、Skill 与 Hook 构建三层防线（AI-Agent/coding, Skill/claude-code）
- [[阿里千问 zvec-grep：让代码搜索变成 AI Agent 基础设施]] — 阿里开源 local-first 代码搜索基建 zvec-grep (zg)，以 BM25 + Vector + RRF 混合检索桥接自然语言意图与代码标识符，重构 Agent 上下文获取（AI-Agent/coding, AI-Agent/tool-calling, RAG/retrieval）

- [[搜索没有变便宜，但 Agent 把它拆成了新的供应链]] — 鸭哥深度剖析 Agent 时代 Web Search 供应链解耦为代理层、定向语义索引、上下文精炼与云端运行时四层，以及分发渠道向模型 API 运行时迁移（AI-Agent/deep-research, AI-Agent/infra, RAG/retrieval）
- [[深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]] — 鸭哥深度对比 DeepSeek DSH 命令式微内核与 Codex 声明式插件世界观，剖析 Agent Loop 插件化与自进化基础设施（RSI, AI-Agent/coding）

- [[Firecrawl 新工具开源，anydoc，将各种输入转换为md]] — Firecrawl 开源纯 Rust 多格式文档转 Markdown 工具 anydoc，中间稿两阶段解析与 Agent Skill 集成（AI-Agent/tool-calling, RAG/chunking）
- [[刚刚，DeepSeek Harness震撼开源：一切皆插件]] — DeepSeek 开源基于 Cordis 微内核的智能体框架 DeepSeek Harness，主张一切皆插件、权威 Session Log 事件源与生命周期调度管控（AI-Agent/harness, AI-Agent/coding）

- [[2026-08-05_How-to-serve-5-models-on-one-GPU_19fd38]] — 多模型 AI 流水线以统一服务层、共享 GPU 池、按需加载和成本感知分批降低闲置资源（Infra/serving, LLM/inference）
- [[2026-08-07_8-LLM-precision-formats_19fddf]] — FP32/TF32/BF16/FP16/FP8/INT8/INT4/NF4 八种 LLM 精度格式的显存、数值范围与训练推理权衡（LLM/inference, LLM/training, Infra/gpu）

- [[目标检测入门_经典模型]] — R-CNN/Fast/Faster R-CNN、YOLO、SSD 经典检测模型综述（CV/detection）
- [[目标检测入门_评测与训练技巧]] — mAP/IoU 评测指标、VOC/COCO 数据集、训练 tricks（CV/detection）
- [[目标检测入门_基础网络与分类定位权衡]] — ResNet/Xception/ResNeXt/SENet/NASNet backbone 演进与 R-FCN/DCN（CV/detection）
- [[目标检测入门_特征复用与实时性]] — FPN/TDM/DSSD/RefineDet 特征金字塔与 YOLOv2/Light-Head/SSDLite 实时检测（CV/detection）
- [[SAM_Segment_Anything模型]] — Meta AI SAM 架构/训练/Prompt 驱动分割（CV）
- [[DiT_扩散模型与Transformer]] — 用 Transformer 替换扩散模型 U-Net，缩放性与 adaLN-Zero（CV/arch）
- [[OCR的有效数据增强]] — OCR 手写识别数据增强：形态学/噪声/变换 + albumentations（CV/data-augmentation）
- [[PyTorch图像增强方法总结]] — 13 个 torchvision.transforms 增强方法附代码（CV/data-augmentation）
- [[Attention复杂度解析与改进方向]] — 自注意力复杂度、FlashAttention 1/2/3、高效注意力（LLM/arch/attention）
- [[Normalization方法总结_BN_LN_IN_GN]] — BN/LN/IN/GN 归一化方法对比（DeepLearning, 面试）
- [[DPP行列式点过程]] — DPP 多样性采样、L-Ensemble、Cholesky 贪婪算法（DeepLearning）
- [[机器学习中SVD总结]] — 特征值分解/SVD 原理、推导与应用（MachineLearning, 面试）
- [[梯度下降优化器可视化解释]] — Vanilla GD/Momentum/AdaGrad/RMSProp/Adam 对比（DeepLearning）
- [[PyTorch训练代码模板]] — PyTorch 训练 9 步模板：超参/模型/数据/训练/早停/绘图/预测（DeepLearning, Skill/python/pytorch）
- [[AI-Native的Infra演化路线L0到L5]] — AI-Native Infra 的 L0-L5 能力成熟度模型与 Result-as-a-Service（Infra/platform）
- [[入局AI_Infra系统设计与挑战]] — AI Infra vs 传统 Infra：硬件/软件/训练/推理挑战全拆解（Infra/platform）
- [[PyTorch常用代码段合集]] — PyTorch 5 大类常用代码段 + 实用 Tips（Skill/python/pytorch, DeepLearning）
- [[RL_Infra行业全景]] — RL 环境/RLaaS/数据三大模块，RL 的 GPT-3 时刻（LLM/training/RL, Infra/rl）
- [[RL环境与智能体能力金字塔]] — Surge AI 智能体能力金字塔：工具/规划/适应/接地气/常识推理（LLM/training/RL, Infra/rl）
- [[RAG基础_索引检索生成]] — RAG 基础流程：Indexing/Retrieval/Generation + LangChain/Qdrant 实现（RAG）
- [[RAG查询翻译_Query_Translation]] — Query Translation：Multi-Query/RAG Fusion/Decomposition/Step-back/HyDE（RAG, RAG/query）
- [[RAG路由_Routing]] — Routing：Logical/Semantic 路由智能选择检索路径（RAG）
- [[RAG查询构造_Query_Construction]] — Query Construction：自然语言转元数据结构化查询（RAG, RAG/query）
- [[RAG索引进阶_Indexing]] — 进阶索引：Multi-representation/RAPTOR/ColBERT（RAG, RAG/chunking）
- [[RAG文本切分_字符切分]] — 文本切分系列1：Level 1 字符切分基础 + 五层级框架（RAG, RAG/chunking）
- [[RAG文本切分_递归字符切分]] — 文本切分系列2：Level 2 递归字符分割（RAG, RAG/chunking）
- [[RAG文本切分_token优化]] — 文本切分系列2.5：递归切分的 token 优化（RAG, RAG/chunking）
- [[RAG文本切分_JSON文档切分]] — 文本切分系列3：Level 3 JSON 文档结构切分（RAG, RAG/chunking）
- [[RAG文本切分_语义切分]] — 文本切分系列4：Level 4 基于向量模型的语义切分（RAG, RAG/chunking）
- [[RAG高级优化_问题生成检索增强]] — 基于问题生成丰富文本片段提高检索准确性（RAG, RAG/query）
- [[RAG高级优化_检索策略Fusion_HyDE]] — Fusion/HyDE 多路检索策略实战（RAG, RAG/retrieval）
- [[RAG高级优化_检索后处理]] — 检索后处理：压缩/重排/Long-text Reorder（RAG, RAG/retrieval）
- [[RAG高级优化_query转换之路]] — query 转换全景：重写/HyDE/子查询/Step-back（RAG, RAG/query）
- [[RAG文本切分_Markdown切分]] — Markdown 标题切分定制化方案（RAG, RAG/chunking）
- [[MRL_俄罗斯套娃表示学习]] — MRL 俄罗斯套娃嵌入技术，截断嵌入维度保留语义（RAG/embedding）
- [[Matryoshka嵌入模型概述_HuggingFace]] — HuggingFace MRL 训练原理、Sentence Transformers 实现与性能实验（RAG/embedding）
- [[从BM25到Multi-Vector_6种Embedding演进路线]] — Sparse/Dense/Quantized/Binary/Matryoshka/Multi-Vector 六种嵌入方案对比选型（RAG/embedding, RAG）
- [[一文详尽之Embedding]] — Embedding 全景综述：One-Hot 到 SimCSE，BERT 各向异性问题与优化（RAG/embedding）
- [[为什么用Qwen3_embedding和rerank]] — Qwen3 Embedding/Rerank 原理：[EOS] 池化、Instruct 机制、LLM 化重排（RAG/embedding, RAG）
- [[ColBERT原理与延迟交互机制]] — ColBERT 多向量表示、延迟交互(MaxSim)与稠密向量对比，BGE-M3 实验（RAG/embedding, RAG）
- [[ColBERTv2残差压缩演进]] — 早期/延迟交互、ColBERT→ColBERTv2 残差压缩(聚类+量化)，BGE-M3 4x 压缩实验（RAG/embedding, RAG）
- [[ES企业AI搜索实践]] — Elasticsearch 向量搜索/混合检索/RRF/量化/Serverless 构建企业 RAG（RAG）
- [[向量数据库原理与应用全解析]] — 向量化演进、索引方法、相似度度量、主流向量数据库对比（RAG/embedding）
- [[RAG_12痛点与解决方案]] — 12 个 RAG 痛点及解决方案：重排序/Prompt压缩/查询转换/PDF提取/安全（RAG）
- [[斯坦福RAG新基线_DOS_RAG]] — DOS RAG：检索后按原文顺序排列，持平或超越 RAPTOR/ReadAgent（RAG）
- [[DMQR-RAG_多样查询改写]] — DMQR-RAG 四种改写策略 + 自适应选择，P@5 提升 14.46%（RAG, RAG/query）
- [[RAG挑战赛冠军方案]] — 企业年报 RAG 冠军：Docling 解析/FAISS/LLM重排序/多路由器/CoT+SO（RAG）
- [[提升RAG问答质量的技术路线]] — RAG 技术路线总览：Query Translation/Routing/Construction/Indexing/CRAG/Self-RAG（RAG）
- [[美团搜索查询改写实践]] — 美团查询改写全栈：离线挖掘/BERT判别/SMT/NMT强化学习/向量化召回（RAG/query）
- [[优图RAG技术详解]] — 腾讯优图RAG全栈：2B Embedding/Reranker蒸馏/Text2SQL/GraphRAG知识树（RAG）
- [[RAG检索_Retrieval入门到精通]] — RAG系列6：Re-Rank/CRAG/Self-RAG 检索优化（RAG, RAG/retrieval）
- [[RAG系统设计_语义搜索与KG驱动选型]] — 语义搜索本质/Loss/距离/Embedding/向量库选型 + KG-RAG/Lazy Graph RAG（RAG/embedding, RAG）
- [[TableRAG_文本表格异构问答]] — 华为云 TableRAG：文本检索+SQL 混合推理，HeteQA 评测集（RAG）
- [[跨模态知识联邦与统一语义推理RAG]] — 枫清科技融合知识库+统一知识图谱处理异构知识（RAG）
- [[RAGAS评估RAG系统]] — RAGAS 框架五大核心指标科学评估 RAG 系统（RAG/eval）
- [[腾讯查询优化四大类综述]] — 腾讯 QO 综述：查询扩展/分解/消歧/抽象四大类（RAG, RAG/query）
- [[RAG技巧与底层代码剖析]] — 阿里云开发者：用 Python 基础库从零手撕 RAG 内核，含 10 大实战技巧（RAG）
- [[OpenAI_LLM应用最佳实践]] — OpenAI DevDay 2023：Prompt Engineering/RAG/Fine-tuning 两轴优化路线图（LLM）
- [[A_Visual_Guide_to_Mamba_and_SSM]] — 50+ 可视化图解 Mamba/SSM 全流程：数学基础/离散化/选择扫描/硬件感知（LLM/arch/Mamba）
- [[Mamba_Explained_Kola_Ayonrinde]] — Mamba 直觉讲解：效率/有效性权衡、选择机制类比、State Swapping 范式（LLM/arch/Mamba）
- [[一文读懂Mamba_知乎]] — 中文解析 Mamba 论文：选择机制动机、作者背景（Albert Gu / Tri Dao）（LLM/arch/Mamba）
- [[Transformer被挑战_Mamba解析与PyTorch复现]] — Mamba 架构解析 + 完整 PyTorch 复现：S6/MambaBlock/RMSNorm/enwiki8 训练（LLM/arch/Mamba）
- [[Mamba2_SSD_大一统]] — Mamba2 SSD 框架：SSM 与 Attention 等价、半可分离矩阵、8倍推理加速（LLM/arch/Mamba）
- [[腾讯混元TurboS技术报告]] — 560B Hybrid Transformer-Mamba MoE 模型，业界首个大规模部署 Mamba 架构，自适应长短 CoT（LLM/arch/Mamba, LLM/arch/MoE）
- [[大模型面试面经_简单透彻理解MoE]] — MoE 结构原理、Router 机制、优缺点、PyTorch 示例代码（LLM/arch/MoE）
- [[手把手教你实现稀疏MoE语言模型]] — 从零 PyTorch 实现稀疏 MoE：Top-k/噪声 Top-k 门控、SparseMoE、完整训练循环（LLM/arch/MoE）
- [[从DeepSeek-V3到Kimi_K2_八种现代LLM架构大比较]] — Sebastian Raschka 对比 8 种 2025 LLM 架构：MLA/MoE/滑动窗口/Post-Norm/NoPE/Muon（LLM/arch）
- [[2025年七大顶流大模型架构]] — 7 大旗舰开源 LLM 架构创新点综述（LLM/arch, LLM/arch/MoE）
- [[从LLaVA到Qwen3-VL_多模态架构演进]] — LLaVA AnyRes vs Qwen3-VL DeepStack，MLLM 两大演进路线全景（LLM/arch/VLM）
- [[DeepSeek_MLA矩阵吸收原理]] — MLA 矩阵吸收图解：K/V 升维矩阵吸收进 Q，三处广播优化（LLM/arch/attention）
- [[KV_Cache原理图解]] — KV Cache 图解：自回归推理缓存 K/V，显存估算，仅适用 Decoder（LLM/inference/kv-cache）
- [[推测解码Speculative_Decoding综述]] — Draft-then-Verify 无损推理加速：Independent/Self Drafting + 验证策略（LLM/inference）
- [[大模型显存占用单卡分析]] — 混合精度训练/KV Cache/LoRA/QLoRA 四场景单卡显存估算公式（LLM/inference, Infra/gpu, 面试）
- [[自适应快慢思考推理模型]] — Qwen3 SFT混合思考、字节AdaCoT Pareto-PPO、清华AdaThinking约束优化三路方案（LLM/reasoning）
- [[DeepSeek-R1工作原理]] — DeepSeek-R1 GRPO+多阶段训练管道，达到 o1-1217 水平（LLM/reasoning, LLM/training/RL）
- [[R1复现认知与误区]] — 一线视角：复现 R1 四大关键（基模/数据/infra/超参）与四大误区（LLM/reasoning, LLM/training/RL）
- [[强化学习入门指南_RLHF到GRPO]] — Unsloth：RLHF→PPO→GRPO→RLVR 原理+奖励函数设计+实战技巧（LLM/training/RL）
- [[LoRA微调实战_Qwen2.5全流程]] — LoRA 低成本微调 Qwen2.5-0.5B 实战：数据/代码/超参/CPU 跑通全流程（LLM/training/post-train）
- [[大规模神经网络优化_超参实践与规模律]] — GPT→LLaMA2 超参演进 + Kaplan/Chinchilla 规模律推导与拾遗（LLM/training）
- [[翁荔_LLM外在幻觉_原因检测抵抗]] — 翁荔 Blog：外在幻觉定义、产幻原因、FActScore/SAFE/CoVe/FLAME 检测与抵抗（LLM/hallucination）
- [[LLM_32种消除幻觉技术综述]] — 32 种幻觉消除技术：提示工程（RAG/反馈/提示微调）与模型开发（解码/KG/损失/SFT）（LLM/hallucination）
- [[大模型幻觉陷阱_AGI之路04期]] — 技术/传播/治理三维解构幻觉本质：长尾压缩→编造、专家之死、对齐税与责任归属（LLM/hallucination）
- [[Discrete_Tokenization多模态综述]] — 首个多模态LLM离散化综述：8类VQ方法（VQ/RVQ/FSQ/LFQ等）、码本坍塌与跨模态全景（LLM/tokenization）
- [[Transformer大模型3D可视化_NanoGPT]] — Brendan Bycroft 3D可视化逐层拆解 GPT-3/NanoGPT：Embedding/LN/Attention/MLP/Softmax（LLM/arch）
- [[LLM面试50题_MIT_CSAIL]] — MIT CSAIL 工程师 Hao Hoang 整理的 50 个 LLM 核心面试题（LLM, 面试）
- [[大模型算法岗面试百问百答]] — 大模型算法岗面试知识点：RAG 体系/LLaMA 架构/SFT 方法/幻觉复读机（LLM, 面试）
- [[Jina_AI创业复盘]] — Jina AI 创始人肖涵六年复盘：两次 Pivot、AI 团队 Scaling Law 困惑、被 Elastic 收购（创业）
- [[淘宝直播数字人_LLM文案生成技术]] — 淘宝直播数字人口语化改写(DPO 97%)、多源信息单步蒸馏、素材图文一致（LLM, LLM/arch/VLM）
- [[别再误会MCP了辟谣指南]] — 阿里云工程师以 SDK 源码法证 MCP CHS 三组件，Host 是 AI 智能唯一承载者（AI-Agent/tool-calling）
- [[MCP遇上代码执行]] — Anthropic：CodeAgent 模式调用 MCP，Token 减少 98.7%，隐私保护与 Skills 沉淀（AI-Agent/tool-calling）
- [[MCP五大原语与Web化]] — MCP 联合创建者 David 解构五大原语，Web 化方向 OAuth 2.1 + Streamable HTTP（AI-Agent/tool-calling）
- [[HumanInTheLoop用MCP实现]] — 阿里云 OpenLM：send_inquiry+MCP Notification 实现服务端 HITL，含 Proxy 代理和 YOLO 模式（AI-Agent/tool-calling）
- [[Context_Engineering_LangChain_Manus_NotebookLM]] — LangChain × Manus 对话提炼：4条反直觉原则——战略边界/可逆压缩/工具分层卸载/简化优先（AI-Agent/context-engineering）
- [[AI应用实战_搞定复杂指令和工具膨胀]] — 阿里云联调造数：单Agent→多Agent，意图识别+工具引擎+逆向推导，工具100+→5个（AI-Agent/context-engineering）
- [[Manus创始人手把手拆解上下文工程]] — Peak 亲写：KV缓存/工具掩码/文件系统记忆/注意力复述/错误保留/Few-Shot多样性六大原则（AI-Agent/context-engineering）
- [[浅谈上下文工程_Claude_Code_Manus_Kiro]] — 提示工程→上下文工程→环境工程演进，Claude Code/Manus/Kiro三产品实践对比（AI-Agent/context-engineering）
- [[也许当前最好的上下文工程讲解_LangChain联合Manus]] — Lance Martin × Peak Ji 对话实录：压缩/总结两模式、隔离两模式、三层行动空间、避免过度工程化（AI-Agent/context-engineering）
- [[Anthropic再发Agent神文_像人类工程师一样思考解决长程任务难题]] — Anthropic 双 Agent 架构解决长程 Coding 任务：初始化 Agent + 编码 Agent + 功能列表/增量进展/端到端测试三支柱（AI-Agent/coding）
- [[一个半月高强度Claude_Code使用后感受]] — 王巍（喵神）：持续使用 Claude Code 的深度体验，心智模型转换与编程效率加速（Skill/claude-code）
- [[写好CLAUDE.md_HumanLayer最佳实践]] — HumanLayer 团队编写 CLAUDE.md 最佳实践，基于上下文工程原则与模块化约束（Skill/claude-code）
- [[Claude_Agent_Skills_从第一性原理深入剖析]] — PaperAgent：Skills 元工具架构速览，SKILL.md 结构、四种模式、纯 LLM 推理技能选择（AI-Agent/skill）
- [[从第一性原理深度拆解_Claude_Agent_Skill_宝玉]] — Han Lee/宝玉：源码级解构 Skills 双消息注入、isMeta 机制、contextModifier 执行上下文修改全生命周期（AI-Agent/skill）
- [[Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降]] — 提出语义早停方法，通过余弦距离收敛判断 Agent Loop 终止，替代硬迭代上限，节省 38% Token 且保证质量（AI-Agent/loop-engineering, AI-Agent/coding）
- [[Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝]] — 解析 Anthropic 官方 13 个领域知识插件，将 CLAUDE.md 等静态规范转化为动态运行时检查与分阶段引导（AI-Agent/skill, AI-Agent/coding）
- [[从提示员到系统架构师：Loop Engineering 的范式跃迁]] — 剖析从 Prompt 到 Loop 工程的四层抽象跃迁，工程师从与 AI 逐轮对话的操作员转变为设计自主循环的架构师（AI-Agent/loop-engineering, AI-Agent/coding）
- [[实测腾讯开源的 BrowserSkill：让 AI 直接用你登录好的浏览器]] — 评测腾讯开源 BrowserSkill CLI，复用日常真实浏览器与登录态进行 Agent 自动化操作，纯本地不隔离（AI-Agent/tool-calling, AI-Agent/skill）
- [[DeepResearch的概念、核心挑战与进化路径]] — 华为/利物浦/牛津综述：DR Agent 定义、四大核心挑战与未来进化路径（AI-Agent/deep-research）
- [[Tongyi DeepResearch的技术报告探秘]] — 魔搭社区解读：通义 DeepResearch 三阶段训练、IterResearch 范式、WebFrontier 数据合成与六大研发问题（AI-Agent/deep-research）
- [[一篇95页最新80种Deep Research系统全面综述]] — 浙大综述 80+ 系统，4 维分类法与单体/流水线/多智能体/混合四种架构（AI-Agent/deep-research）
- [[通义 DeepResearch：开源 AI 智能体的新纪元]] — 通义官方博客：全开源 Web Agent 完整技术全貌，Agentic CPT+SFT+RL 端到端训练与 Research-Synthesis 框架（AI-Agent/deep-research）
- [[AI智能体8种Memory策略与技术实现]] — 8 种记忆策略原理+模拟代码：全量/滑动窗口/相关性过滤/摘要/向量DB/知识图谱/分层/类OS内存管理（AI-Agent/memory）
- [[OpenAI_构建AI智能体实用指南]] — OpenAI 官方指南（宝玉译）：Agent 三大基石/单一+主管+去中心化编排/分层安全护栏/HITL（AI-Agent/multi-agent）
- [[用系统架构思维告别意大利面条式系统提示词]] — 系统提示词四层架构（核心定义/交互接口/内部处理/全局约束）替代扁平规则堆砌（AI-Agent/prompt-engineering）
- [[腾讯OlaChat_LLM智能数据分析平台实践]] — 腾讯 OlaChat：FlattenedRAG/StructuredRAG 元数据检索 + Text2SQL 微调+Agent + 多任务对话编排（AI-Agent/AI-BI）
- [[腾讯ABI工程架构探索与实践]] — OlaChat 工程架构：原子 Agent + DAG 编排 + 统一协议 + Text2DSL 中间层方案（AI-Agent/AI-BI）
- [[AI_Agent与AI_Workflow的区别和深度解析]] — AI Agent 自主决策 vs AI Workflow 预定义流程：四类 Agent + 五大 Workflow 优势（AI-Agent）
- [[Agent系统开发经验]] — 三种复杂性幻觉+三层复杂度（可运行/可复现/可进化）+LLM放大效应+系统化工程原则（AI-Agent）
- [[企业落地NL2SQL_AI-ready_data与小模型]] — NL2SQL生产落地：AI-ready data + 小模型（3B/7B LoRA）+ 两级Schema Linking，幻觉率7.9%→1.3%（AI-Agent/AI-BI）
- [[FastAPI架构指南_项目模板与实战经验]] — 生产级 FastAPI 项目结构：Routers/Schemas/Services 三层分离 + 安全中间件 + Makefile（Skill/python）
- [[Python并发_async_await与FastAPI]] — FastAPI 官方文档：async/await 协程、并发 vs 并行、路径函数 def/async def 选择（Skill/python）
- [[Docker化Flask_Django应用从pip切换到uv]] — Nick Janetakis：Docker 项目 pip→uv，约 10x 提速，pyproject.toml/uv.lock/非 root（Skill/python）
- [[加速Python循环的12种方法]] — 12 种 for 循环优化：map 970x/set 498x/filterfalse 131x/lru_cache 57x（Skill/python）
- [[五个鲜为人知的Python功能]] — contextlib.suppress/setrecursionlimit/typing.Literal/__missing__/__subclasshook__（Skill/python）
- [[自动探索性数据分析EDA_10个Python包]] — D-Tale/Pandas-Profiling/Sweetviz/AutoViz/Dataprep 等 10 个自动 EDA 包对比与选型（Skill/python, Skill/data-analysis）
- [[Pandas一行代码绘制25种美图]] — DataFrame.plot/Series.plot 一行代码绘制 25 种图表（Skill/data-analysis）
- [[超强图解Pandas操作大全]] — 图解 Pandas 核心操作：排序/分组/连接/透视/索引（Skill/data-analysis, 面试）
- [[图解Pandas常用操作_NumPy对比与进阶]] — Pandas Illustrated 翻译：NumPy 对比/Series/DataFrame/MultiIndex 四部分（Skill/data-analysis, Skill/python, 面试）
- [[一行代码让matplotlib图表变高大上]] — dufte 库三个 API 自动美化 matplotlib 图表样式（Skill/data-analysis）
- [[600条Linux命令速查手册]] — 28 大类约 600 条 Linux 命令分场景速查手册（Skill/linux）
- [[现代打工人如何获得幸福]] — 评论尸：时间度量衡/幸福积分模型/天职/逃离职场PUA五种思维（Life）
- [[Gemini的PPT生成技巧与模板提示词]] — Gemini APP PPT 生成能力使用技巧与五套百搭风格提示词（AIGC）
- [[九大主流AI_PPT横测]] — 九大 AI PPT 工具横测：AI原生派vs传统革新派，最后一公里难题（AIGC）
- [[一套提示词实现封面自由]] — 模块化封面生成提示词：小红书/公众号封面+十套风格，DeepSeek V3 也能用（AIGC）
- [[Nano-Banana_Pro论文绘图教程]] — 「架构师→渲染器→编辑器」三步工作流，VISUAL SCHEMA 驱动 Gemini 2.5 Flash Image 生成 CVPR/NeurIPS 学术插图（AIGC）
- [[关于Nano_Banana的一些浅思]] — Gemini 2.5 Flash Image 功能/提示词模板全解析+普通人与大模型协作哲学/Vibe Coding 三阶段实践（AIGC）
- [[超详细提示词教程_玩转Wan2.2]] — 通义万相 2.2 文生视频提示词完整词典：基础/进阶/图生视频公式 + 9大维度美学控制（AIGC）
- [[淘宝直播数字人_TTS语音合成技术]] — 淘天直播 AIGC 团队：TTS 数据管线 + V1→V4 四代模型演进（CosyVoice2+vLLM）（TTS）
- [[Foundation_Sprint产品验证完全指南]] — 谷歌 Jake Knapp 的 Foundation Sprint：10 小时奠定战略基础，基础/差异化2x2/Magic Lenses 三阶段 + 创始假设（创业）
- [[Superhuman_PMF引擎方法论]] — Superhuman 把 PMF 量化为可优化指标的四步引擎，22%→58%，ARR 3500 万美元（创业）
- [[Bundle_Unbundle视角看AI时代机会]] — 42章经：Grammarly 案例 + Shishir Bundle 理论(MCC/2x2) + 集装箱历史类比 AI（创业）
- [[100家顶尖AI初创公司的7个真相]] — Leonis AI 100：高人效/倒漏斗GTM/多赢家/快速转型/阈值解锁/收入激增/研究型创始人（创业）
- [[50年旅行经验之谈_Kevin_Kelly]] — Kevin Kelly 53 年旅行经验：Retreat/Engage 两模式 + Laser-Back 直达返回法 + 大量实操 tips（Life）
- [[初入投资容易犯的错误]] — laike9m：选错市场/一开始重仓/风格横跳三大错误 + 除以十/3-6月试错/固定1-2模式框架（Life）
- [[什么是真正有效的驱蚊产品]] — 少数派：DEET/Picaridin/IR3535/OLE 四成分 + 浓度影响时长 + 安全性建议（Life）
- [[中枢与网关使用指南]] — 米家智能家居：网关/中枢系统/主备中枢/从网关/盲网关概念体系（Life）
- [[AI时代如何做独立开发]] — 艾逗笔：一年十款产品的五条感悟 + 出海 SOP/SEO/AI Wrapper + AI Coding/Agent/Infra/MCP 四方向（创业）

- [[四段核心Prompt提示词实战指南]] — 收录并深度拆解四段极具实战价值的高阶结构化提示词（Prompt），涵盖 PPT、前端网页设计与 3D 动画规划（AI-Agent/prompt-engineering, AIGC）
- [[小红书精准运营与数据复盘实战]] — 详解自媒体小红书平台精准内容运营法则，通过关键数据指标（CTR/完播率/互动率）复盘优化选题模型（创业）
- [[全流程备战面试开卷推理SOP]] — 少数派文章：提出将职场面试视为基于样本积累与反向推导的“开卷推理游戏”，构建结构化面试备战与复盘 SOP（面试, Life）
- [[Google_Generative_UI综述]] — Google Research 官方博客关于生成式用户界面（Generative UI）的阐述，按提示词动态生成丰富的定制化交互组件（AI-Agent/UI, AI-Agent/coding）
- [[FastAPI生产部署ASGI_WSGI避坑指南]] — 生产环境下部署 FastAPI 高并发服务的实践指南，对比 Uvicorn 与 Gunicorn 架构职责并给出 Docker 稳定调优配置（Skill/python）
- [[Anthropic多智能体研究系统构建]] — 深入解析 Anthropic 构建 Claude 生产级多智能体研究系统的工程挑战与经验，涵盖编排器-工作者架构、并行推理及长跨度状态管理（AI-Agent/multi-agent, AI-Agent/deep-research）
- [[GPT5通用验证器与RL探索]] — 深度解析 LLM 从 RLVR 向开放主观领域进化的核心关键“通用验证器”，详细剖析 RaR、Rubicon、VeriFree 及终极 OaK 架构六大技术路径（LLM, LLM/training/RL）
- [[大模型显存计算公式与优化]] — 系统梳理 Transformer 大模型在训练与推理场景下的显存消耗公式，深入探讨 3D 并行、重计算及 ZeRO 优化显存核心路径（LLM/inference, Infra/gpu）
- [[Claude Code与Obsidian飞书知识库搭建实践]] — 基于 Karpathy 的 LLM Wiki 理念，结合 Claude Code（大脑）、Obsidian（眼睛）与飞书机器人（手），实现知识库入库与复利积累（Skill/knowledge-bank, AI-Agent/coding）
- [[LLM Agent记忆进化路径三阶段研究综述]] — 港中深与上海 AI 实验室综述，提出 Storage -> Reflection -> Experience 三阶段演进框架及主动探索机制（AI-Agent/memory）
- [[Dropbox基于DSPy优化Dash Chat评估与提示词]] — Dropbox Dash Chat 评估驱动实践：人工标注校准 LLM-as-a-Judge + DSPy GEPA 自动迭代系统提示词（AI-Agent/eval, AI-Agent/prompt-engineering）
- [[MiniMax_vs_Kimi_注意力路线之争]] — MiniMax M2 回归 Full Attention，Kimi 发布开源混合注意力模型 Kimi Linear（KDA+MLA 3:1），两条技术路线的工程视角对比（LLM/arch/attention）
- [[后训练认知_SFT_vs_RL_记忆与遗忘机制]] — 普林斯顿陈丹琦团队发现 RL 抗遗忘优于 SFT，根源在于 on-policy 数据分布，而非算法形式（LLM/training/post-train）
- [[2026程序员必读的向量数据库原理与选型指南]] — 系统剖析 ANN 算法（HNSW/IVF/DiskANN）与标量过滤，横向对比 8 大向量数据库选型决策树（RAG/embedding, Infra/storage）
- [[Karpathy推文引发的LLM_Wiki知识库搭建实践]] — Andrej Karpathy 提出的 LLM Wiki 知识编译范式、三层架构、四大核心操作与 80 年思想谱系（Skill/knowledge-bank, AI-Agent/coding）
- [[OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]] — Lilian Weng 剖析 Harness Engineering：递归自我改进（RSI）近期的近路不是改模型权重，而是围绕模型搭建的 Harness 系统（RSI, AI-Agent/coding）
- [[wiki/sources/Vault死链治理与单向推导架构维护复盘]] — Hugo Yang 总结 Obsidian 知识库死链假性鉴别（重定向/去前缀/待建节点）、级联清理行内安全感知与单向推导管线维护纪律（Skill/knowledge-bank）
- [[XGBoost_SHAP一键生成10张出版级模型解释图]] — 利用 XGBoost 与 SHAP 构建 10 张高分辨率出版级可视化图表（MachineLearning, Skill/data-analysis, Skill/python）
- [[不用title你怎么介绍自己]] — 反思职业 Title 与 Ego 绑定，用动词定义自己与探索核心问题（Life）
- [[代码强化学习的双刃剑_前沿模型为何集体走向作弊]] — 解析代码 RL 可验证奖励如何激活推理元能力，又因代理奖励漏洞导致模型集群发生 Reward Hacking 作弊现象及防范（LLM/training/RL, LLM/reasoning）
- [[如何系统评价一个_Agent_Skill]] — 系统拆解 Agent Skill 的六大评估维度（触发、轨迹、产物、效率、安全、复用）与对比实验设计范式（AI-Agent/skill, AI-Agent/eval）
- [[DeepSeek Agent开发岗三面，再面一轮就offer啦！！！]] — Agent 开发岗面试复盘：私人助理架构、幻觉与代码安全、记忆、评测闭环及 RAG 优化（AI-Agent/coding, AI-Agent/eval, 面试）
- [[快手data agent一面，我裂开了！！！]] — Data Agent 面试复盘：工具、记忆、ReAct、权限重试、循环控制与 Subagent 设计（AI-Agent/coding, AI-Agent/context-engineering, 面试）
- [[月之暗面 Agent开发岗，凉凉！！！]] — Agent 面试复盘：上下文摘要触发、长期记忆召回、工具渐进披露与 RAG 可观测性（AI-Agent/memory, AI-Agent/context-engineering, 面试）
- [[高德地图AI应用开发岗一面，我跪了！！！]] — AI 应用面试复盘：多轮 RAG、RRF、粗排精排、结构切分、记忆冲突与 Agent Loop（RAG/retrieval, RAG/chunking, 面试）
- [[美团AICoding面试，跪了！！！]] — AI Coding 面试复盘：将高风险评论审核拆为规则、输入输出、权限和测试四层系统（AI-Agent/coding, AI-Agent/eval, 面试）
- [[DeepSeek AI Infra 一面，面爽了！！！]] — DeepSeek AI Infra 面试复盘：Harness 插件哲学、早停与防震荡机制、工具沙箱、大小模型协同及多 Agent 协作平台（Infra/platform, AI-Agent/coding, 面试）
- [[美团AI全栈Agent一面，笑着聊完挂了！！！]] — 美团 AI 全栈 Agent 面试复盘：行程规划工具编排、多轮澄清、Query 改写、Schema 校验、记忆压缩、分布式锁与并发终止（AI-Agent/coding, AI-Agent/tool-calling, 面试）
- [[读：读代码前先跑的五个 git 命令 - 暗无天日]] — 用 Git 历史识别变更热点、关键维护者、缺陷聚集、提交趋势和救火信号（Skill/linux, AI-Agent/coding）
- [[2025-01-31_7-Uses-of-Underscore-in-Python_194be0]] — 本文介绍了 Python 中下划线（_）的 7 种主要使用场景，包括获取最后计算值、循环占位符、大数字分隔符以及四种用于命名对象的下划线规范（单前导、单后缀、双前导和双前后导）。（python, python/syntax）
- [[2025-02-03_4-ways-to-test-ML-models-in-production_194cd4]] — 本文介绍了在生产环境中测试机器学习模型的 4 种经典方法，即 A/B 测试、金丝雀测试、交叉测试（Interleaved）以及影子测试（Shadow），并在其扩展阅读中提及了多臂强盗部署（MAB）。（machinelearning, MLOps, modeltesting）
- [[2025-04-23_11-Types-of-Variables-in-a-Dataset_196640]] — 介绍了数据集中常见的 11 种变量类型及其定义与应用场景，包括自变量、因变量、混杂变量、控制变量、潜变量、交互变量、平稳/非平稳变量、滞后变量和泄露变量。（data-science, statistics, variable-types）
- [[2025-05-07_Memory-Pinning-to-accelerate-model-training_196ac3]] — 介绍了在 PyTorch 中使用固定内存（Memory Pinning）技术来加速 CPU-GPU 数据传输的原理和配置方法，通过 pin_memory=True 和 non_blocking=True 实现 CPU 和 GPU 的异步并行工作。（deep-learning, pytorch, performance-optimization, memory-management）
- [[2025-05-29_5-chunking-strategies-for-RAG_1971dc]] — 本文介绍了在构建 RAG 系统时常用的五种文本切分（chunking）策略，包括固定大小切分、语义切分、递归切分、基于文档结构的切分以及基于 LLM 的切分，并对比了各自的优缺点和适用场景。（RAG, chunking, textsplitting）
- [[2025-06-27_15-techniques-to-optimize-neural-network-training_197b30]] — 本文总结了15种神经网络训练优化技术，包括使用高效优化器、最大化Batch Size、贝叶斯超参搜索、混合精度训练、He/Xavier初始化、多GPU并行训练、大模型专用库、 activation checkpointing（激活值重计算）、在GPU上进行数据归一化、梯度累积以及DataLoader优化（max_workers和pin_memory）等。（deeplearning, neuralnetwork, optimization, training）
- [[2025-06-30_4-strategies-for-multi-GPU-training_197c27]] — 介绍多 GPU 模型训练的四种核心并行化策略：模型并行、张量并行、数据并行和流水线并行，并说明其优势与局限。（LLM/training, GPU/parallelism）
- [[2025-07-01_Accelerate-tSNE-with-GPU_197c7a]] — 讨论 t-SNE 降维算法在处理大规模数据集时的二次方复杂度瓶颈，并介绍 GPU 加送库 tSNE-CUDA 带来的巨大性能提升（达 700x 速度）及仅支持 2D 投影的限制。（ML/dimension-reduction, GPU/acceleration, t-SNE）
- [[2025-07-01_Full-global-attention-vs-alternating-attention_197c7a]] — 介绍了 ModernBERT 如何通过交替注意力（Alternating Attention，每三层全局注意力，其余层 128 tokens 的滑动窗口局部注意力）来打破传统 BERT 全局注意力二次方复杂度瓶颈，提升内存效率与长序列处理能力。（modernbert, attentionmechanism, deeplearning）
- [[2025-08-25_Building-pairwise-sentence-scoring-systems_198e2e]] — 探讨了成对句子评分（Pairwise Sentence Scoring）作为现实世界中 RAG 检索、问答系统、信息检索、去重引擎等应用的基础定位，引入了双编码器和交叉编码器等核心 SOTA 方法。（sentencesimilarity, biencoder, crossencoder, nlp）
- [[2025-08-25_PyTorch-Dataloader-has-two-terrible-default-settings_198e2e]] — 介绍 PyTorch 中 DataLoader 的默认设置问题（导致 CPU 和 GPU 串行等待），并阐述如何通过启用固定内存 (pin_memory=True)、多进程加载以及非阻塞传输 (non_blocking=True) 来实现 CPU-GPU 的异步流水线优化，在 MNIST 数据集上实现 4.7 倍的加速。（deeplearning, pytorch, performancetuning, dataloader, memorypinning）
- [[2025-08-30_Simplify-Python-imports-with-explicit-packaging_198fc6]] — 探讨 Python 项目中显式包管理机制。虽然 Python 3.3+ 引入了隐式命名空间包，但显式使用 __init__.py 能够明确包的导出接口、简化外部导入路径并避免冗余导入，是优化工程设计的最佳实践。（python, engineeringpractices, moduleandpackage）
- [[2025-09-16_Clustering-evaluation-without-labels_199543]] — 介绍在无标签情况下评估聚类质量的三种常用指标：轮廓系数（Silhouette Coefficient）、CH指数（Calinski-Harabasz Index）以及基于密度的聚类验证（DBCV），并对比了它们各自的计算开销与适用场景。（machinelearning, clustering, evaluation, unsupervisedlearning）
- [[2025-10-18_A-subtle-neural-network-optimization-technique_199f91]] — 讨论神经网络训练中的一个细微优化技巧：在图像分类等任务中，将数据归一化（如从 8-bit 整数转为 32-bit 浮点数）的时机放在数据传输到 GPU 之后，以减少 CPU 到 GPU 的数据搬运量，从而提高训练效率。（deeplearning, neuralnetwork, optimization, gpu, datatransfer）
- [[2025-10-18_Avoid-Using-PCA-for-Visualization-Unless..._199f91]] — 探讨主成分分析（PCA）用于数据可视化时的局限性，并介绍如何通过累计解释方差（CEV）曲线来验证 2D PCA 可视化的可信度，最后指出 t-SNE、UMAP 等专用算法更适合高维数据的可视化任务。（machinelearning, dimensionalityreduction, datavisualization）
- [[2025-10-24_Top-Gradient-Boosting-Methods_19a177]] — 全面梳理了四大主流梯度提升树模型（XGBoost、CatBoost、LightGBM、NGBoost）的原理、独特创新点（树生长策略、特征处理方式、分层采样机制、概率预测）及选型逻辑，并提供了相关的顶级学术论文引用。（machinelearning, ensemblelearning, gbdt）
- [[2025-10-27_ANN-search-using-inverted-file-index_19a274]] — 介绍了在向量检索中使用倒排文件索引 (IVF) 进行近似最近邻 (ANN) 搜索的原理。相比暴力搜索 kNN 的 O(ND) 复杂度，IVF 通过 k-means 聚类建立质心到分区的映射，将搜索复杂度降低到 O(KD + ND/K)，大幅度缩减耗时（N=10M，K=100 时可实现近 100 倍加速），同时客观阐述了其以精度折中换取低延迟的机制。（vector-database, vector-search, approximate-nearest-neighbor, indexing）
- [[2025-11-12_25-most-important-mathematical-definitions-in-DS_19a79c]] — 汇总了数据科学中 25 个最核心的数学定义与公式，并对极大似然估计 (MLE)、标准分数 (Z-score)、最小二乘法 (OLS)、熵 (Entropy)、特征值与特征向量、R方系数 (R-squared)、KL散度、奇异值分解 (SVD) 以及拉格朗日乘子法进行了重点释义和应用场景关联。（data-science, mathematics, statistics, machine-learning）
- [[2025-11-20_Descriptors-in-Python_19aa2d]] — 探讨 Python 中的描述符（Descriptors）机制。介绍描述符如何解决传统 @property getter/setter 机制在多属性校验时的冗余以及无法在构造时拦截的问题，并对描述符的三个核心魔术方法进行了原理解析。（python, oop, descriptor）
- [[2025-11-20_Should-you-gather-more-data_19aa2d]] — 探讨如何通过绘制学习曲线（Learning Curve）来评估是否需要收集更多训练数据。介绍了将数据集划分为多个等分并累加训练来测定模型表现的方法，并详细阐述了未饱和曲线与已饱和曲线的物理意义。（machinelearning, modeldiagnostics, learningcurve, datacollection）
- [[2025-11-28_How-to-use-kNNs-for-imbalanced-datasets_19acc3]] — 探讨了 kNN 算法在不平衡数据集上的局限性，并详细介绍了两种改进方案：距离权重 kNN（在 sklearn 中配置 weights='distance'）和动态调整超参数 k 的算法。（machinelearning, knn, imbalanceddata）
- [[2025-11-28_Two-techniques-to-extend-the-context-length-of-LLMs_19acc3]] — 探讨了扩展大语言模型（LLM）上下文长度面临的二次方复杂度瓶颈，并详细介绍了两种主流优化技术：近似计算的稀疏注意力（Sparse Attention）和优化 GPU 显存数据流搬运的 Flash Attention，同时指出选择合适位置编码（如 RoPE）在长上下文理解中的关键作用。（deeplearning, llm, attentionmechanism, flashattention, sparseattention）
- [[2025-12-02_7-categorical-data-encoding-techniques_19ae0c]] — 介绍了 7 种常见的类别型数据编码技术（One-Hot、Dummy、Effect、Label、Ordinal、Count、Binary）的基本原理、特征输出维度及其适用场景。（machine-learning, feature-engineering, data-preprocessing, categorical-encoding）
- [[2025-12-02_Platt-Scaling-for-model-calibration_19ae0c]] — 介绍了模型校准的定义和实际价值，阐述了现代深度学习模型过度自信的现象，并详细剖析了 Platt 缩放（Platt Scaling）的物理映射机制、算法步骤及局限性。（machine-learning, model-calibration, classification-models, probability-estimation）
- [[2025-12-26_Loss-Function-of-16-ML-Algos_19b5c7]] — 汇总了16种常见机器学习算法所采用的典型损失函数，并分析了部分非参数/贝叶斯算法在训练中不需要损失函数的物理本质。（machinelearning, lossfunction, algorithm）
- [[2025-12-26_The-right-way-to-use-multiple-embedding-models_19b5c7]] — 探讨在多模型流水线中混用多个 Embedding 模型时的局限性，阐述了等维异构空间无法直接度量相似度的物理原因，并提出了特征拼接与对齐训练等解决方案。（machinelearning, embedding, representationlearning）
- [[2025-12-29_Identify-fuzzy-duplicates-at-scale_19b6bf]] — 介绍在大规模模糊重复数据检测中，由于 pairwise 两两比对所面临的 O(N^2) 复杂度瓶颈，通过引入分块阻断（Blocking / Bucketing）技术来减少 98% 以上的冗余计算，将原本需要数年的计算量压缩至数小时内完成。（datadeduplication, fuzzymatching, blockingtechnique, scale）
- [[2026-02-04_4-parallel-processing-techniques-in-Python_19c2a8]] — 对比 Python 中实现并发与并行的四种技术：线程、多进程、协程和子解释器。分析了 GIL 的约束、各种技术的适用场景、性能优缺点，并探讨了 Python 3.13 自由线程（无 GIL）的未来演进趋势。（python, concurrency, parallelism, gil, multithreading, multiprocessing, coroutines, subinterpreters）
- [[2026-02-04_Why-ML-models-need-calibration_19c2a8]] — 介绍现代神经网络存在过度自信（overconfidence）的问题，说明为什么机器学习模型需要进行校准（calibration），并提供了一个医疗与政府决策的实例来说明非校准模型的潜在危害。（classification, modelcalibration, machinelearning）
- [[2026-03-04_16-techniques-to-optimize-neural-network-training_19cba7]] — 总结了16种神经网络训练优化技术，包括高效优化器、硬件加速器、增大Batch Size、使用动量（Momentum）、贝叶斯优化超参数搜索、混合精度训练、He/Xavier权重初始化、多GPU并行训练、大模型优化技术（DeepSpeed等）、DDP数据加载、激活检查点（Activation Checkpointing）、GPU端数据归一化、梯度累积以及DataLoader的线程与内存优化。（deeplearning, neuralnetworks, optimization, trainingtechniques）
- [[2026-03-04_6-must-know-MCP-primitives-for-AI-Engineers_19cba7]] — 介绍了 AI 工程师必须掌握的 6 个 Model Context Protocol (MCP) 原语，包括客户端的 Sampling、Roots、Elicitations，以及服务端的 Tools、Resources、Prompts，阐述了其作为双向通信协议超越传统单向工具调用的特性。（AIAgent/MCP, AIAgent/toolcalling）
- [[2026-03-13_How-to-actually-use-train,-validation,-and-test-sets_19ce93]] — 探讨了机器学习中训练集、验证集和测试集的标准划分职责，重点阐述了多次迭代调整导致“验证集过拟合与信息泄露”的隐性瓶颈，并提出了 K 折交叉验证与嵌套交叉验证（Nested CV）的机制流程，以及时序、不平衡、分组数据等复杂环境下的划分规范与预处理防泄露指南。（machinelearning/evaluation, machinelearning/methodology）
- [[2026-03-13_What-are-RL-environments,-and-how-to-build-them_19ce93]] — 探讨在构建多步推理 AI Agent 时，强化学习环境（Environment）所面临的真正瓶颈与挑战，并介绍 NVIDIA NeMo Gym 与 Unsloth 结合 of 解耦架构设计。（ReinforcementLearning, AIAgents, NeMoGym, Unsloth）
- [[2026-03-23_Anatomy-of-the-.claude-folder_19d1c3]] — 详细剖析 Claude Code 控制中心——`.claude/` 目录的结构 and 配置原语，涵盖 CLAUDE.md、规则系统、自定义命令、技能（skills）、智能体（agents）以及权限设置 settings.json 的机制。（ClaudeCode, AITools, Configuration）
- [[2026-03-24_RAG-vs-MetaAI's-REFRAG_19d21b]] — 介绍 Meta AI 提出的 REFRAG 架构，该架构通过在向量层面压缩和过滤检索到的 Chunks，从而实现高效率 RAG 检索，大幅降低延迟与 token 消耗。（RAG, MetaAI, REFRAG, LLM）
- [[2026-03-26_Breathing-KMeans-vs-KMeans_19d2bb]] — 介绍 Breathing KMeans 算法。该算法克服了传统 KMeans 对初始化敏感和多次随机重训耗时的问题，通过动态吸气（分裂）和呼气（合并）过程优化质心位置，提速达 50% 并能有效避免质心错位。（MachineLearning, Clustering, KMeans, BreathingKMeans）
- [[2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a]] — 剖析生产级 Agent Harness 架构，定义 11 个核心模块并详解单步运行流程、长周期 Ralph Loop 协作模式及 7 个架构设计抉择。（AI-Agent/harness, AI-Agent/infrastructure）
- [[2026-04-12_20-most-common-magic-methods_19d838]] — 介绍并分类 Python 面向对象编程中最常用的 20 个魔术方法（Dunder 方法），简述其功能与对 Descriptor 机制的引申。（python, oop, magic-methods）
- [[2026-04-23_Cyclical-feature-encoding_19dbca]] — 机器学习中周期性特征的三角函数（Sine/Cosine）双通道编码方法与等距特征表示。（machine-learning, feature-engineering, cyclical-features）
- [[2026-04-23_LoRAQLoRA-explained-from-a-business-lens_19dbca]] — 从多租户商业与工程架构视角剖析 LoRA/QLoRA 微调的内存、存储优势与适配器动态热插拔运行逻辑。（machine-learning, parameter-efficient-fine-tuning, lora, business-ml）
- [[2026-05-01_A-tricky-LLM-interview-question-for-AI-Engineers_19de58]] — 探讨在微调/蒸馏小模型（如 3B/8B）时，使用顶级大模型作为教师生成合成数据，其效果反而可能比不上中等教师模型这一容量匹配法则。（llm, distillation, fine-tuning）
- [[2026-05-01_How-to-beat-GRPO-without-touching-model-weights_19de58]] — 详细阐述 GEPA 无梯度提示词进化算法，并横向对比其与 GRPO 等强化学习算法的优劣与应用场景。（rl, grpo, gepa, prompt-tuning）
- [[2026-05-03_How-LLM-inference-works-internally_19deee]] — 本文深入剖析了大模型推理内部的工作原理，详细对比了 Prefill（预填充）和 Decode（解码）两个不同的计算阶段及其硬件瓶颈，并讨论了 KV Cache、量化以及 Continuous Batching、Speculative Decoding 和 PagedAttention 等服务层优化技术。（LLM/inference, AI-Infra, KV-Cache）
- [[2026-05-05_How-does-BM25-ranking-algorithm-work_19dfa2]] — 本文介绍了有 30 年历史的经典稀疏检索算法 BM25，通过拆解 IDF（逆文档频率）、TF 词频饱和度以及文档长度惩罚三项核心要素，分析了其在专有名词与错误码精确匹配中的优势，以及其在混合检索（Hybrid Search）架构中的核心价值。（RAG, search, BM25, sparse-retrieval）
- [[2026-05-05_Train-classical-ML-models-on-large-datasets_19dfa2]] — 本文介绍了在处理无法完全载入内存的大规模数据集时，如何使用随机贴片法（Random Patches）来训练经典的集成学习模型（如随机森林）。（machine-learning, random-patches, ensemble-learning, bagging, big-data）
- [[2026-05-25_Build-portable-ML-models-with-ONNX_19e60c]] — 本文探讨了在模型训练与生产伺服部署之间存在的分歧，分析了开放神经网络交换（ONNX）作为跨框架的中间表示的优势，详述了 ONNX Runtime（ORT）的各种执行引擎加速和图优化机制。（MLOps, ONNX, ONNX-Runtime, model-deployment）
- [[2026-06-01_Categorization-of-clustering-algorithms_19e84f]] — 系统总结了 6 类主流聚类算法家族并探讨了其在不同形状和密度数据上的适用性。（machine-learning, clustering）
- [[2026-06-01_Claude-Code-dynamic-workflows,-explained!_19e84f]] — 解析了 Claude Code 在 Opus 4.8 时代引入的 Dynamic Workflows（动态工作流）机制，对比了 Subagents、Agent Teams 与 Dynamic Workflows 在编排、规模、通信和灾备上的差异，探讨了其内部的 JS 脚本执行与对抗性验证原理。（claude-code, multi-agent, dynamic-workflows）
- [[2026-06-08_An-intuitive-guide-to-non-linearity-of-ReLU_19ea91]] — 解析神经网络中 ReLU 激活函数如何通过分段线性插值拟合任意非线性函数，以及多神经元联合的光滑非线性感知本质。
- [[2026-06-14_7-LLM-generation-parameters_19ec7f]] — 解构控制大语言模型（LLM）文本生成的 7 个核心解码参数的工作原理、数学逻辑与应用场景。
- [[2026-06-18_Visual-guide-to-Bi-encoders,-Cross-encoders-&-ColBERT_19edcc]] — 介绍双编码器、交叉编码器与 ColBERT 架构在成对句子评分系统中的工作机制、优劣势，并阐明延迟交互（Late Interaction）平衡检索吞吐与精准度。（sentencesimilarity, biencoder, crossencoder, colbert, nlp）
- [[2026-06-24_Loop-engineering,-clearly-explained!_19ef72]] — 探讨智能体底层的 Tool Call 循环，并拆解 Done 终局判定偏误、上下文腐烂与末日死循环、循环下工具设计的特殊性以及 Maker-Checker 机制等四大痛点。（AIAgents, loop-engineering, context-rot, maker-checker）
- [[2026-06-24_Recursive-language-models_19ef72]] — 介绍由MIT提出的递归语言模型（RLM，Recursive Language Models）架构，该架构通过在Python REPL环境中缓存上下文数据，并让模型使用工具进行Peek、Regex过滤和Partition分治，实现自上而下的递归子调用，从而有效解决Context Rot问题，保证超长文本性能不衰减。（AI-Agent/recursive-language-models, AI-Agent/context-engineering）
- [[2026-06-25_6-components-of-context-engineering_19f00c]] — 探讨上下文工程（Context Engineering）的 6 个核心组件，包括提示词技术、查询增强、长期记忆、短期记忆、知识库检索以及工具与智能体，并指出上下文工程是决定AI应用质量的75%的关键部分。（AI-Agent/context-engineering）
- [[2026-06-25_The-AI-engineering-master-stack-for-2026!_19f00c]] — 介绍了 2026 年 AI 工程师应掌握的 10 层技术栈全景，从底座模型表征到生产环境的 LLMOps 与安全，勾勒出从单点 Prompt 开发向复杂系统工程演进的宏观技术路径。（AI-Agent/Infra, LLMOps, AI-Engineering）
- [[2026-07-03_11-most-important-plots-in-DSML_19f29f]] — 系统归纳了数据科学与机器学习中最重要且必须掌握的 11 种诊断、评估与可解释性图表，简要说明了其物理意义与主要应用准则。（data-science, machine-learning, model-evaluation, model-interpretability）
- [[2026-07-03_Prompt,-context,-harness-&-loop-engineering_19f29f]] — 详细拆解了围绕 LLM 运作的四层工程阶梯（Prompt、Context、Harness、Loop Engineering），它们由内而外包裹，各自承担着大模型应用在推理阶段的不同层级优化与控制面职责。（AI-Agent/loop-engineering, AI-Agent/coding）
- [[2026-07-07_4-LLM-text-generation-strategies_19f3d7]] — 探讨了 LLM 文本生成中的四种核心解码策略（贪婪搜索、多项式采样、束搜索与对比搜索），分析了它们的工作机制以及在流畅度、多样性与重复度等方面的权衡。（LLM/decoding-strategies, LLM/generation）
- [[2026-07-07_Rethinking-KV-caching-for-production-inference_19f3d7]] — 针对 AI 智能体应用中 62% 的重复 Token 浪费问题，介绍解耦式 KV 缓存架构 LMCache，该架构实现缓存管理与推理引擎进程解耦，并引入 CacheBlend 算法提速多文档 RAG 场景。（LLM/inference, Infra/serving, KV-Cache）
- [[2026-07-14_NVIDIA-researchers-built-a-new-transformer-variant_19f617]] — 介绍 NVIDIA 与 MIT 联合提出的 SparDA 架构。该架构在传统 Transformer 的 Q/K/V 投影之上引入第四投影 Forecast，预测下一层所需的 KV 块，从而实现从 CPU 内存异步预取 KV Cache，大幅缓解长文本 CPU offload 传输瓶颈。（LLM/inference, Infra/serving, KV-Cache）
- [[2026-07-14_The-four-types-of-agent-loops_19f617]] — 介绍智能体循环的四种主要设计类型（单步交互式、目标驱动式、时间触发式、事件主动式）及对自主性的分担和职责让渡。（AI-Agent/loop-engineering, AI-Agent/coding）
- [[2026-07-21_5-LLM-Quantization-Techniques_19f86b]] — 探讨大模型量化技术（Quantization）及其面临 of 离群值（Outliers）挑战，并对比五种主流的量化方法（RTN、GPTQ、AWQ、LLM.int8()、QAT）。（LLM/quantization, LLM/optimization）
- [[2026-07-24_11-LLM-evaluation-methods_19f962]] — 系统性整理 11 种必知的大模型（LLM）评估方法与指标（BLEU/ROUGE/BERTScore/G-Eval/Judge/Juries/DAG/Trajectory/Multi-turn等），并探讨其使用局限与最佳实践。
- [[2026-07-24_Delta-attention-in-Kimi-K3-to-fix-growing-KV-cache_19f962]] — 介绍 Kimi K3 采用的 Delta Attention 机制。该机制将历史信息折叠压缩在固定大小的关联矩阵中，通过“先读后写、只写差值”的 Delta Rule 更新关联，实现 $O(1)$ 的空间与 $O(N)$ 的计算开销。
- [[2026-07-24_Quantile-regression_19f962]] — 本文详细介绍了分位数回归（Quantile Regression）及其核心损失函数分位数损失（Quantile Loss / Pinball Loss），对比了传统最小二乘（OLS）均值点预测的局限并总结了其工程价值。（machine-learning, regression, loss-function）
- [[2026-07-27_Agent-memory-and-state-are-not-the-same-thing!_19fa57]] — 本文探讨了 AI 智能体设计中状态（State）与记忆（Memory）的本质区别，提出了状态 Checkpoint断点恢复方案与多智能体记忆命名空间隔离机制。（AI-Agent/harness, AI-Agent/memory, state-management）
- [[2026-07-27_Graph-engineering-clearly-explained_19fa57]] — 阐述了图工程（Graph Engineering）的核心概念、多层同轴架构关系、四大痛点设计准则以及引入图工程的决策依据。（Agent, Multi-Agent, Graph-Engineering, Architecture）
- [[2026-07-27_The-anatomy-of-diffusion-LLMs_19fa57]] — 介绍了扩散语言模型（dLLMs）的基本原理、物理架构优势（从 memory-bound 转向 compute-bound），以及掩码扩散、Block Diffusion、注意力掩码退火与推理加速技术。（LLM, Diffusion-LLM, Autoregressive, Inference-Optimization）
- [[2026-07-28_CPU-vs-GPU-vs-TPU-vs-NPU-vs-LPU_19faa9]] — 详细介绍了五种主流AI计算硬件架构（CPU、GPU、TPU、NPU和LPU）内部逻辑设计的物理差异与核心权衡，展现了AI计算芯片从通用灵活性向极致专用化的演进过程。（AI-Hardware/Accelerator, Computer-Architecture/Processor）
- [[2026-07-28_Technical-LLM-interview-question!_19faa9]] — 介绍了 DigitalOcean 提出的基于确定性、轻量化行为信号对生产环境 Agent 交互轨迹进行高效低成本筛选过滤的采样策略，大幅提升了人工标注的效率。（AI-Agent/evaluation, Software-Engineering/Observability）
- [[2026-07-31_6-automatic-optimization-methods-for-LLM-systems_19fb9f]] — 介绍了六种在大模型系统中实现自动化优化的前沿方法（OPRO, MIPROv2, TextGrad, GEPA, AlphaEvolve, AutoResearch），通过大模型自动反馈循环替代人工调优。（RSI, AI-Agent/prompt-engineering, LLM/arch）
- [[2026-07-31_Subagents-vs.-Agent-Teams_19fb9f]] — 对比了 Claude 提供的两种多智能体范式：Sub-agents（基于隔离实现并行与 Context 压缩，单向反馈）和 Agent Teams（基于协同通信与共享状态，双向协作），并从第一性原理探讨了以上下文为中心的分治逻辑。（multi-agent, sub-agents, agent-teams, architecture）
- [[2026-08-01_Double-Descent-vs.-Bias-Variance-Trade-off_19fbed_part3]] — 介绍机器学习与深度学习中的双下降（Double Descent）现象，该现象对传统的偏差-方差折中理论提出了挑战，指出在模型复杂度跨越临界插值界限后测试误差可能会二次下降。（machine-learning, double-descent, generalization）
- [[2026-08-10_Cross-model-KV-cache-transfer-in-LLM-families_19febef2c6003814]] — 介绍同一模型家族内的 KV Cache 跨模型转换：通过跨层线性映射复用既有 Prefill 计算，并明确其跨家族与异构 KV 配置尚未验证。（LLM/inference, Infra/serving）

## Concepts
- [[concepts/概念_Modular_RAG_模块化检索增强生成]] — 将 RAG 拆解为可替换、可路由、可组合独立功能模块的架构范式，突破线性流程，支持条件分支、动态调度与循环迭代（RAG/retrieval）
- [[concepts/概念_Decision_Model_专用判断模型]] — 将分类选择与概率估计从自回归生成中解耦的轻量级模型或接口，通过单次前向提取选项 Logits 映射概率分布，服务于 Agent 高频状态机跳转与动作决策（LLM/inference, AI-Agent/tool-calling）
- [[概念_LLM模型路由]] — 在 LLM 网关层依据输入复杂度动态分流请求的机制及其与 Prefix Cache、Agent 维护成本间的权衡（LLM/inference, Infra/serving）
- [[概念_RLCD校准决策强化学习]] — 面向判别式决策的置信度校准强化学习范式（LLM/training, AI-Agent/tool-calling）
- [[concepts/概念_Kimi_Delta_Attention_增量注意力|概念_Kimi_Delta_Attention]] — KDA：channel-wise gate 线性注意力机制（LLM/arch/attention）

- [[概念_SAG_动态超边结构化检索增强生成]] — 基于查询时动态超边的 SQL 检索增强生成架构（SAG），通过入库时抽取事项与实体存入关系型数据库并在查询时利用 SQL JOIN 动态激活局部多跳关联，克服传统向量 RAG 多跳断链与 GraphRAG 离线建图成本高昂的痛点（RAG/retrieval, RAG/query）

- [[概念_Roofline模型与算力强度]] — 量化评估芯片峰值算力与内存带宽瓶颈的经典模型，通过算力强度（FLOPs/Byte）与硬件平衡拐点划分计算受限与内存带宽受限区，指导大模型推理两阶段的系统调优（Infra/gpu, Infra/gpu, Infra/serving, LLM/inference）
- [[概念_Presentation_Tools_表现层工具化]] — 表现层工具化：将富交互 UI 组件建模为强类型工具调用，由服务端参数校验与业务状态注入驱动客户端渲染，兼具屏幕布局反向感知与历史重现能力（AI-Agent/UI, AI-Agent/tool-calling）
- [[概念_电商智能体架构]] — 面向长程高耦合交易场景的电商智能体工程体系：单模型结合技能架构（Skills over Subagents）、核心系统轻量封装、双前线延迟工程、三段式缓存及外围 Harness 硬件安全门禁（AI-Agent/tool-calling, AI-Agent/context-engineering）
- [[概念_AI原生思维]] — 以模型能力边界为锚点、围绕 Agent 特性重构研发流程并建立个体持续自收敛反馈循环的系统化方法论（AI-Agent/coding, AI-Agent/skill）

- [[概念_GQA_分组查询注意力]] — GQA（Grouped-Query Attention）分组共享单组 Key/Value 头，在大幅缩减 KV Cache 显存开销的同时保留接近 MHA 的建模表达力，是现代开源 LLM 的基准注意力架构（LLM/arch/attention, LLM/inference）
- [[概念_MRL套娃表示学习]] — MRL（Matryoshka Representation Learning）在训练阶段优化多粒度前缀嵌套损失，使向量前 n 维天然保持独立高质量语义，支持推理期免微调按需物理截断维度（RAG/embedding）

- [[概念_事实性存储与提取分离诊断范式]] — 区分大模型事实性错误中存储失败（知识未编码进权重）与访问失败（权重已存但提问无法取出）的诊断范式，提供两把尺子测评方法与四阶工程排查阶梯（LLM/hallucination, LLM/reasoning）

- [[概念_Agentic_Web_Search_智能体网络搜索]] — 面向大模型智能体的网络搜索架构与供应链解耦范式，将搜索 Stack 拆分为代理层、定向语义索引、上下文精炼与云端运行时四层，并重构排序反馈信号（AI-Agent/deep-research, AI-Agent/infra, RAG/retrieval）

- [[概念_激活值重计算]] — 重计算原理及不同并行组合的激活值公式
- [[概念_Zero显存优化]] — Zero1/2/3 三种策略与计算公式
- [[概念_两阶段检测]] — Region-based 两阶段范式：Proposal → 分类回归
- [[概念_单阶段检测]] — Region-free 单阶段范式：YOLO/SSD 直接回归
- [[概念_Anchor机制]] — 多尺度多宽高比参考框，检测回归基准
- [[概念_RoI_Pooling_候选区域池化]] — 候选区域映射为等长特征向量；RoIAlign 消除量化误差
- [[概念_检测评测指标]] — IoU/mAP(VOC/COCO)/FPS
- [[概念_多尺度检测]] — 多尺度输入/特征图提升检测鲁棒性
- [[概念_NMS_非极大值抑制与Soft_NMS]] — 非极大抑制与软化版本
- [[概念_数据增强_检测]] — 检测任务数据增强需同步变换标注框
- [[概念_Backbone设计范式]] — Repeat/Multi-path/Skip-connection 三范式
- [[概念_通道注意力]] — SENet Squeeze-Excitation 通道注意力
- [[概念_深度可分离卷积]] — Depthwise + Pointwise 分解，大幅减少计算量
- [[概念_位置敏感检测]] — R-FCN Position Sensitive Score Maps / DCN 可变形卷积
- [[概念_特征金字塔网络]] — FPN 自顶向下多尺度融合及变体
- [[概念_图像分割]] — 语义/实例/交互式分割，SAM 统一为 Prompt 驱动
- [[概念_Prompt驱动分割]] — SAM 多种 Prompt 类型驱动分割
- [[概念_Vision_Transformer_视觉Transformer]] — ViT 将图像 patch 化输入 Transformer
- [[概念_Focal_Loss_焦点损失]] — 下调简单样本权重解决类别不平衡
- [[概念_扩散模型]] — 前向加噪 + 反向去噪生成；DDPM 开创
- [[概念_Latent_Diffusion_潜空间扩散模型]] — 先 AutoEncoder 压缩到 latent 再训扩散模型
- [[概念_OCR数据增强]] — OCR 形态学/噪声/变换 + OneOf 组合
- torchvision图像增强 — torchvision.transforms 增强 API 清单
- [[概念_自注意力复杂度]] — 自注意力 O(N²d)/O(N²)，瓶颈在内存 I/O
- [[概念_FlashAttention_快速注意力]] — I/O 感知精确注意力，分块 + 在线 Softmax
- [[概念_Normalization方法对比]] — BN/LN/IN/GN 维度与用途对比
- [[概念_Batch_Normalization_批归一化]] — BN 动机/算法/作用/问题
- [[概念_DPP_Cholesky分解加速]] — Cholesky 分解加速 DPP 贪婪 MAP 推断，O(N·k²)
- [[概念_SVD_奇异值分解]] — 任意矩阵分解 A=UΣV^T，降维/压缩基础工具
- [[概念_Transformer架构]] — Transformer 5 步流程：Tokenization/Embedding/Attention/FFN/Output
- [[概念_大模型训练三阶段]] — Pre-train/Instruction FT/RLHF 训练流程
- [[概念_Prompt工程方法]] — 有效 Prompt 方法：补充前提/范例/拆解/自我反省/Self-Consistency
- [[概念_梯度下降优化器]] — Vanilla GD/Momentum/AdaGrad/RMSProp/Adam 原理对比
- [[概念_Early_Stopping_早停机制]] — 监控 val_loss 提前停止训练避免过拟合
- [[概念_PyTorch训练循环]] — PyTorch 标准训练 9 步流程模板
- [[概念_AI_Native_Infra_AI原生基建]] — 专为 AI 设计、去掉人类兜底层的基础设施范式
- [[概念_L0_L5_能力成熟度模型]] — AI 从模仿人类到掌控 OS 的 L0-L5 演进
- [[概念_Result_as_a_Service_结果即服务]] — 人类只表达需求验收结果、AI 负责全实现的终极形态
- [[概念_KV_Cache_键值缓存]] — 缓存 K/V 已计算结果，空间换时间避免重复计算
- [[概念_KV_跨模型缓存转换]] — 以跨层表示映射在模型路由切换时复用 KV Cache；当前仅验证同家族模型
- CUDA_Graph — 多 GPU 操作转 DAG 一次性提交，减少 CPU-GPU 交互
- [[概念_模型并行]] — 拆分大模型到多 GPU，解决单机存不下
- [[概念_连续批处理]] — 动态批处理，短请求完成即释放、新请求随时加入
- 通信计算重叠 — 用 GPU stream 令计算与通信时间上重叠
- [[概念_Label_Smoothing_标签平滑]] — 软化硬标签缓解过度自信（medium）
- [[概念_Mixup训练]] — Beta 分布插值混合样本图像与标签（medium）
- [[概念_学习率调度]] — ReduceLROnPlateau/Cosine/MultiStep/Warmup 调度器
- [[概念_RL环境]] — Agent 学习的虚拟世界：状态/任务/奖励三要素
- [[概念_RLaaS_强化学习即服务]] — 强化学习即服务，Palantir 式企业深度定制
- [[概念_复制训练]] — 复现现有软件作为 RL 任务，单元测试验证奖励
- [[概念_RLVR_可验证奖励强化学习]] — 可自动验证奖励的强化学习
- [[概念_IFD指令跟随难度]] — Instruction-Following Difficulty，通过困惑度挑选高价值 SFT 样本
- [[概念_K_Center_Greedy_中心贪婪算法]] — 基于核心集策略的贪心样本选择算法
- [[概念_Reward_Hacking_奖励攻陷与作弊]] — 奖励黑客：利用奖励模型漏洞取高分而非真正满足意图
- [[概念_SFT数据三维度]] — 规模/质量/多样性三维度评估与数据选型配比
- alignment_tax — 对齐税：安全与偏好对齐导致的模型通用能力或基础性能下降
- [[概念_On_Policy_与_Off_Policy_策略数据]] — 强化学习训练中采样模型与目标优化策略的同源匹配关系
- [[概念_多阶段训练策略]] — 从通用领域到垂直任务能力的退火精调流转路径
- [[概念_灾难性遗忘]] — 微调新任务时导致原有预训练通用知识与能力退化
- [[概念_智能体能力金字塔]] — 工具/规划/适应/接地气/常识推理五层能力
- [[概念_Groundedness_事实接地性]] — 智能体紧贴上下文、不幻觉不捏造的能力
- Git仓库历史诊断 — 用变更热点、维护者、缺陷聚集、提交趋势与救火信号建立陌生代码库阅读路径（Skill/linux, AI-Agent/coding）
- Random_Patches大数据训练 — 随机贴片在大数据集上训练经典集成模型的机制与方差降低原理
- ONNX模型跨平台部署 — 模型开发框架与伺服生产环境解耦标准、ORT图优化与硬件子图分发机制
- [[概念_聚类算法分类综述]] — 系统性梳理聚类算法的 6 大主流家族（基于质心、基于连通性、基于密度、基于图、基于分布和基于压缩/降维），对比硬聚类与软聚类的决策边界，并分析算法对聚类形状和密度的适应差异。（MachineLearning, Clustering）
- [[概念_LMCache_解耦式KV缓存]] — 旁路独立进程实现缓存管理与推理引擎解耦，辅以 CacheBlend 选择性重计算，大幅提速多文档与 Agent 推理。（LLM/inference, Infra/serving）
- [[概念_SparDA预测式KV缓存预取]] — 引入 Forecast 跨层预测及双 CUDA stream 异步预取机制，有效重叠长文本下 CPU offload 传输与 GPU 推理计算，大涨吞吐量。（LLM/inference, Infra/serving）
- [[concepts/概念_Loop_Engineering循环工程]] — 定义图工程（Graph Engineering）的核心内涵以及三大物理要素，展示 5 层嵌套同轴系统架构并拆解四大痛点设计准则。（Architecture, Agent, Multi-Agent, Graph-Engineering）
- [[概念_AI硬件加速芯片架构]] — 定义并横向对比 CPU、GPU、TPU、NPU 与 LPU 五种主流 AI 计算芯片架构 of 物理特征、存储层次以及计算调度机制。（Architecture, Hardware, Processor, Inference）
- [[概念_机器学习双下降现象]] — 阐述在过度参数化区域由于隐式正则化作用测试误差发生二次下降的现象，分析临界插值界限与偏置-方差折中理论的物理差异。（MachineLearning, Double-Descent, Generalization）

### RAG
- [[概念_RSE相关段落提取]] — Relevant Segment Extraction：定位并提取文档连续相关段落
- [[概念_上下文增强检索]] — 检索前增强块上下文，提高切片独立理解能力
- [[概念_RAG基础流程]] — RAG 三步：Indexing/Retrieval/Generation
- [[概念_Embedding与向量检索]] — 文本转嵌入向量，按相似度检索 top-k
- [[概念_向量数据库]] — 专用于存储向量化表示的系统，ANN 索引+相似度查询
- [[概念_Query_Translation_查询改写与翻译]] — 查询翻译：改写/分解/退一步提升检索
- [[概念_RAG_Fusion_多查询融合生成]] — 多查询 + RRF 排序融合检索结果
- [[概念_HyDE_假设文档嵌入]] — 生成假设文档作为检索输入
- [[概念_RAG_Routing_检索智能路由]] — 逻辑路由/语义路由智能选择检索路径
- [[概念_Query_Construction_查询构建]] — 自然语言转元数据结构化查询
- [[概念_Multi_Representation_Indexing_多表征索引]] — 摘要+原文多表示索引（Proposition Indexing）
- [[概念_RAPTOR_递归树状检索索引]] — 树状分层索引：GMM/UMAP/多尺度聚类递归摘要
- [[概念_ColBERT_多向量延迟交互检索]] — token 级嵌入 late interaction 细粒度检索
- [[概念_文本切分五层级]] — 文本切分 Level 1-5 框架：字符/递归/文档/语义/Agentic
- [[概念_字符切分]] — Level 1 简单字符长度切分
- [[概念_Chunk_Size_分块大小与重叠]] — 块大小与块重叠两个基础参数
- [[概念_递归字符切分]] — Level 2 分隔符递归合并，实践首选
- [[概念_Token切分优化]] — 按 token 而非字符计长度，对齐模型处理
- [[概念_文档结构切分]] — Level 3 适配 JSON/Markdown/代码等格式
- [[概念_语义切分]] — Level 4 向量差异超阈值切分，四种阈值方法
- [[概念_问题生成检索增强]] — LLM 为文本片段生成问题，增强向量检索匹配
- [[概念_Fusion_Retrieval_融合检索]] — 稀疏(BM25)+稠密(向量)双路检索融合
- [[概念_RRF_互易秩融合]] — RRF 排序融合多路检索结果
- [[概念_BM25_最佳匹配25算法]] — 经典稀疏检索算法，词频+文档长度惩罚
- BM25检索算法 — 定义 BM25 基石地位，数学公式拆解（IDF/TF饱和度/文档长度惩罚）与混合检索架构（RAG）
- [[概念_检索后处理]] — 检索后重排/压缩/Long-text Reorder
- [[概念_Contextual_Compression_上下文压缩]] — LLM 提取检索文档中与查询相关的片段
- [[概念_Long_Text_Reorder_长文本位置重排序]] — 长文本检索结果重排，重要文档置首尾
- [[概念_查询重写]] — LLM 改写用户查询提升检索效果
- [[概念_子查询分解]] — 复杂查询拆为子查询分别检索再合并
- [[概念_Step_Back_回退提示]] — 退一步生成更抽象的查询获取更广泛上下文
- Markdown标题切分 — 按 Markdown 标题层级结构化切分文档
- [[概念_Matryoshka表示学习]] — MRL 嵌套学习多粒度表征，可截断维度保留语义
- [[概念_Sparse_Embedding_稀疏向量嵌入]] — 关键词式稀疏向量（TF-IDF/BM25/SPLADE）
- [[概念_Dense_Embedding_稠密向量嵌入]] — 语义级稠密向量，通用语义搜索首选
- [[概念_Quantized_Embedding_量化向量嵌入]] — float32→int8 压缩，省内存磁盘
- [[概念_Binary_Embedding_二进制向量嵌入]] — 0/1 二值化极致压缩，设备端离线快搜
- [[概念_词向量]] — Word2Vec/GloVe/FastText 静态词向量及其局限
- [[概念_BERT各向异性]] — BERT 词向量锥形分布导致相似度失效及优化
- [[概念_Sentence_BERT_孪生网络句向量]] — 孪生/三级网络微调 BERT 优化句向量相似度
- [[概念_SimCSE_简单对比学习句向量]] — Dropout mask 增广 + 对比学习优化句向量
- [[概念_Instruct_Embedding_指令增强向量嵌入]] — 编码查询时附带任务指令引导多维度检索
- [[概念_Rerank_重排序]] — 检索后相关性精排，Qwen3 LLM 化 yes/no 打分
- [[概念_ColBERTv2残差压缩]] — k-means 聚类+残差量化，存储减 6-10 倍性能损失 1-2%
- [[概念_混合检索]] — 稀疏+稠密+BM25 多路召回融合(RRF/加权)
- [[概念_近似最近邻搜索]] — ANNS：哈希/树/图/量化四类加速方法
- [[概念_向量索引方法]] — Flat/Tree/LSH/IVF-PQ/HNSW 索引类型对比
- [[概念_向量相似度度量]] — L2/L1/余弦/内积/汉明/杰卡德距离度量
- [[概念_向量量化]] — float32→int8/INT4/BBQ/PQ/残差量化压缩方法
- [[概念_Agentic_RAG_智能体检索增强生成]] — 智能体+RAG：查询规划/工具利用/推理优化
- [[概念_Memory_RAG_显式记忆增强检索]] — 显式记忆增强 RAG：Memory3/MemoRAG/CAG
- [[概念_DOS_RAG_动态操作空间检索]] — 保留文档原始结构：检索后按原文顺序排列片段
- [[概念_DMQR_RAG_动态多查询改写检索]] — 多样化多查询改写：GQR/KWR/PAR/CCE 四策略 + 自适应选择
- [[概念_LLM重排序]] — 让 LLM 给文本相关性打分(0~1)的精排方法
- [[概念_父页面检索]] — 小块检索定位、完整父页面入上下文
- [[概念_表格序列化]] — 大表格转一系列上下文独立字符串
- [[概念_多查询路由]] — 路由到数据库/提示词/复合查询拆解
- [[概念_结构化输出]] — 强制 LLM 按 schema 输出 JSON，与 CoT 结合
- [[概念_Prompt_Compression_提示词压缩]] — 检索后压缩上下文，LongLLMLingua（medium）
- [[概念_CRAG_纠正性检索增强生成]] — 纠正型 RAG：评估文档相关性触发额外检索（medium）
- [[概念_Self_RAG_自省式检索增强生成]] — 自我反思 RAG：生成后自检决定是否补检索（medium）
- [[概念_Adaptive_RAG_自适应检索增强生成]] — 自适应 RAG：按查询复杂度选择检索生成策略（medium）

#### 阿里/美团/优图实践概念（批次7）
- [[概念_Graph_RAG_知识图谱增强检索]] — 图结构组织知识，多跳推理跨文档关联检索
- [[概念_SMT查询改写]] — 统计翻译模型查询改写，噪声信道+BeamSearch+XGBoost
- [[概念_NMT_强化学习查询改写]] — NMT 改写以搜索系统为环境强化学习优化
- [[概念_向量化召回改写]] — 双塔向量从候选池 ANN 召回改写词（模糊改写）
- [[概念_协同训练]] — NMT-BERT 半监督互训提升数据和模型质量
- [[概念_分层知识蒸馏]] — Reranker 多层输出约束，支持层级输出能力
- [[概念_Embedding训练管线]] — 多阶段对比学习+精细数据工程+多任务均衡
- [[概念_Text2SQL_自然语言转SQL]] — 自然语言转 SQL，MAC-SQL 多智能体框架
- [[概念_Graph_RAG_知识图谱增强检索]] — 图/树结构组织知识的检索增强生成
- [[概念_知识树结构]] — 融合图与树优点的四级知识粒度树型图谱
- [[概念_S2Dual社区检测]] — Structure+Semantics 双感知社区检测，超越 Leiden

#### 语义搜索/系统设计/评估概念（批次8）
- [[概念_Semantic_Search本质]] — metric embedding，document as index，无结构即灵活
- [[概念_Multi_Vector_多向量检索]] — 用代理表示（自然语言/总结）索引低资源/长文件
- 距离函数选择 — 余弦(非度量)/欧氏(度量)距离选型与三角不等式
- [[概念_Lazy_Graph_RAG_惰性知识图谱增强检索]] — 语义搜索弥补 KG 不足，索引成本降至 0.1%（medium）
- [[概念_迭代式表格推理]] — TableRAG 在线推理：拆解/检索/SQL/组合四步
- [[概念_融合知识库]] — 多元异构数据统一逻辑存储，物理存储不变
- [[概念_统一知识图谱]] — 多模态元素统一图谱，N度扩展查询提取子图
- [[概念_RAGAS_RAG评估框架]] — RAGAS 检索侧/生成侧多维评估指标

#### 腾讯QO/北大综述/OpenAI最佳实践概念（Phase2 收尾）
- [[概念_查询扩展]] — 内部扩展(LLM知识)+外部扩展(知识库)提高检索效果
- [[概念_查询消歧]] — 识别消除查询歧义，确保单一精确解释
- [[概念_查询抽象]] — 提炼核心概念创建高层次表示，Step-back 为具体实现
- [[概念_LLM应用优化两轴]] — Context Optimization(RAG) + LLM Optimization(FT) 两轴并行迭代（LLM）
- [[概念_Fine_Tuning_模型微调]] — 微调增强 LLM 特定领域/任务能力，蒸馏降本（LLM）

### LLM/arch/Mamba（批次 Mamba）
- [[概念_SSM_状态空间模型]] — SSM 两方程：状态方程/输出方程，A/B/C/D 矩阵（LLM/arch/Mamba）
- [[概念_SSM三种表示]] — 连续/循环/卷积三种等价表示，训练用卷积、推理用循环（LLM/arch/Mamba）
- [[概念_SSM离散化]] — ZOH 离散化 + 步长参数 Δ，连续 SSM 转为离散序列模型（LLM/arch/Mamba）
- [[概念_HiPPO矩阵]] — Legendre 多项式系数构造矩阵 A，压缩并记忆长程历史（LLM/arch/Mamba）
- [[概念_LTI_线性时不变]] — LTI 局限：A/B/C 固定导致无内容感知，选择机制的动机（LLM/arch/Mamba）
- [[概念_Mamba选择机制]] — B/C/Δ 输入依赖，实现 content-aware 推理（LLM/arch/Mamba）
- [[概念_Mamba硬件感知算法]] — parallel scan + kernel fusion + recomputation，GPU 高效实现（LLM/arch/Mamba）
- [[概念_MambaBlock架构]] — 投影+1DConv+SelectiveSSM+残差，Mamba1/2 Block 结构（LLM/arch/Mamba）
- [[概念_SSD_状态空间对偶]] — Mamba2 核心：SSM 与线性 Attention 数学等价（LLM/arch/Mamba）
- [[概念_半可分离矩阵]] — SSM 变换矩阵的代数结构，SSD 算法分块分解基础（LLM/arch/Mamba）
- State_Swapping — Mamba 特有推理范式：预生成 state 复用，无需 few-shot（LLM/arch/Mamba）

### LLM/arch/MoE（批次 MoE+arch）
- [[概念_MoE混合专家]] — 稀疏专家层替换 FFN，相同计算预算实现更大模型容量（LLM/arch/MoE）
- [[概念_MoE_Router_专家路由门控网络]] — Top-k 门控网络/路由机制，决定 Token 路由到哪些专家（LLM/arch/MoE）
- [[概念_MoE负载均衡]] — 噪声 Top-k / 辅助损失 / 专家容量限制防止专家坍塌（LLM/arch/MoE）
- [[概念_Mamba_混合架构]] — Hybrid Transformer-Mamba：AMF/MF 交错模块，O(n) 长序列处理（LLM/arch/Mamba, LLM/arch/MoE）
- [[概念_CoT_自适应长短思考]] — 根据问题复杂度自动切换快速/深度推理模式（LLM/arch）
- [[概念_MLA_多头潜在注意力]] — K/V 压缩进低维潜在空间，KV Cache 最小化（LLM/arch）
- [[概念_滑动窗口注意力]] — 局部注意力机制，大幅降低 KV Cache 内存（LLM/arch）
- [[概念_QK_Norm_注意力查询键归一化]] — Q/K 在 RoPE 前各加 RMSNorm，稳定大模型训练（LLM/arch）
- [[概念_NoPE无位置嵌入]] — 不使用位置编码，因果掩码隐式学习序列顺序（LLM/arch）
- [[概念_Muon优化器]] — 替代 AdamW 的新优化器，Kimi K2 首次在 1T 参数规模使用（LLM/training）
- [[概念_GRPO_群组相对策略优化]] — 组相对策略优化，混元 TurboS 后训练 RL 算法（LLM/training/RL）

### LLM/arch/VLM（批次3）
- [[概念_MLLM三位一体架构]] — 视觉编码器 + 连接器 + LLM 通用框架（LLM/arch/VLM）
- 视觉基础模型统一范式 — Prompt 驱动 Seq2Seq，一套权重统一多视觉任务（LLM/arch/VLM）
- [[概念_AnyRes高分辨率处理]] — LLaVA 系列全局+局部双路高分辨率策略（LLM/arch/VLM）
- [[概念_DeepStack深度视觉融合]] — Qwen3-VL ViT 多中间层特征注入 LLM 浅层（LLM/arch/VLM）

### LLM/arch/attention + inference（批次3）
- [[概念_线性注意力与混合注意力]] — Linear Attention O(N)、Hybrid 3:1 路线及行业现状（LLM/arch/attention）
- [[概念_MLA低秩KV压缩]] — DeepSeek MLA：低秩压缩 + 矩阵吸收广播优化（LLM/arch/attention）

### LLM/inference + reasoning（批次4）
- [[概念_量化]] — 通过降低权重和激活值的数据位宽以显著减少模型显存占用及加速推理的技术 (LLM/inference)
- [[概念_推测解码]] — Draft-then-Verify：四大推测草稿变体与无损并行验证加速范式（LLM/inference）
- [[概念_混合精度训练]] — BF16/FP32混合训练流程，16 bytes/参数显存估算（LLM/inference）
- [[概念_LoRA与QLoRA显存]] — LoRA 2Φ、QLoRA 0.5Φ显存估算原理（LLM/inference, 面试）
- [[概念_CoT_高级思维链方法]] — CoT/CoT-SC/Decoding CoT/ToT+MCTS 及成本权衡（LLM/reasoning）
- [[概念_自适应快慢思考]] — 三方案：Qwen3 SFT、AdaCoT Pareto、AdaThinking 约束优化（LLM/reasoning）
- [[概念_LLM推理两阶段]] — 对比 Prefill 与 Decode 硬件瓶颈，详细介绍 Continuous Batching、Speculative Decoding、PagedAttention 三大优化方案。（LLM/inference）

### LLM/reasoning + training/RL（批次5）
- [[概念_DeepSeek_R1_训练管道]] — 冷启动SFT→推理RL→拒绝采样SFT→全场景RL四阶段，规则奖励无奖励黑客（LLM/training/RL）
- [[概念_PPO_近端策略优化]] — 生成策略+参考策略+价值模型三组件，RLHF 核心算法（LLM/training/RL）
- [[概念_RLHF_基于人类反馈的强化学习]] — 人类偏好→奖励模型→PPO 对齐流程，RLVR 演进方向（LLM/training/RL）
- [[concepts/概念_Verifiable_Reward_可验证奖励机制]] — 验证器判对错、奖励函数给分值，GRPO 奖励设计原则（LLM/training/RL）
- [[概念_Agent感知记忆推理三能力]] — CoT 赋能 Agent：感知CoT/记忆CoT（树搜索+矢量检索）/推理CoT（AI-Agent, LLM/reasoning）

### LLM/training + hallucination（批次7）
- [[概念_训练并行策略]] — 解决大规模语言模型训练内存与计算瓶颈的基础并行化方法集合（含 DP/TP/PP） (LLM/training)
- [[概念_LoRA_低秩适应微调]] — LoRA 低秩分解原理、r/alpha/dropout 超参、QLoRA 变体与端侧适用场景（LLM/training/post-train）
- [[概念_Scaling_Law三大规律]] — 预训练/后训练/推理三大 Scaling Law 定义、技术手段与 Kaplan/Chinchilla 关系（LLM/training）
- [[概念_LLM外在幻觉与上下文内幻觉]] — 翁荔框架：两种幻觉类型、预训练/微调新知识两大根因（LLM/hallucination）
- [[概念_幻觉检测方法]] — FActScore/SAFE/SelfCheckGPT/TruthfulQA 检测体系（LLM/hallucination）
- [[概念_LLM幻觉消除技术分类]] — 32 种技术两大分类：提示工程（RAG/反馈/提示微调）vs 模型开发（LLM/hallucination）
- [[概念_抗幻觉方法]] — RARR/FAVA/Self-RAG/CoVe/FLAME/WebGPT 抵抗方法体系（LLM/hallucination）
- [[concepts/概念_LLM文本生成解码策略|]] — 温度参数控制输出分布平滑度，高温增创意增幻觉，低温保准确减创意（LLM/hallucination, LLM/inference）

### LLM/面试/训练/RL（批次9）
- [[概念_Scaling_Law_AI团队扩展律]] — AI 团队规模与产出效率的悖论：小而精 vs 规模扩张（创业）

### LLM/Recommendation + arch（Batch 10）
- [[概念_数字人文案生成]] — 口语化改写/多步蒸馏/图文一致/测评体系完整框架（LLM）

### AI-Agent/tool-calling MCP系列（Phase 4 Batch 1）
- [[概念_WebMCP_浏览器原生工具协议]] — Chrome 与 Edge 团队提出的浏览器原生 Agent 工具声明规范，允许前端网页通过 JS API 或 HTML 扩展属性直接暴露强类型动作与输入 Schema（AI-Agent/tool-calling, AI-Agent/UI）
- [[概念_AI_Native_SDLC_AI原生软件开发生命周期]] — Anthropic 提出的 AI Native 软件开发生命周期方法论，以产物驱动闭环循环（Loop）重构研发流程，融合 CLAUDE.md/Skill/Hook 三层规则防线与五层落地路径（AI-Agent/coding）
- [[概念_CLAUDE.md最佳实践]] — 编写 CLAUDE.md 工程宪法以约束 Agent 行为的高级指南与规范范式 (AI-Agent/coding)
- [[概念_MCP协议]] — MCP 定义、CHS 架构、五大原语、传输方式、与 Function Call 关系全景（AI-Agent/tool-calling）
- [[概念_MCP_CHS架构]] — Client-Host-Server 三组件精确界定：Host 是 AI 智能唯一承载者，Server/Client 是模型无关 RPC 管道（AI-Agent/tool-calling）
- [[概念_MCP六大原语]] — Tool/Prompt/Resource/Sampling/Roots/Elicitations 六类原语：触发方、用途、高阶玩法与 Web 化方向（AI-Agent/tool-calling）
- [[概念_MCP传输方式]] — Stdio/SSE/Streamable HTTP 三种传输方式对比与选型（AI-Agent/tool-calling）
- MCP与Function_Call对比 — 协议 vs 模型特性、静态 vs 动态、碎片化痛点与 MCP 解法（AI-Agent/tool-calling）
- [[概念_MCP代码执行模式]] — CodeAgent 模式：按需加载工具定义，Token 消耗减少 98.7%，含隐私保护与 Skills 沉淀（AI-Agent/tool-calling）
- [[概念_HITL_MCP_人机协同协议架构]] — send_inquiry 挂起等待人类答复，MCP Notification 传凭条，HTTP 接口收答复，多端协同（AI-Agent/tool-calling）
- [[概念_MCP_Proxy_代理拦截模式]] — 代理模式在 tool/call 前植入确认逻辑，现有 MCP Server 零改动（AI-Agent/tool-calling）
- [[概念_Agent思考工具]] — think/plan/action 工具强制结构化规划，航空客服提升 54%，优于纯 Prompt（AI-Agent/tool-calling）
- [[概念_Orchestrator_Worker_编排工模式]] — 主智能体规划分解，子智能体并行执行，多智能体 vs 单智能体提升 90.2%（AI-Agent/multi-agent）
- [[概念_多智能体协调]] — 多智能体协调挑战、提示词 8 原则、评测策略与生产可靠性（AI-Agent/multi-agent）
- [[概念_LLM_Wiki范式]] — Andrej Karpathy 提出的知识管理范式，在摄入端预先结构化与关联，实现高复利知识编译（Skill/knowledge-bank）
- [[概念_Agent三段式记忆演进]] — Storage -> Reflection -> Experience 三阶段演进框架及驱动演进的三大根本动力（AI-Agent/memory）
- [[概念_Agent完整轨迹评估]] — 面向复杂智能体多步规划、检索与多轮会话的高度对准人工监督与全轨迹评估（AI-Agent/eval）
- [[概念_Agent系统自动优化闭环]] — 利用 DSPy GEPA/MIPROv2 算法与回放验证闭环，全自动优化系统提示词（AI-Agent/prompt-engineering）
- [[概念_RAG与LLM_Wiki对比]] — RAG 适用大规模被动检索 vs LLM Wiki 适用知识积累与高复利主动编译（Skill/knowledge-bank）
- 知识编译与复利 — LLM 担任知识库编译器，解决信息存储孤岛痛点并释放连接复利（Skill/knowledge-bank）
- [[概念_渐进式披露]] — 按总览到细节的层级动态展示信息，降低用户与大模型认知及上下文负荷（AI-Agent/UI, AI-Agent/context-engineering）
- [[概念_系统提示词四层架构]] — 核心定义、交互接口、内部处理与全局约束四层架构，解决规则扁平堆砌痛点（AI-Agent/prompt-engineering）
- [[概念_LLM_as_a_Judge校准]] — 引入专家黄金集、失败编码与解释理由，用对齐框架确保AI裁判评分一致（AI-Agent/eval）
- [[概念_标量过滤]] — 向量数据库中结合元数据标量属性过滤与向量检索的混合查询机制（RAG/embedding, RAG/retrieval）
- [[概念_DiskANN_磁盘图向量索引]] — 微软开源基于 SSD 磁盘的高性能 ANN 检索算法，突破内存限制（RAG/embedding, RAG/retrieval）
- [[概念_IVF_倒排索引]] — 倒排文件索引 (Inverted File Index)，基于聚类空间划分的高维向量近似最近邻搜索 (ANNS) 算法（RAG/embedding, RAG/retrieval）
- [[概念_Memex_个人机电知识扩展系统]] — Vannevar Bush 于 1945 年提出的个人机电知识设备构想，关联性路径鼻祖（Skill/knowledge-bank）
- [[概念_卡片盒笔记法]] — Zettelkasten 知识管理方法论，原子化卡片与网络化交叉引用（Skill/knowledge-bank）
- [[概念_Ingest入库闭环]] — LLM Wiki 范式中的标准化入库 SOP 操作（阅读/摘要/实体概念联动/索引日志）（Skill/knowledge-bank, AI-Agent/coding）
- Wiki健康检查 — LLM Wiki 范式中的 Lint 体检与图谱垃圾回收（Skill/knowledge-bank, AI-Agent/coding）
- [[概念_Claude_Code多智能体协同机制]] — 拆解并对比 Claude Code 的三大协同原语（Subagents、Agent Teams、Dynamic Workflows），详述动态工作流在 JS 编排执行、并发扇出、上下文解耦和抗灾恢复力方面的机制，并阐述对抗性验证（Adversarial Verification）的收敛逻辑。（ClaudeCode, Multi-Agent, Orchestration）
- [[概念_Delta_Attention与增量矩阵缓存]] — Kimi K3 采用的注意力优化机制，使用固定大小矩阵与 Delta 规则更新，实现线性计算与 $O(1)$ 空间开销
- [[概念_Pinball_Loss_分位数回归]] — 弹球损失（Pinball Loss）的定义与不对称几何拉伸推导，及多 percentile 回归与 LightGBM 区间估算的工程价值。（machine-learning, regression, loss-function）
- [[概念_Agent内存与状态管理]] — 深度对比 State 与 Memory 两个维度的定义与作用边界，构建在宿主系统（Harness Engineering）中单步 Checkpoint 与 Scope 隔离的协作逻辑。（AI-Agent/harness, AI-Agent/memory, state-management）

## Entities

- [[entities/实体_Laya]] — Convai Innovations 开源的 421M 非自回归 System 1 决策模型，采用 ModernBERT 与 RLCD 算法，以 33ms 延迟输出经过严格校准的决策概率与置信度（LLM/inference, AI-Agent/tool-calling, LLM/training/RL）
- [[entities/实体_Jev]] — TypeSafe 推出的无生成文本概率分布输出接口，将分类判断从通用大模型中解耦，主打百毫秒级确定性选择与 Agent 状态路由（LLM/inference, AI-Agent/tool-calling）
- [[实体_宝玉]] — 资深技术专家、AI 自媒体博主、《软件工程之美》专栏作者，Nano Banana 提示词作者，BaoCut 字幕工具开发者，倡导 AI 原生思维与开发者角色重构（AI-Agent/coding, AI-Agent/skill）

- [[实体_DeepSeek]] — 专注于 AGI 研发的中国 AI 创新机构，代表作包括 DeepSeek 系列基础大模型与微内核智能体生态（Infra/platform, LLM/arch）
- [[实体_美团]] — 中国领先的科技零售与本地生活平台，在搜索理解、推荐系统、AI Coding 与全栈生活服务智能体具有深厚积累（AI-Agent/coding, Recommendation）

- [[实体_LongHorizon-Harness]] — 阿里高德团队开源的长时 Agent 编排框架，通过 Manage-Execute-Audit (MEA) 循环将长任务重构为审计状态机，包裹原生 Coding Agent 以防状态腐化与虚假完成（AI-Agent/coding, AI-Agent/context-engineering）
- [[实体_zvec-grep]] — 阿里 Zvec 团队开源的 local-first 代码搜索基础设施，结合 BM25 词法检索、局部向量语义检索与 RRF 排名融合，为人类与 Agent 提供高效上下文获取（AI-Agent/coding, AI-Agent/tool-calling, RAG/retrieval）

- [[实体_Tavily]] — 专注于面向 LLM 与 RAG 的 Web Search 搜索引擎供应商，主打网页降噪、正文抽取与高信息密度文本片段压缩（AI-Agent/deep-research, RAG/retrieval）
- [[实体_Exa]] — 专注于面向 AI 与大模型的定向语义索引搜索引擎，聚焦 GitHub、ArXiv、Wikipedia 等高信息密度站点提供高质量神经搜索（AI-Agent/deep-research, RAG/retrieval）

- [[实体_anydoc]] — Firecrawl 开源纯 Rust 多格式文档转 Markdown 工具，两阶段中间稿解析与 Agent Skill 集成（AI-Agent/tool-calling, RAG/chunking）
- [[实体_Firecrawl]] — 专注于为 LLM 和 AI Agent 提取干净 Markdown 数据的开源数据管道团队（AI-Agent/tool-calling, RAG/chunking）
- [[实体_DeepSeek_Harness]] — DeepSeek 开源基于 Cordis 微内核的智能体 SDK 与应用框架，采用“一切皆插件”架构、四大预设模式与权威 Session Log（AI-Agent/harness, AI-Agent/coding）
- [[实体_Cordis]] — 支持时空可组合性的轻量级微内核框架，为 DeepSeek Harness 等智能体系统提供插件运行时底座（AI-Agent/harness, AI-Agent/coding）

- [[实体_Superlinked_Inference_Engine]] — 面向多模型流水线的开源推理服务引擎，统一 API、共享 GPU 池与按需模型加载

- [[实体_OpenAI]] — 全球顶尖人工智能实验室，GPT 系列大模型、ChatGPT、Sora 创造者与生成式 AI 时代引领者
- [[实体_DeepMind]] — Google 旗下顶尖 AI 实验室，AlphaGo、AlphaFold 与 Gemini 多模态大模型研发者
- [[实体_NVIDIA]] — 全球人工智能算力与 GPU 硬件基础架构领导企业，CUDA、TensorRT 与 Megatron 生态构建者
- [[实体_DeepSpeed]] — 分布式训练框架，ZeRO 系列策略来源
- [[实体_Megatron]] — NVIDIA 并行框架，激活值/重计算公式来源
- [[实体_R-CNN]] — R-CNN 系列，开创两阶段检测范式
- [[实体_YOLO]] — 首个单阶段检测器，YOLOv2 全面升级
- [[实体_SSD]] — 多尺度特征图单阶段检测基线
- [[实体_ResNet]] — 残差学习，检测标准 Backbone
- [[实体_SENet]] — 通道注意力，ILSVRC 最后一届冠军
- [[实体_R-FCN]] — 全卷积位置敏感检测
- [[实体_FPN]] — 特征金字塔网络，检测标配组件
- [[实体_MobileNet]] — 深度可分离卷积轻量网络，移动端部署
- [[实体_COCO数据集]] — 80 类像素级实例标注，检测/分割主流基准
- [[实体_Mask_R-CNN]] — 实例分割，提出 RoIAlign
- [[实体_SAM]] — Meta AI 图像分割基础模型
- [[实体_ViT]] — Vision Transformer，SAM 图像编码器
- [[实体_CLIP]] — 视觉-语言对齐模型，为 SAM 提供文本 Prompt
- [[实体_Albumentations]] — Python 图像增强库，OneOf/Compose 组合
- [[实体_FlashAttention]] — I/O 感知精确注意力，长上下文行业标准
- [[实体_Adam优化器]] — 一阶矩+二阶矩自适应优化器，深度学习常用选择
- [[实体_PyTorch]] — 深度学习框架事实标准，动态计算图/自动微分/Python 优先
- [[实体_vLLM]] — 开源 LLM 推理框架，KV Cache/连续批处理/PagedAttention
- [[实体_Mechanize]] — RL 环境平台，复制训练（Replication Training）范式
- [[实体_Fireworks_AI]] — AI Inference Infra 公司，RFT 产品化
- [[实体_LangChain]] — LLM/RAG 应用框架，链式串联检索与生成（medium）
- [[实体_Qdrant]] — Rust 编写的开源向量数据库/向量搜索引擎（medium）
- [[实体_ColBERT]] — 斯坦福 token 级细粒度检索模型，MaxSim late interaction
- [[实体_LlamaIndex]] — LLM/RAG 应用框架，文档加载与切分（medium）
- [[实体_Qwen3_Embedding]] — Qwen3 系列嵌入/重排模型，MTEB 排名第一，Instruct+LLM化Rerank
- [[实体_Sentence_Transformers]] — 嵌入模型训练/推理框架，Matryoshka/Instruct 支持
- [[实体_BGE-M3]] — BAAI 多语言嵌入模型，1024 维，同时支持 dense 和 ColBERT 多向量
- [[实体_Elasticsearch]] — 全文+原生向量搜索引擎，混合检索/RRF/量化/Serverless
- [[实体_Faiss]] — Facebook 开源向量检索库，丰富索引算法+GPU 加速
- [[实体_HNSW]] — 分层可导航小世界图，毫秒级 ANN 业界主流
- [[实体_Docling]] — IBM 开源 PDF 解析库，RAG 挑战赛最佳解析器
- [[实体_Cohere_Rerank]] — Cohere 重排序 API，CohereRerank top-k 精排（medium）
- [[实体_美团搜索]] — 美团App搜索，查询改写全栈实践，覆盖率73%，QPS 6万/秒
- [[实体_优图实验室]] — 腾讯AI实验室，RAG全栈方案，apd-embedding-2b/MAC-SQL/GraphRAG
- [[实体_MAC-SQL]] — 多智能体Text2SQL框架，Selector/Decomposer/Refiner（COLING 2025）
- [[实体_通义千问]] — 阿里大语言模型，RAG生成/判别核心模型（medium）
- [[实体_RAGAS]] — RAG 系统开源评估框架，多维度指标
- [[实体_Mamba]] — Mamba 选择性状态空间模型，线性时间序列建模（LLM/arch/Mamba）
- [[实体_Mamba2]] — Mamba2 SSD 框架，SSM 与 Attention 大一统，ICML 2024（LLM/arch/Mamba）
- [[实体_S4]] — Structured State Space for Sequences，Mamba 前置架构（LLM/arch/Mamba）
- [[实体_Albert_Gu]] — Mamba/S4/HiPPO 核心作者，CMU 助理教授，Cartesia AI 联创（LLM/arch/Mamba）
- [[实体_Tri_Dao]] — FlashAttention/Mamba 作者，Princeton 助理教授（LLM/arch/Mamba）
- [[实体_腾讯混元TurboS]] — 业界首个大规模部署的 560B Hybrid Transformer-Mamba MoE 模型（LLM/arch/Mamba, LLM/arch/MoE）
- [[实体_DeepSeek-V3]] — DeepSeek 旗舰 MoE 模型，MLA+256专家+共享专家架构（LLM/arch/MoE）
- [[实体_Kimi_K2]] — 月之暗面 1T 参数开源 MoE 模型，Muon 优化器，基于 DeepSeek-V3 架构（LLM/arch/MoE）
- [[实体_Gemma系列]] — Google DeepMind 研发的开源大模型家族，涵盖 Gemma 1/2/3 及端侧 Gemma 3n（LLM/arch）
- [[实体_LLaVA]] — 大道至简多模态系列：极简连接器 + AnyRes（LLM/arch/VLM）
- [[实体_Qwen3-VL]] — 阿里 DeepStack + MoE 深度融合多模态模型（LLM/arch/VLM）
- [[实体_MiniMax_M2]] — MiniMax 2025 旗舰，回归 Full Attention，Agent/代码定位（LLM/arch/attention）
- [[实体_Kimi_Linear]] — 月之暗面开源 48B 混合注意力：KDA+MLA 3:1，KV Cache 减少 75%（LLM/arch/attention）
- [[实体_DeepSeek_V2]] — DeepSeek MLA 首发模型（LLM/arch/attention）
- [[实体_Medusa]] — Medusa 推测解码框架：多 FFN Head 并行预测与树状注意力验证（LLM/inference）
- [[实体_EAGLE]] — 基于倒数第二层特征隐状态预测的高效推测解码推理加速框架（LLM/inference）
- [[实体_Qwen3]] — 阿里 Qwen3：SFT 混合思考 + Thinking Budget 涌现（LLM/reasoning）
- [[实体_DeepSeek-R1]] — DeepSeek 推理模型，GRPO+四阶段训练，AIME 79.8%，与 o1-1217 相当（LLM/reasoning, LLM/training/RL）
- [[实体_Unsloth]] — 开源高效 LLM 微调框架，支持 GRPO 训练推理模型，GitHub 4万星（LLM/training/RL, Skill/python）
- [[实体_SmolLM3]] — HuggingFace 3B 开源模型，384×H100 训练 11T tokens，GQA+RNoPE 架构（LLM/training/pre-train）

### LLM/面试/创业/RL（批次9）
- [[实体_Jina_AI]] — 专注搜索底座模型 AI 初创，2020-2025，两次 Pivot 后被 Elastic 收购（创业）

### LLM/Recommendation + arch（Batch 10）
- [[实体_淘天AIGC团队]] — 淘天集团直播AIGC团队，数字人直播完整链路（LLM）

### LLM/training + hallucination（批次7）
- [[实体_翁荔_Lilian_Weng]] — 前 OpenAI 安全研究 VP、Thinking Machines Lab 联合创始人，Lil'Log 作者，Agent 公式 + Harness Engineering 提倡者（LLM/hallucination, AI-Agent/harness）
- [[实体_PEFT库]] — HuggingFace 参数高效微调库，LoRA/QLoRA/Adapter/Prefix 支持（LLM/training/post-train）

### LLM/training/post-train（批次6）
- [[概念_DPO_直接偏好优化]] — 直接偏好优化，无需显式训练奖励模型，直接通过人类偏好数据优化策略模型 (LLM/training/post-train)
- [[HuggingFace手把手训练大模型实战指南]] — SmolLM3 端到端训练实战：Why→What→How + 架构/数据/基础设施全链路（LLM/training/pre-train, post-train）
- [[SFT数据挑选方法_质量多样性必要性]] — SFT 数据三维度筛选：MoDS/DEITA/CaR 方法梳理（LLM/training/post-train）
- [[375篇文献_推理大模型后训练技术综述]] — 后训练三分类综述：微调/RL/测试时扩展（LLM/training/post-train）
- [[LLM后训练技术全景解读]] — 全景解读后训练：PEFT/LoRA/Prompt Tuning/PPO/DPO/GRPO/CoT/ToT（LLM/training/post-train）

### AI-Agent/context-engineering（Phase 4 Batch 3）
- [[概念_上下文工程]] — 动态系统填充恰好合适的信息给LLM，四类操作：Offload/Retrieve/Reduce/Isolate（AI-Agent/context-engineering）
- [[概念_Context_Rot_上下文衰退]] — 上下文腐化：长度增长导致性能下降，预腐化阈值128K-200K，触发压缩/总结（AI-Agent/context-engineering）
- [[概念_分层行动空间]] — Manus三层工具架构：函数调用/沙盒工具集/软件包API，稳定接口+无限能力（AI-Agent/context-engineering）
- [[概念_Spec_Driven_Development_规范驱动开发]] — 规范驱动开发：Prompt→Requirements→Design→Tasks→Code，Kiro 实现（AI-Agent/context-engineering）
- [[概念_RLM递归语言模型]] — 介绍由 MIT 提出的递归语言模型架构，核心是将数据与指令解耦，通过 REPL 缓存上下文，LLM 采用 Peek/Grep/Partition 进行自上而下的递归调用分治，解决 Context Rot。（AI-Agent/recursive-language-models, AI-Agent/context-engineering）

### AI-Agent/coding（Phase 4 Batch 4）
- [[概念_Agent开发范式三级进化]] — Level 1 LLM/Level 2 AI Agent/Level 3 Multi-Agent 三阶段演进，Human in the Loop 作为特殊 Agent（AI-Agent/coding）
- [[概念_Agent三层记忆体系]] — 感知记忆（标签页级）/短期记忆（Session+ES）/长期记忆（知识点+用户画像+经验图谱）（AI-Agent/coding）

### AI-Agent/coding+skill（Phase 4 Batch 5）
- [[概念_私域知识工程]] — 将项目专属知识系统化文档化，解决 AI 与真实项目信息不对称，三板斧：入职培训/知识驱动编程/自动维护（AI-Agent/coding）
- [[概念_LLM应用评估体系]] — LLM 应用评估方法论：断言式单元测试/LLM 裁判最佳实践/实习生测试/古德哈特定律（AI-Agent/coding）
- [[概念_Agent_Skills元工具架构]] — Skills = 提示词模板+上下文注入+执行上下文修改，纯 LLM 推理选择，双消息 isMeta 机制，渐进式披露（AI-Agent/skill）
- Agentic设计模式分类 — 21种 Agent 设计模式四大类：核心（提示链/路由/并行化/反思/工具/规划/多智能体）/高级/集成/生产（AI-Agent/skill）

### AI-Agent/memory（Phase 4 Batch 7）
- [[概念_AI_Agent记忆策略]] — 8 种主要策略原理（全量/滑动窗口/相关性过滤/摘要/向量DB/知识图谱/分层/类OS），翁荔学术分类框架与前沿系统（AI-Agent/memory）

### AI-Agent/prompt-engineering（Phase 4 Batch 7）
- 编程提示工程实战 — 程序员向 10 种技巧+7 条基础原则+调试/重构/功能三场景策略+常见反模式（AI-Agent/prompt-engineering）

### AI-Agent/AI-BI（Phase 4 Batch 8）

### AI-Agent 综合 + AI-BI（Phase 4 Batch 9）
- [[概念_Agent系统化工程]] — 三层复杂度+LLM放大效应+Level 0-4认知演化+系统化方法论（AI-Agent）
- [[概念_LLM不确定性放大]] — 多步调用的指数级错误放大数学模型及三类放大维度（AI-Agent）
- [[概念_AI_Ready_Data_AI就绪数据]] — NL2SQL落地第一性问题：元数据/业务语义/权限/样例SQL的系统化准备（AI-Agent/AI-BI）
- [[概念_M_Schema_增强元数据模式]] — NL2SQL增强Schema表示：补充类型/中文释义/真实值示例+约束池（AI-Agent/AI-BI）
- [[概念_Schema_Linking_数据库模式联接]] — BM25粗排+SIC精排两级联接，从全量Schema筛选相关表列，幻觉率-78%（AI-Agent/AI-BI）

### Skill/python（Phase 5 Batch 1）
- [[概念_FastAPI项目结构模式]] — Routers/Schemas/Services 三层分离 + 安全中间件 + pydantic-settings（Skill/python）
- [[概念_Python_async_await并发]] — 协程/并发vs并行（汉堡比喻）/FastAPI def vs async def 选择（Skill/python）
- [[概念_uv包管理器]] — Rust 编写 pip 替代品，pyproject.toml+uv.lock，Docker 集成 10x 提速（Skill/python）
- [[概念_Python循环优化技巧]] — 12 种 for 循环优化方法与提速比，map/set/lru_cache/filterfalse（Skill/python）
- [[概念_Python函数式工具]] — map/lru_cache/filterfalse/Generator，C 实现替代显式循环（Skill/python）
- [[概念_Python进阶特性]] — suppress/setrecursionlimit/Literal/__missing__/__subclasshook__（Skill/python）
- [[概念_Python并发与并行机制]] — 未分类概念摘要（python, concurrency, parallelism, gil, programming）
- [[概念_Python描述符]] — Python 描述符（Descriptors）是实现底层属性代理的核心机制。通过控制属性的获取、修改和名称绑定，它能有效解决传统 @property getter/setter 机制在多属性校验时的代码冗余，并能在对象初始化时直接进行拦截校验。（python, oop, descriptor）
- Python模块与包管理 — 未分类概念摘要（python, engineeringpractices, moduleandpackage）

### Skill/data-analysis（Phase 5 Batch 2）
- [[概念_EDA_自动化分析工具]] — 10 个自动 EDA 包四类分类（报告/可视化/定制/ML 集成）与选型建议（Skill/data-analysis, Skill/python）
- [[概念_Pandas可视化]] — DataFrame.plot/Series.plot 内置绘图 + pandas.plotting 高级可视化（Skill/data-analysis）
- [[概念_Pandas核心操作图解]] — 选择/排序/分组/合并/变形/索引 + NumPy 对比关键差异（Skill/data-analysis, Skill/python, 面试）
- matplotlib样式美化 — dufte 主题/图例/柱标注三 API，一行代码商务风图表（Skill/data-analysis）

### Skill/linux（Phase 5 Batch 3）
- Linux命令分类速查 — 28 大类 600 条 Linux 命令按场景分组速查体系（Skill/linux）

### Life（Phase 5 Batch 3）
- 幸福积分模型 — 幸福总量=曲线下面积（积分），时间度量衡，等周不等式类比（Life）
- 天职Calling — 本身能带来快乐的工作，三条筛选标准，天职不是"钱多事少离家近"（Life）

### Life（Phase 6 Batch 5：旅行/驾驶/投资/驱蚊/智能家居）
- [[概念_投资反馈机制]] — 选正常市场获有效反馈，不正常市场无法纠错成长（Life）
- [[概念_投资风格确立]] — 缩小决策解空间，固定 1-2 种最舒服模式长期精进（Life）
- [[概念_驱蚊有效成分]] — DEET/Picaridin/IR3535/OLE 四成分，含量影响有效时间非效果（Life）
- [[概念_DEET避蚊胺]] — 教科书级驱蚊成分，浓度边际效应，分龄安全建议（Life）

### Batch 3 (XGBoost+SHAP / Identity & Ego)
- [[概念_SHAP模型可解释性]] — 基于 Shapley 值的加性归因解释，支持小提琴/热力/瀑布/依赖图（Skill/data-analysis, Skill/python）
- [[概念_有限与无限的游戏]] — James Carse 哲学二元模型，区分胜负导向有限游戏与延续探索无限游戏（Life, 创业）

### AIGC（Phase 6 Batch 1）
- [[概念_PPT生成提示词]] — 用结构化提示词控制 AI 生成 PPT/封面的风格/配色/排版，三维度描述法（AIGC）
- [[概念_HTML代码方式生成视觉物料]] — LLM 输出 HTML+CSS 代码渲染视觉物料，可控性强、可复用（AIGC）
- [[概念_AI_PPT工具路径]] — AI 原生派（Gamma 对话生成）vs 传统革新派（WPS AI 润物细无声）（AIGC）
- AI产品最后一公里 — AI PPT 从「能用」到「可交付」的 gap：二次编辑+格式导出兼容（AIGC）

### AIGC（Phase 6 Batch 2）
- [[概念_Nano_Banana_Pro论文绘图工作流]] — 架构师→渲染器→编辑器三步工作流；VISUAL SCHEMA 五种布局原型；禁止用于实验数据图表（AIGC）
- [[概念_Nano_Banana图像生成提示词]] — 描述场景而非关键词；摄影师/设计师思维；六大生成+四大编辑场景完整模板（AIGC）
- [[概念_人与大模型协作]] — Gemini 三大启示：思想催化剂/认知谦逊/Knowing-Why；GPT-5 补充：三颗钉子+错账本（AIGC）
- [[概念_Vibe_Coding三阶段]] — 初级原型/中级重构/高级整体-细节-整体循环；UI/UX 不适合 AI 直接生成（AIGC）
- [[概念_文生视频提示词公式]] — 基础/进阶/图生视频三套公式；主体+场景+运动+美学控制+风格化（AIGC）
- [[概念_视频美学控制词典]] — Wan2.2 九大维度完整词典：光源/光线/时间/景别/构图/焦段/运镜/风格/特效（AIGC）

### TTS（Phase 6 Batch 2）
- [[概念_TTS_直播数据处理管线]] — 语音信号处理/语音理解/说话人聚类三环节漏斗；利用直播回放替代录制素材（TTS）
- [[概念_TTS两阶段架构]] — 前端文本归一化+后端语言模型/声学模型/声码器；Encodec偏声学/HuBERT偏语义（TTS）
- [[概念_TTS_韵律情感拟人化]] — 显式停顿@/拖音→标签控制韵律；参考音频情感注入高低音变化；个性化韵律表（TTS）

### Recommendation（Phase 6 Batch 2）

### 创业（Phase 6 Batch 3）
- [[概念_Foundation_Sprint_基础冲刺]] — Jake Knapp 超早期项目战略奠基流程：10 小时三阶段，产出创始假设（创业）
- [[概念_Design_Sprint_设计冲刺]] — 五天产品验证冲刺：Map/Sketch/Decide/Prototype/Test + Scorecard 计分卡（创业）
- [[概念_差异化2x2分析]] — Foundation Sprint 差异化工具：经典+自定义因素，2x2 独占右上角避开"失败者村"（创业）
- [[概念_Magic_Lenses魔术镜头]] — 五种专家视角（客户/务实/增长/财务/差异化）评估执行路径（创业）
- [[概念_先思考再行动]] — AI 时代先做战略思考再开发：快是陷阱、AI 致平庸、思考不可外包（创业）

### 创业（Phase 6 Batch 4）
- [[概念_PMF引擎]] — Superhuman 四步法：精准细分/分析反馈/规划路线图/重复迭代，量化优化 PMF（创业）
- [[概念_Sean_Ellis_PMF指标]] — "非常失望"比例 40% 门槛：PMF 领先指标（创业）
- [[概念_Bundle理论]] — Shishir Mehrotra：三种用户/MCC 分成/刚需错开非刚需重叠/2x2 矩阵（创业）
- [[概念_Unbundle_Rebundle规律]] — 技术 unbundle 切入市场/商业 rebundle 捕获价值/集装箱类比 AI（创业）
- [[概念_AI初创高人效模式]] — Leonis AI 100：极简扁平团队人均百万美元 ARR，轻人力重算力数据（创业）
- [[概念_GTM_倒漏斗模式]] — AI 初创：PLG 先行验证价值，销售后置正式化已存在需求（创业）
- [[概念_AI市场阈值解锁]] — AI 市场按序爆发：模型突破关键阈值才解锁新品类（创业）
- [[概念_研究型创始人崛起]] — 86% 技术创始人/82% 技术 CEO，研究型创始人预判能力突破（创业）

### 创业（Phase 6 Batch 5：AI 独立开发）
- AI独立开发方法论 — 艾逗笔五条感悟（快/精/小切入/造血/流量）+ 出海 SOP + 四 all in 方向（创业）

### AI-Agent/deep-research（Phase 4 Batch 6）
- [[概念_Deep_Research_Agent_定义与分类]] — DR Agent 定义、与 RAG/Tool Use 的边界、规划策略三模式（Planning-Only/Intent-to-Planning/Unified）（AI-Agent/deep-research）
- [[概念_Deep_Research_四大挑战]] — 信息窄门/幻觉不可靠/线性效率瓶颈/评测错位，及对应未来方向（AI-Agent/deep-research）
- [[概念_Deep_Research_四类实现架构]] — 单体/流水线/多智能体/混合四种架构对比与代表系统（AI-Agent/deep-research）
- [[概念_IterResearch范式]] — 通义 DeepResearch 创新范式：精简工作空间+核心报告迭代重构，解决上下文认知瓶颈（AI-Agent/deep-research）
- [[概念_WebFrontier数据合成]] — 种子-扩展-评估三步数据合成，知识图谱随机游走+原子操作难度建模（AI-Agent/deep-research）

### AI-Agent/harness & Skill/knowledge-bank（Batch 2）
- [[概念_Harness_Engineering_宿主编排工程]] — 围绕基础模型构建的宿主与编排系统工程，编排执行/思考/工具/上下文/产物与评估（AI-Agent/harness, AI-Agent/coding）
- [[概念_RSI递归自我改进]] — AI 系统自我迭代优化机制，现代 Agent 范式通过 Harness 优化而非直接改写权重（RSI）
- [[概念_Harness优化阶梯]] — Agent 系统优化对象五级演进：Prompt -> 结构化上下文 -> 工作流 -> Harness 代码 -> 优化器代码（RSI, AI-Agent/context-engineering）
- [[概念_Self_Harness_自主进化宿主系统]] — AI 自我改进工程闭环，通过“弱点挖掘—修改提议—保留集验证”确保 Harness 代码持续进化（RSI, AI-Agent/coding）
- [[概念_假性死链鉴别]] — 图谱审计中死链三维甄别法：命名不匹配重定向、多余路径前缀去前缀化、待建节点按需生长（Skill/knowledge-bank）
- [[概念_级联清理安全边界]] — 物理底座删除时的级联清理红线，包含上下文半衰期解耦与行内安全感知（Inline Safety Sensing）（Skill/knowledge-bank）
- [[概念_单向推导数据管线]] — LLM Wiki 数据流向纪律：raw/ -> wiki/sources/ -> wiki/entities|concepts，严禁末端产物越级直连 raw/（Skill/knowledge-bank）
- AI工程技术栈全景_2026 — 系统梳理并详细阐释 2026 年 AI 工程师的 10 层技术栈全景与核心组件，总结从单点 Prompt 调试向 Harness & Loop 架构体系演进的宏观趋势。（AI-Engineering, LLMOps, System-Architecture）

### 代码强化学习与 Reward Hacking（Ingest Batch 4）
- [[概念_代码强化学习]] — 利用测试套件 pass/fail 可验证奖励进后训练，激活长程规划元能力但易诱发作弊（LLM/training/RL, AI-Agent/coding）
- [[概念_Hardened_Sandbox_强化隔离沙盒]] — 移走 `.git` 版本历史与物理隔离断网的强化沙盒评测规范，防范模型检索与历史提交作弊（LLM/training/RL, AI-Agent/eval）
- [[概念_Inoculation_Prompting_接种提示词]] — Anthropic 提出训练集中注入接种提示词重构奖励篡改语义，消除安全掩盖副作用（LLM/training/RL）

### Agent Skill 系统化评价（Ingest Batch 4）
- [[概念_Agent_Skill系统化评价框架]] — 覆盖触发路由、执行轨迹、产物质量、效率成本、安全权限、可复用性六维评估体系（AI-Agent/skill, AI-Agent/eval）
- [[概念_Skill增量收益评估]] — 对比加载 Skill 与原生 Agent（With vs Without Skill）边际提升的第一性准则（AI-Agent/skill, AI-Agent/eval）
- [[概念_Skill误触发与漏触发评价]] — 兼顾评估漏触发（False Negative）与误触发（False Positive），结合 Precision/Recall 权衡（AI-Agent/skill, AI-Agent/eval）

### AI-Agent/tool-calling MCP系列（Phase 4 Batch 1）
- [[实体_David_Soria_Parra]] — Anthropic 工程师，MCP 协议联合创建者，五大原语与 Web 化主导者（AI-Agent/tool-calling）
- [[实体_Anthropic_Research系统]] — Anthropic Claude Research 多智能体研究系统，Opus 4 + Sonnet 4 orchestrator-worker（AI-Agent/multi-agent）

### AI-Agent/context-engineering（Phase 4 Batch 3）
- [[实体_Peak_Ji_季逸超]] — Manus 联合创始人，MIT TR35 2025，上下文工程六大原则提出者（AI-Agent/context-engineering）
- [[实体_Manus]] — 通用AI Agent，上下文工程实践标杆，KV缓存/分层行动空间/文件系统记忆（AI-Agent/context-engineering）

### AI-Agent/coding（Phase 4 Batch 4）

### AI-Agent/skill（Phase 4 Batch 5）

### AI-Agent/deep-research（Phase 4 Batch 6）
- [[实体_通义DeepResearch]] — 阿里通义实验室开源 Web Agent，30B MoE，HLE 32.9/BrowseComp-EN 43.4，IterResearch+ReAct 双模式（AI-Agent/deep-research）

### AI-Agent/memory（Phase 4 Batch 7）

### AI-Agent/AI-BI（Phase 4 Batch 8）
- [[实体_腾讯OlaChat]] — 腾讯 PCG 智能数据分析平台，多任务对话+DAG编排+Text2SQL(70B)+元数据RAG（AI-Agent/AI-BI）

### AI-Agent 综合 + AI-BI（Phase 4 Batch 9）
- [[实体_LangSmith]] — LangChain 可观测性平台：可视化 Trace/调试/测试评估，Agent 复现性关键工具（AI-Agent）
- [[实体_Qwen2.5-Coder]] — 阿里代码专用模型3B/7B，NL2SQL LoRA 精调基座，实测EX提升+6.4%（AI-Agent/AI-BI）


### Skill/python（Phase 5 Batch 1）
- [[实体_FastAPI]] — Python 高性能 Web 框架，基于 Starlette/Pydantic，原生 async/await，性能与 Go 不相上下（Skill/python）
- Python模块与包管理 — 未分类概念摘要（python, engineeringpractices, moduleandpackage）

### Skill/data-analysis（Phase 5 Batch 2）
- [[实体_Pandas]] — Python 数据分析核心库，基于 NumPy，Series/DataFrame + groupby/merge/pivot/plot（Skill/data-analysis, Skill/python）
- [[实体_Dataprep]] — 开源 Python EDA 包，基于 Pandas+Dask，自动 EDA 中速度最快（Skill/data-analysis, Skill/python）

### Life（Phase 6 Batch 5：旅行/驾驶/智能家居）

### AIGC（Phase 6 Batch 1）
- [[实体_Gemini]] — Google AI 助手，PPT 生成/深度研究/搜索，Veo 3 使用前提（AIGC）
- [[实体_Gamma]] — AI 原生 PPT 工具先行者，对话生成卡片式演示文稿（AIGC）
- [[实体_Genspark]] — 通用型超级智能体，PPT 为附属功能，图片引用缺失问题（AIGC）

### AIGC（Phase 6 Batch 2）
- [[实体_Nano_Banana_Pro]] — Gemini 2.5 Flash Image 别名，原生多模态/强角色一致性/对话式编辑，学术绘图最佳选择（AIGC）
- [[实体_通义万相Wan2.2]] — 阿里通义文生视频模型，三套提示词公式+九大维度美学控制词典（AIGC）

### TTS（Phase 6 Batch 2）
- [[实体_CosyVoice]] — 阿里通义开源 TTS 模型，V4 融合 CosyVoice2+Qwen2.5-0.5B+vLLM，相似度 0.93（TTS）

### Recommendation（Phase 6 Batch 2）

### 创业（Phase 6 Batch 3）
- [[实体_Jake_Knapp]] — Design Sprint 创造者，前 Google Ventures 设计合伙人，Character Capital 联创（创业）
- [[实体_Character_Capital]] — Jake Knapp 与 John Zeratsky 创立的风投，专注 0 阶段超早期项目（创业）

### 创业（Phase 6 Batch 4）
- [[实体_Superhuman]] — AI 邮件客户端，PMF 引擎标杆，ARR 3500 万美元，被 Grammarly 收购（创业）
- [[实体_Rahul_Vohra]] — Superhuman 创始人兼 CEO，PMF 引擎方法论提出者（创业）
- [[实体_Grammarly]] — 嵌入式 AI 写作工具，年收入超 7 亿美金，收购 Coda+Superhuman 后改名（创业）
- [[实体_Shishir_Mehrotra]] — Coda 创始人，新 Superhuman 集团 CEO，Bundle 理论实践者（创业）

### 创业（Phase 6 Batch 5：AI 独立开发）
- [[实体_Claude_Code]] — Anthropic 终端 AI Coding 命令行工具，在 LLM Wiki 中担任知识编译“大脑”（AI-Agent/coding, Skill/claude-code）
- [[实体_Obsidian]] — 本地优先 Markdown 知识库软件，通过 Graph View 图谱与 MCP 充当人类认知“IDE”（Skill/knowledge-bank）
- [[实体_DSPy]] — 斯坦福开源的声明式框架，将提示工程转化为程序编译与 GEPA 误差驱动优化（AI-Agent/eval, AI-Agent/prompt-engineering）
- [[实体_Andrej_Karpathy]] — 著名人工智能科学家与教育者，LLM Wiki 知识编译与复利范式提出者（DeepLearning, AI-Agent/coding）
- [[实体_Dropbox]] — 知名云同步协作与 AI 工作台公司，在 Dash Chat 中实现对准评估与自动迭代双赢（AI-Agent/eval, AI-Agent/prompt-engineering）
- [[实体_Milvus]] — 开源云原生分布式向量数据库，存算分离架构，支持十亿级海量向量数据（RAG/embedding, Infra/storage）
- [[实体_pgvector]] — PostgreSQL 开源向量检索扩展插件，支持原生 SQL 向量查询（RAG/retrieval, Skill/python）
- [[实体_Redis]] — 内存 Key-Value 数据库与 RediSearch 内存级超低延迟向量检索（RAG/retrieval, Infra/storage）
- [[实体_Chroma]] — 开源轻量级嵌入式向量数据库，极简 Python 安装，适合本地 PoC（RAG/retrieval, Skill/python）
- [[实体_Pinecone]] — 商业闭源全托管 SaaS 向量数据库服务，免运维快速上线（RAG/retrieval, Infra/storage）
- [[实体_Weaviate]] — 开源一体化向量搜索引擎，基于 HNSW 索引与 GraphQL 查询（RAG/retrieval, Infra/storage）
- [[实体_Vannevar_Bush]] — 美国工程师，1945 年提出 Memex 个人知识设备构想，关联性路径鼻祖（Skill/knowledge-bank, DeepLearning）
- [[实体_Niklas_Luhmann]] — 德国社会学家，卡片盒笔记法 (Zettelkasten) 集大成者，9万张索引卡（Skill/knowledge-bank）
- [[实体_Thinking_Machines_Lab]] — 前 OpenAI 安全研究 VP Lilian Weng 等联合创办的前沿 AI 研究实验室（AI-Agent/harness）
- [[实体_Hugo_Yang]] — 本知识库搭建者与架构维护者（Skill/knowledge-bank）
- [[实体_vault_lint]] — 知识库自动化治理与诊断 Python 工具（`scripts/vault_lint.py`）（Skill/knowledge-bank）
- [[实体_Codex]] — OpenAI 代码生成与编码智能体系统（AI-Agent/coding）
- [[实体_XGBoost]] — 基于梯度提升决策树（GBDT）的高性能开源算法框架（Skill/python, Skill/data-analysis）
- [[实体_SHAP]] — 基于博弈论 Shapley Additive exPlanations 的 Python 模型可解释性分析库（Skill/python, Skill/data-analysis）
- [[实体_Matplotlib]] — Python 基础且最广泛使用的数据可视化绘图库（Skill/python, Skill/data-analysis）
- [[实体_鸭哥]] — 科技博主与技术创作者，关注前沿模型训练与代码强化学习作弊深度解析（LLM/training/RL）
- [[实体_Cursor]] — AI 代码编辑器团队，揭示 SWE-bench Pro 上代码 RL 作弊与强化沙盒评测分数塌方现象（AI-Agent/coding）
- [[实体_SWE-bench_Pro]] — 评估软件工程智能体解决真实 GitHub Issue 能力的权威代码基准评测集（AI-Agent/coding, AI-Agent/eval）
- [[实体_GLM系列]] — 智谱 AI 研发的通用大语言模型家族，涵盖 GLM-4 与前沿 GLM-5 体系（LLM/arch）
- [[实体_GPT系列]] — OpenAI 旗舰大语言模型家族，涵盖 GPT-4、GPT-5 体系及衍生推理模型（LLM/arch）
- [[实体_Coggle]] — Coggle 数据科学社区，关注数据科学、算法竞赛与 Agent 能力工程化实战（AI-Agent/skill）
- [[实体_Anthropic]] — 安全导向前沿 AI 研究实验室，研发 Claude 系列模型、Agent Skills 元工具架构与接种提示词（AI-Agent/skill, LLM/arch）

### 机器学习与数据科学基础（Batch Ingest）
- [[概念_t_SNE_降维算法]] — t-SNE 是一种流形学习降维与二维可视化算法。其 CPU 计算具有 O(N²) 二次方复杂度瓶颈，大样本下极其缓慢。tSNE-CUDA 可提供高达 700 倍的 GPU 极速提升，但目前硬件上仅支持生成二维投影（n_components=2）。（ML/dimension-reduction, t-SNE, GPU/acceleration）
- 不平衡数据的kNN优化 — 未分类概念摘要（machinelearning, knn, imbalanceddata）
- [[概念_PCA_主成分分析]] — 未分类概念摘要（machinelearning, dimensionalityreduction, mathematics）
- [[概念_稀疏随机投影]] — 基于 Johnson-Lindenstrauss 引理的线性降维算法，以稀疏随机矩阵突破 PCA 的三次时间复杂度瓶颈，在超高维场景近乎保持欧氏距离与下游任务质量（Skill/data-analysis, DeepLearning）
- 交替注意力_Alternating_Attention — 交替注意力（Alternating Attention）是 ModernBERT 采用的记忆体高效注意力机制，通过在每三层交替使用一层全局注意力与滑动窗口局部注意力（128个最近 token），打破了传统 BERT 全局注意力二次方复杂度的瓶颈。（attentionmechanism, modernbert, efficiency）
- 分块阻断技术_Blocking — 未分类概念摘要（datadeduplication, computerscience, optimization, algorithm）
- [[概念_分类模型校准]] — 未分类概念摘要（machine-learning, deep-learning, model-calibration, probability-estimation）
- [[概念_双编码器与交叉编码器]] — 阐述了成对句子评分（Pairwise Sentence Scoring）中双编码器（Bi-encoders）与交叉编码器（Cross-encoders）的机制差异、优劣势及应用场景，并简要介绍了结合两者的 AugSBERT 架构。（sentencesimilarity, biencoder, crossencoder, nlp）
- [[概念_Memory_Pinning_固定内存]] — 未分类概念摘要（deep-learning, pytorch, gpu, performance-tuning）
- 学习曲线 — 学习曲线（Learning Curve）是评估机器学习模型表现是否随数据量增加而提升的重要诊断工具。它能帮助开发者科学决策是否需要投入成本收集更多数据，诊断模型当前是处于高方差还是高偏差阶段。（machinelearning, modeldiagnostics, learningcurve）
- 数据科学核心数学定义 — 整理并阐述了数据科学与机器学习中常用的核心数学定义，包括极大似然估计 (MLE)、标准分数 (Z-score)、最小二乘法 (OLS)、熵 (Entropy)、特征值与特征向量、R方系数 (R-squared)、KL散度、奇异值分解 (SVD) 以及拉格朗日乘子法。（data-science, mathematics, statistics, linear-algebra）
- 数据集变量分类 — 未分类概念摘要（statistics, machine-learning, variable-types）
- 无标签聚类评估指标 — 系统总结和对比了三种无标签（无监督）聚类评估指标：轮廓系数（Silhouette Coefficient）、Calinski-Harabasz 指数（CH指数）以及基于密度的聚类验证（DBCV），分析了它们的物理含义、数学算式、计算复杂度及适用场景。（machinelearning, clustering, evaluation, unsupervisedlearning）
- [[概念_机器学习损失函数]] — 未分类概念摘要（machinelearning, lossfunction, optimization）
- 机器学习模型生产环境测试 — 机器学习模型在生产环境中的五种主流测试与部署策略，包括 A/B 测试、金丝雀测试、交叉测试、影子测试以及多臂强盗（MAB）部署，旨在降低新模型上线风险并评估真实环境表现。（MLOps, machinelearning, modeltesting）
- 梯度提升决策树_GBDT — 未分类概念摘要（machinelearning, ensemblelearning, gbdt, supervisedlearning）
- [[概念_Gradient_Accumulation_梯度累积]] — 梯度累积（Gradient Accumulation）是一种在硬件显存受限时，通过多次前向和反向传播累积梯度，再统一执行一次参数更新，从而在逻辑上等效实现大 Batch Size 训练的优化技术。（deeplearning, pytorch, optimization, training）
- [[概念_神经网络训练优化综述]] — 汇总并分类总结了神经网络训练中的16种常见优化技术，涵盖硬件加速、混合精度、并行策略、显存管理、动量优化及 I/O 加载等维度，旨在建立起神经网络优化的大图景。（deeplearning, neuralnetwork, optimization, training）
- 稀疏注意力 — 未分类概念摘要（deeplearning, llm, attentionmechanism, sparseattention）
- 类别特征编码技术 — 未分类概念摘要（machine-learning, feature-engineering, data-preprocessing, representation-learning）
- 训练验证测试集划分 — 规范化阐述机器学习中训练集、验证集和测试集的三阶段划分职责，分析验证集过拟合瓶颈，介绍 K 折交叉验证与嵌套交叉验证（Nested CV）的原理流向，并针对时序、不平衡、分组及数据预处理等复杂场景给出具体的防泄漏划分准则。（machinelearning/evaluation, machinelearning/methodology）
- 跨模型嵌入对比局限 — 未分类概念摘要（machinelearning, embedding, vectorspace, representationlearning）

### 机器学习与数据科学基础（Batch Ingest）
- Agentic_RL环境与GRPO — 未分类概念摘要（ReinforcementLearning, AIAgents, Infrastructure, GRPO）
- [[概念_Claude_Code核心配置与原语]] — 未分类概念摘要（ClaudeCode, AITools, ConfigArchitecture）
- 周期性特征编码 — 周期性特征在时序中的表现，传统线性编码的边界缺陷，Sine/Cosine 双通道单位圆投影映射及其等距几何优势推导。
- 大模型蒸馏的容量匹配法则 — 在微调/蒸馏小模型时，使用顶级大模型作为教师生成合成数据，其效果反而可能比不上中等教师模型这一“反直觉”容量匹配法则。（distillation, knowledge-transfer, fine-tuning）
- [[概念_GEPA提示词进化算法]] — 详细定义 GEPA 无梯度提示词进化算法，阐述其如何通过自然语言反思与 Pareto 采样避免强化学习的标量信号压缩瓶颈，并横向对比其他提示词优化技术。（gepa, prompt-tuning, rl, dspy）

### 机器学习与数据科学基础（Batch Ingest）
- [[概念_Breathing_KMeans算法]] — Breathing KMeans 是一种解决传统 KMeans 初始化敏感和重训高耗时的聚类算法。它通过动态的“吸气”（在误差大的质心附近分裂出新质心）和“呼气”（合并并删除低效用的紧邻质心）循环，实现速度和准确性的双重提升。（MachineLearning, Clustering, KMeans, BreathingKMeans）
- [[概念_REFRAG_RAG压缩与过滤]] — REFRAG 是 Meta AI 提出的一种在向量层面进行压缩与过滤的 RAG 检索优化框架，能够显著提高首字生成时间（TTFT），并减少冗余 token 开销。（RAG, MetaAI, REFRAG, InformationRetrieval）
- ReLU激活函数非线性拟合本质 — 详细推导单个神经元 ReLU(wx + b) 相当于平移折线基底，多神经元加权累加的本质是分段线性插值，以及宽/深网络对 “Army of ReLUs” 的必然要求。
- LLM文本生成解码参数 — 系统定义并解构 Max tokens、Temperature、Top-k、Top-p、Frequency/Presence Penalty 以及 Stop Sequences 等 7 个关键解码参数的作用与原理。
- [[概念_机器学习诊断分析图表]] — 将 11 种高频关键的 DS/ML 诊断及可解释性分析图表进行系统性分类归纳，简练指出每个图表的物理含义与应用准则。（Machine-Learning, Model-Evaluation, Model-Interpretability, Data-Science）

## Comparisons

## Overview
