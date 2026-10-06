---
type: "entity"
tags:
  - "AI-Agent/UI"
  - "AI-Agent/memory"
summary: "Meta 推出的 Personal Agent（个人智能体）旗舰产品，具备专属云端沙盒电脑、双安全域隔离架构（Harness 与宿主 Sentinel）、夜里学习与持续目标追踪能力。"
sources:
  - "wiki/sources/Meta复盘Muse_Agent怎么才能像一个人长期存在.md"
updated: "2026-10-06"
---

# 实体：Muse

## 基本信息

- **开发机构**：[[entities/实体_Meta|Meta]]
- **产品类型**：Personal Agent（个人智能体 / 个人超级智能）
- **核心定位**：打破单纯问答的 Chatbot 形态，为用户提供一个专属、长程在线、替用户自主办事的数字伙伴。
- **关键设计者**：Mona Sarantakos（Muse 产品设计负责人）、马克·扎克伯格（Meta 创始人兼 CEO）、Moxie Marlinspike（Signal 创始人，受聘主导 Muse 机密虚拟机安全项目）。

## 交互设计与产品架构

1. **单会长对话与侧边上下文隔离**：
   - 主界面设计为一段跨越天周的长对话，保留跨会话记忆，支持打断与连续派发多任务；
   - 引入侧边对话（Side Conversations）隔离复杂长流程任务上下文；
   - 允许用户定制专属形象、名字与性格风格。
2. **超越 Chat 的富交互产物（Artifacts）**：
   - 摈弃纯长文本输出，由 Agent 针对任务输出量身定制的可交互界面（如动态开支仪表盘、行程规划表单），结合 [[concepts/概念_Presentation_Tools_表现层工具化|表现层工具化]] 交付高质量体验。
3. **高门槛主动通信与全流程透明化**：
   - 能够长期在后台推进任务，但主动通知的门槛极高，仅在出现里程碑新进展或需要用户决策时打断；
   - 提供直观的活动说明、历史执行轨迹以及独立的「目标」标签页（Goals Tab）。

## 安全系统：双安全域隔离

Muse 为每位用户配备专属云端虚拟机环境，并创新性地划分为**两个物理/逻辑互不信任的安全域**：

- **运行单元 (Agent Harness)**：处于受控隔离沙盒内，负责执行推理、运行代码与浏览网页。该环境被预设为正在遭受攻击，所有外部数据均被打标为不可信输入，无 Root 权限亦无法访问真实凭证。
- **宿主侧哨兵 (Host Sentinel)**：独立于 Agent 的宿主审批中枢，作为所有系统连接器和外部网络出站流量的唯一权威裁决方。
- **纵深防御与 Simon Willison 致命三要素**：
  - **结构化审批卡片**：关键操作前展示明确「接受/拒绝」卡片，防止用户产生“横幅盲视”；
  - **连接器脱敏**：邮件连接器自动清洗验证码（OTP）与密码重置链接；
  - **一次性支付凭证**：未知商户支付自动签发一次性虚拟卡号；
  - **机密虚拟机（Confidential VM）**：借助硬件加密技术保障连 Meta 自身也无法窃视用户私密数据。

## 记忆机制与“夜里学习”

- **夜里学习 (Nightly Learning)**：在夜间空闲时段将白天的交互反思与任务进展自动整合归纳进长期记忆，并衍生新建议；
- **记忆完全透明**：用户拥有独立的记忆文件，可随时直接查看、修正与删除；
- **受训的分寸感 (Discretion)**：模型在预训练与后训练阶段专门强化了信息敏感度识别能力，确保对外代办事务时严格隐去用户非必要的个人隐私。

## 关联页面

- **归属机构**：[[entities/实体_Meta|实体_Meta]]
- **核心概念**：[[concepts/概念_Personal_Agent_个人智能体|概念_Personal_Agent_个人智能体]]、[[concepts/概念_Agent三层记忆体系|概念_Agent三层记忆体系]]、[[concepts/概念_Presentation_Tools_表现层工具化|概念_Presentation_Tools_表现层工具化]]、[[concepts/概念_Hardened_Sandbox_强化隔离沙盒|概念_Hardened_Sandbox_强化隔离沙盒]]
- **对比实体**：[[entities/实体_Claude_Code|实体_Claude_Code]]（企业代码工程智能体 vs 个人生活协同智能体）

## 来源与参考

- [[wiki/sources/Meta复盘Muse_Agent怎么才能像一个人长期存在.md]]
