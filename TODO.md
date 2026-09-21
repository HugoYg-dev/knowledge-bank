- [x] 全量 Ingest 阶段（Phase 1 至 Phase 6，共 191 篇 Sources 导入）已全部完成。
- [x] wiki/sources 需要修复每个的frontmatters(主要是source，191 篇已全部完成规范化清洗与 Cubox 物理路径 100% 关联)
- [x] wiki/下的entities、sources的tag需要整理（已完成 191 篇 sources 与 137 篇 entities 全量合规检查与补全）
- [x] 全库 Tag 体系合规性治理：门禁加固 (vault_lint)、存量 830 篇清洗 (normalize_tags)、单一权威规则同步、Fallback 策略改造与 36 组单元测试 100% 通过
- [x] raw/articles/ 历史 76 篇邮件拆分裸文本批量回溯注入标准 Frontmatter (scripts/backfill_raw_frontmatter.py)

## wiki
- [x] frontmatter不一致（已全量深度重构与清洗，sources/entities/concepts 共 652 篇全部达成字段一致与内容齐全）
- [x] sources/ 数量和 raw/ 是否一致（已对齐，双方均为 163 篇，完成 1对1 精准映射）
- [x] wiki/entities 频率不高的人/组织/单次工具移除与模型家族化整合（已完成入度<=1实体的全量分类审阅与用户逐项审批：清理 18 篇低复利价值人物/组织/工具，聚合 GPT/GLM/Gemma 家族，保留核心基建与作者实体，全库 0 死链通过）
- [x] entities、conceptes等，是否移除tag（经讨论决定保留 Tag 字段，维持跨文件夹的多维度横向标签聚类能力）
- [x] entites、concepts的frontmatter中的上游sources需要仔细审查（编写 scripts/audit_upstream_sources.py 完成 77 篇页面的虚假来源清洗与真实双链回填）
- [x] 治理历史遗留的 26 个来源死链错误（恢复 23 篇 raw/playbooks 物理文献，清理 2 篇废弃概念与实体，Vault Lint 100% 绿灯通过）
- [ ] 面经文章汇总：全库带有「面试」tag 的面经文章仅用于生成一篇体系化的面经总结文档（Overview），不作为实体（entities）的信息来源；需完成全库面经梳理并生成专题总结。
- [x] 概念命名标准化迁移：参考 [[docs/plans/concept_naming_migration_plan.md]] 已全量完成存量概念规范化治理（Phase 1 倒置纠偏 26 篇、Phase 2 纯英文补全 69 篇、Phase 3 分界符标准化 20 篇全部完成，0 错误 0 死链通过门禁）
- [ ] 检索的部分，还需要工程化，现有方案（grep/ mcp/ sed 等）

## others
- [ ] workdocs/ 存放了工作期间的项目文档docx，需要解析并入库
- [ ] wucai的库存同步过来，同时合并目录cubox和notes，统一命名为raw/
