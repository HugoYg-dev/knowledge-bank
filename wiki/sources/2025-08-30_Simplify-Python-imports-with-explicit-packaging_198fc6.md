---
type: source
tags:
- Skill/python
summary: 探讨 Python 项目中显式包管理机制。虽然 Python 3.3+ 引入了隐式命名空间包，但显式使用 __init__.py 能够明确包的导出接口、简化外部导入路径并避免冗余导入，是优化工程设计的最佳实践。
sources:
- raw/articles/2025-08-30_Simplify-Python-imports-with-explicit-packaging_198fc6.md
updated: 2026-08-03
---

# Simplify Python imports with explicit packaging

本文介绍了如何通过显式创建 `__init__.py` 文件来进行 Python 项目的包管理，以及它在简化导入路径和控制包接口等方面的工程设计优势。

## 来源信息
- **邮件主题**: Data and Pipeline Engineering for ML Systems (With Implementation)
- **发送人**: Daily Dose of DS (avi@dailydoseofds.com)
- **日期**: 2025-08-30
- **链接**: [Daily Dose of DS](https://www.dailydoseofds.com/)

## 核心要点
1. **术语定义**：
   - **Module（模块）**：指单个 `.py` 文件。
   - **Package（包）**：指包含一组 Python 模块的目录。
   - **Library（库）**：指多个包的集合。
2. **隐式与显式包装的对比**：
   - Python 3.3+ 引入了**隐式命名空间包 (Implicit Namespace Packages)**，即便目录中没有 `__init__.py` 文件，该目录默认也会被视为一个包。
   - 但工程上仍然强烈建议显式创建 `__init__.py` 文件。
3. **显式包管理的主要优势**：
   - **定制包级接口**：可以在 `__init__.py` 中显式指定哪些类、函数可以被外部导入。
   - **简化外部导入路径**：在未使用 `__init__.py` 时，外部需写多行繁琐导入（如 `from model.train import Training`，`from model.test import Testing`）；而在 `__init__.py` 中整合后，外部可以直接通过 `from model import Training, Testing` 完成导入，即将包视作单个模块处理。
   - **避免冗余导入**：优化了开发者的使用体验，使包的边界和公共 API 更加清晰。

## 关键引文
> "While Python 3.3+ provides Implicit Namespace Packages , which means a directory with modules is considered a package by default, it is still advised to create an explicit `__init__.py` file."
> 
> "In other words, specifying the `__init__.py` file lets you treat your package like a module. This simplifies your imports."

## 联动概念
- Python模块与包管理

---
> 📎 **物理文献**：[[raw/articles/2025-08-30_Simplify-Python-imports-with-explicit-packaging_198fc6.md]]
