---
type: concept
tags:
- Skill/python
- DeepLearning
summary: PyTorch 深度学习模型标准训练流程，包含训练/验证/预测三阶段及辅助组件。
sources:
- wiki/sources/PyTorch常用代码段合集.md
- wiki/sources/PyTorch训练代码模板.md
- wiki/sources/手把手教你实现稀疏MoE语言模型.md
updated: '2026-07-06'
---

# 概念：PyTorch 训练循环


## 定义

PyTorch 深度学习模型标准训练流程，包含训练/验证/预测三阶段及辅助组件。

## 完整 9 步结构（全文模板）

1. **导入包 + 随机种子**：torch.manual_seed / np.random.seed / random.seed 保证可复现
2. **超参定义**：用类承载 epochs, learning_rate, patience, hidden_size, input_size, device
3. **模型定义**：继承 nn.Module，实现 `__init__` 和 `forward`
4. **早停类**：[[概念_Early_Stopping_早停机制]]，可省略
5. **数据集**：继承 Dataset 实现 `__getitem__` / `__len__`；DataLoader 包装（batch_size, shuffle）
6. **实例化**：model.to(device)、criterion（如 MSELoss）、optimizer（如 Adam）
7. **训练循环**：
   - model.train() → 前向 → optimizer.zero_grad() → loss.backward() → optimizer.step()
   - model.eval() → 验证阶段（不做梯度计算）
   - early_stopping 判断
   - 手动 lr 调整：字典定义特定 epoch 的 lr 值
8. **绘图**：matplotlib 绘制 train_loss / epochs_loss（train vs valid）
9. **预测**：model.eval() → 直接前向推理

## 关键细节

- 数据转 float32 并 .to(device)
- 训练时记录 batch 级和 epoch 级 loss
- 验证阶段不调用 optimizer
- lr_adjust 字典方式手动调度学习率（epoch 2/4/6/8/10/15/20 逐步衰减）

## 来源

- [[PyTorch训练代码模板]]