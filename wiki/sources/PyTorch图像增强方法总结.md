---
type: source
tags:
- CV/data-augmentation
summary: 13 个 PyTorch（torchvision.transforms）图像增强方法实战总结附代码：Resize、灰度、标准化、随机旋转、中心/随机裁剪、高斯模糊、ColorJitter、水平/垂直翻转、高斯噪声、随机块、中心区域。
sources:
- raw/playbooks/实战｜13个Pytorch 图像增强方法总结（附代码）.md
updated: '2026-07-01'
---
# 13 个 PyTorch 图像增强方法总结

## 来源信息

- 标题：实战｜13个Pytorch 图像增强方法总结（附代码）
- 作者：结发授长生（知乎 https://zhuanlan.zhihu.com/p/559887437）
- URL：https://mp.weixin.qq.com/s/Qg2wI8Ow_hYPF7LCnntDCg
- 基于全文 ingest（眼底图像为例，均含可运行代码）

## 核心要点

数据增强增加数据集图像多样性，提升模型性能和泛化能力。基于 `torchvision.transforms`：

1. **调整大小 Resize**：`T.Resize(size=size)`，如 128/256
2. **灰度变换 Grayscale**：`T.Grayscale()` 将 RGB 转灰度
3. **标准化 Normalize**：`T.Normalize(mean, std)`，从每通道减均值再除以通道标准差；加快计算与学习速度
4. **随机旋转 RandomRotation**：`T.RandomRotation(degrees=90)`
5. **中心裁剪 CenterCrop**：`T.CenterCrop(size=size)` 裁剪中心区域
6. **随机裁剪 RandomCrop**：`T.RandomCrop(size=size)` 随机裁剪某部分
7. **高斯模糊 GaussianBlur**：`T.GaussianBlur(kernel_size, sigma)`，sigma 越大越模糊
8. **亮度/对比度/饱和度 ColorJitter**：`T.ColorJitter(brightness, contrast, saturation)`
9. **水平翻转 RandomHorizontalFlip**：`T.RandomHorizontalFlip(p=1)`
10. **垂直翻转 RandomVerticalFlip**：`T.RandomVerticalFlip(p=1)`
11. **高斯噪声**：自定义 `add_noise`，`inputs + torch.randn_like(inputs) * noise_factor` 再 clip；noise_factor 越高噪声越大
12. **随机块**：自定义 `add_random_boxes`，在随机位置加正方形黑色补丁（置 0），补丁越多越难
13. **中心区域**：自定义 `add_central_region`，类似随机块但补丁加在图像中心

> 注：标准化用 `T.ToTensor()` 先转 tensor；高斯噪声/随机块/中心区域为自定义函数（非内置 transform）。

## 关联概念

- torchvision图像增强

---
> 📎 **物理文献**：[[raw/playbooks/实战｜13个Pytorch 图像增强方法总结（附代码）.md]]