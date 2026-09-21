---
type: source
tags:
- DeepLearning
- Skill/python
summary: 一套完整的 PyTorch 深度学习训练代码模板，涵盖超参定义、数据集、模型、早停、训练验证测试九个步骤。
sources:
- raw/playbooks/实操教程 _ 深度学习pytorch训练代码模板(个人习惯).md
updated: '2026-07-01'
---
# PyTorch 训练代码模板

> URL：https://mp.weixin.qq.com/s?__biz=MzU4NjIxODMyOQ==&mid=2247511189

## 摘要

从参数定义到网络模型、训练/验证/测试步骤，一套直观的 PyTorch 训练代码模板。

## 主要内容（9 步骤）

### 1. 导入包及设置随机种子

```python
import numpy as np, torch, torch.nn as nn, pandas as pd
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt, random

seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)
```

### 2. 以类的方式定义超参数

用空的 `argparse()` 类承载超参（epochs, learning_rate, patience, hidden_size, input_size, device）。

### 3. 定义模型

继承 `nn.Module`，实现 `__init__` 和 `forward`。

### 4. 定义早停类（EarlyStopping，可省略）

- patience 计数器，监控 val_loss
- val_loss 不再下降超过 patience 次则 early_stop
- save_checkpoint 保存最优模型 state_dict

### 5. 定义数据集 Dataset / DataLoader

继承 `Dataset`，实现 `__getitem__`、`__len__`、`__load_data__`；用 DataLoader 包装（batch_size=64, shuffle=True）。

### 6. 实例化模型、loss、优化器

```python
model = Your_model().to(args.device)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
early_stopping = EarlyStopping(patience=args.patience, verbose=True)
```

### 7. 训练循环及调整 lr

- 训练阶段：model.train()，前向 → optimizer.zero_grad() → loss.backward() → optimizer.step()
- 验证阶段：model.eval()，记录 valid_loss
- early_stopping 判断
- 手动调整 lr：用 lr_adjust 字典在特定 epoch 切换学习率

### 8. 绘图

用 matplotlib 绘制 train_loss 和 epochs_loss（train/valid 对比）。

### 9. 预测

model.eval() 后直接预测，或定义预测集 Dataloader。

## 相关概念

- [[概念_Early_Stopping_早停机制]]
- [[概念_PyTorch训练循环]]

## 相关实体

- （无独立实体需创建）

---
> 📎 **物理文献**：[[raw/playbooks/实操教程 _ 深度学习pytorch训练代码模板(个人习惯).md]]