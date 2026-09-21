---
type: source
tags:
- MachineLearning
- Infra/platform
summary: 本文介绍了在生产环境中测试机器学习模型的 4 种经典方法，即 A/B 测试、金丝雀测试、交叉测试（Interleaved）以及影子测试（Shadow），并在其扩展阅读中提及了多臂强盗部署（MAB）。
sources:
- raw/articles/2025-02-03_4-ways-to-test-ML-models-in-production_194cd4.md
updated: '2026-08-03'
---
# 4 ways to test ML models in production

## 核心要点

1. **生产环境测试的必要性**：即使在本地验证集和测试集上表现优异，直接全量替换模型也可能带来灾难性后果。在真实的线上数据上逐步进行生产测试是更稳妥的选择。
2. **A/B 测试**：将流量非均匀分配给旧模型和新模型，通常用于限制新模型的曝光比例以减少潜在风险。
3. **金丝雀测试**：与 A/B 测试随机分配不同，金丝雀测试将候选模型优先部署到一小部分特定用户群中，确保稳定性后再逐步扩展至全量用户。
4. **交叉测试（Interleaved Testing）**：将多个模型的预测结果交错混合后一次性呈现给用户，可以通过单一请求的用户点击偏好快速迭代对比。
5. **影子测试（Shadow Testing）**：双路分流但只选用旧模型的响应作为最终用户结果，新模型的预测仅记录在日志中。这种方法对用户体验完全无侵入且无风险。
6. **多臂强盗部署（MAB）**：文章提及了第五种技术 MAB（Multi-armed Bandits），它在测试中动态学习并分配流量给表现更优的模型。

## 关键引文

> "Despite rigorously testing an ML model locally (on validation and test sets), it could be a terrible idea to instantly replace the previous model with the new model."
> "Shadow testing (or dark launches) lets us test a new model in a production environment without affecting the user experience."

## 关联

- **相关概念**：机器学习模型生产环境测试
- **来源**：[[raw/articles/2025-02-03_4-ways-to-test-ML-models-in-production_194cd4.md]]

---
> 📎 **物理文献**：[[raw/articles/2025-02-03_4-ways-to-test-ML-models-in-production_194cd4.md]]
