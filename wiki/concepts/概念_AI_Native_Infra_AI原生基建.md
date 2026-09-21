---
type: concept
tags:
- Infra/platform
summary: AI-Native Infra 是专为 AI（而非人类工程师）设计的基础设施，去掉"人类兜底层"，所有状态/操作/错误都 API 化、结构化、机器可读，让
  AI 能自驱动地完成构建、部署、运维全流程。
sources:
- wiki/sources/AI-Native的Infra演化路线L0到L5.md
- wiki/sources/入局AI_Infra系统设计与挑战.md
updated: '2026-09-21'
aliases:
- AI-Native Infra
- AI Native Infra
- AI原生基建
- 概念_AI-Native_Infra
---

# 概念：AI-Native Infra

## 定义

AI-Native Infra 是从零开始、专为 AI 的工作方式设计的基础设施"操作台"和"工具箱"，不是把人类工具"翻译"给 AI 用，而是去掉整个"人类兜底层"。在这个范式中 AI 不再是工具的使用者，而是系统的主导者和决策者。

## 问题背景：隐性人类假设

现有后端系统（Firebase、Supabase、Vercel、AWS 等）都隐含默认前提：使用者是人类工程师且始终在线兜底。体现在三个层面：
- **界面交互层**：需人手动点击/确认/读图表
- **认知负担层**：需人记操作顺序、理解隐含业务逻辑、跨系统建心理模型
- **异常处理层**：报错是"人话"（如 `permission denied`、"请检查配置"）而非机器可操作指令

GUI、CLI、文档本质上都是"人类语义翻译器"，假设背后有聪明人能理解上下文、填补空白、处理异常。

## 应具备的特征

- **状态透明化**：所有系统状态通过标准化 API 暴露
- **接口标准化**：每个操作有明确 API 定义，输入输出格式固定
- **模块可组合**：服务像乐高积木自由组合
- **操作可回滚**：任何变更可程序化撤销/重做
- **逻辑自包含**：不依赖外部"常识"，所有规则明确编码
- **结构化错误响应**：含 error_code、missing_role、fix_endpoint、fix_payload 等可操作信息

## 关联

- [[AI-Native的Infra演化路线L0到L5]]（来源）
- [[入局AI_Infra系统设计与挑战]]（来源）
- [[概念_L0_L5_能力成熟度模型]]
- [[概念_Result_as_a_Service_结果即服务]]