---
type: source
tags:
- Skill/python
- DeepLearning
summary: PyTorch 常用代码段大全，涵盖基本配置（可复现性/显卡设置）、张量处理（类型转换/形变/拼接/矩阵乘法）、模型定义与操作（权重初始化/提取层/预训练加载/SyncBN）、数据处理（均值标准差/预处理/TSN
  采样）、模型训练与测试（分类训练/Label Smoothing/Mixup/梯度裁剪/学习率衰减/断点续训/TensorBoard 可视化）及实用 Tips。
sources:
- raw/playbooks/PyTorch常用代码段合集.md
updated: '2026-07-01'
---
# PyTorch 常用代码段合集

## 来源信息

- 标题：PyTorch常用代码段合集
- 作者：Jack Stark / 极市平台（转载）
- URL：https://mp.weixin.qq.com/s/FtO1zuusgUTjL9y-JkFG0A
- 原始来源：https://zhuanlan.zhihu.com/p/104019160
- 基于全文 ingest

## 核心内容

### 1. 基本配置

- **可复现性**：固定 `torch.manual_seed(0)`、`np.random.seed(0)`、`torch.cuda.manual_seed_all(0)`；设置 `cudnn.deterministic=True`、`cudnn.benchmark=False`
- **显卡设置**：`CUDA_VISIBLE_DEVICES` 环境变量指定多卡；`torch.cuda.empty_cache()` 清显存；`nvidia-smi --gpu-reset` 重置 GPU

### 2. 张量处理

- 9 种 CPU + 9 种 GPU 张量类型；`FloatTensor` 远快于 `DoubleTensor`
- 命名张量（PyTorch 1.3+）：`names=('N','C','H','W')`，支持 `align_to`
- 类型转换：`.cuda()`/`.cpu()`/`.float()`/`.long()`
- Tensor ↔ ndarray：`tensor.cpu().numpy()` / `torch.from_numpy()`
- Tensor ↔ PIL.Image：`torchvision.transforms.functional.to_pil_image` / `to_tensor`
- 张量形变：`torch.reshape`（自动处理不连续）优于 `torch.view`
- 拼接：`torch.cat`（沿给定维度拼接）vs `torch.stack`（新增一维）
- one-hot 编码：`scatter_` 方法
- 矩阵乘法：`torch.mm`（2D）/ `torch.bmm`（3D batch）/ `*`（逐元素）
- 欧式距离：`torch.sqrt(torch.sum((X1[:,None,:] - X2)**2, dim=2))`（利用 broadcast）

### 3. 模型定义与操作

- 双线性汇合（bilinear pooling）：`torch.bmm` + signed-sqrt + L2 归一化
- 多卡同步 BN：`torch.nn.SyncBatchNorm`；可递归转换已有网络所有 BN 层
- 计算参数量：`sum(torch.numel(p) for p in model.parameters())`
- 权重初始化：Conv2d 用 `kaiming_normal_`，BN 用常数 1/0，Linear 用 `xavier_normal_`
- 提取层：`nn.Sequential(*list(model.children())[:N])`
- 预训练加载：`load_state_dict(strict=False)`；GPU→CPU 用 `map_location='cpu'`
- 导入另一模型相同部分：字典交集更新

### 4. 数据处理

- 计算数据集均值和标准差：两遍遍历法
- 视频基本信息：`cv2.VideoCapture` 获取 H/W/帧数/FPS
- TSN 分段采样：训练随机/测试取中间帧
- 标准预处理：训练用 RandomResizedCrop+HorizontalFlip，验证用 Resize+CenterCrop；ImageNet 均值 (0.485, 0.456, 0.406)

### 5. 模型训练与测试

- 分类训练代码：CrossEntropyLoss + Adam + forward/backward/step
- 分类测试：`model.eval()` + `torch.no_grad()`
- 自定义 loss：继承 `nn.Module`
- Label Smoothing：LSR 类实现或直接 `smoothed_labels.scatter_`
- Mixup：Beta 分布采样 λ，混合图像和标签
- L1 正则：`torch.sum(torch.abs(param))`
- 不对 bias 做 weight decay：分组参数
- 梯度裁剪：`clip_grad_norm_`
- 学习率衰减：ReduceLROnPlateau / CosineAnnealing / MultiStepLR / Warmup / 链式 Scheduler
- 断点续训：同时保存 model、optimizer、epoch、best_acc
- 提取预训练特征：VGG/ResNet 各层提取方式
- 微调策略：冻结卷积层只训 fc / 不同层设不同 lr

### 6. 实用 Tips

- 不要使用太大线性层（`nn.Linear(m,n)` 占 O(mn) 内存）
- 不要在太长序列上用 RNN（BPTT 内存线性于长度）
- `model.train()` vs `model.eval()` 切换 BN/Dropout 行为
- `torch.no_grad()` 关闭自动求导减少显存
- `model.zero_grad()` vs `optimizer.zero_grad()` 作用范围不同
- `CrossEntropyLoss` 输入不需经 Softmax
- `pin_memory=True` 通常更快；`del` 及时删中间变量；inplace 操作节显存
- 减少 CPU-GPU 数据传输（累积后一次传回）
- 半精度 `half()` 加速需注意数值稳定性
- `assert tensor.size()` 作为调试手段
- `torch.autograd.profiler.profile` 统计耗时
- TorchSnooper：自动打印每行执行结果的 tensor 信息

## 关联概念

- [[概念_PyTorch训练循环]]
- [[概念_Early_Stopping_早停机制]]
- [[概念_Batch_Normalization_批归一化]]
- [[概念_Label_Smoothing_标签平滑]]
- [[概念_Mixup训练]]
- [[概念_学习率调度]]

## 关联实体

- [[实体_PyTorch]]

---
> 📎 **物理文献**：[[raw/playbooks/PyTorch常用代码段合集.md]]