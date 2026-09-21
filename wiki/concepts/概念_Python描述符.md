---
sources:
- wiki/sources/2025-11-20_Descriptors-in-Python_19aa2d.md
- wiki/sources/2026-04-12_20-most-common-magic-methods_19d838.md
summary: Python 描述符（Descriptors）与魔术方法（Dunder Methods）是实现底层属性代理、对象协议重载与面向对象行为定制的核心机制。深入剖析
  __new__ 与 __init__ 生命周期、正数校验描述符及 20 种常用对象协议魔术方法。
tags:
- Skill/python
type: concept
updated: '2026-09-21'
---
# 概念_Python描述符

## 定义

**描述符（Descriptor）**是 Python 中实现了特定协议（即魔术方法 `__get__()`、`__set__()` 或 `__delete__()` 中的任意一个）的类实例。它用于代理和定制另一个类中属性的访问、赋值及删除行为。描述符是 Python 语言中许多高级特性（如 `@property`、实例方法绑定、`classmethod`、`staticmethod` 等）的底层实现基础。

## 底层魔术方法与生命周期

描述符的工作依赖于以下三个核心魔术方法：

1. **`__set_name__(self, owner, name)`**
   - **参数**:
     - `self`: 描述符实例本身。
     - `owner`: 定义描述符的类对象（即宿主类）。
     - `name`: 描述符实例在宿主类中被赋给的属性名称（字符串）。
   - **生命周期与触发时机**: 在宿主类定义被执行（类加载）时自动调用。Python 会自动将属性名绑定给描述符，省去了早期版本中需要手动在构造函数中传入属性名称的繁琐步骤。

2. **`__set__(self, instance, value)`**
   - **参数**:
     - `self`: 描述符实例本身。
     - `instance`: 访问属性的宿主类实例。如果是在类级别进行赋值，则不会触发该方法。
     - `value`: 要赋予属性的新值。
   - **生命周期与触发时机**: 当对宿主类实例的被代理属性进行赋值（如 `obj.attr = value`）时调用。此处是执行自定义校验、类型检查或数据转换的最佳时机。通常把值保存在 `instance.__dict__` 中，键名由 `__set_name__` 决定。

3. **`__get__(self, instance, owner=None)`**
   - **参数**:
     - `self`: 描述符实例本身。
     - `instance`: 访问属性的宿主类实例。如果直接通过类访问（如 `Class.attr`），`instance` 为 `None`。
     - `owner`: 宿主类本身。
   - **生命周期与触发时机**: 当获取宿主类实例的被代理属性（如 `obj.attr`）时调用。通常需要处理通过类直接访问的情况（若 `instance is None`，通常直接返回描述符实例本身 `self`）。

---

## 描述符 vs 传统 `@property`

当类中需要对多个属性进行相似的条件校验（例如：要求属性值必须是正数、必须是特定类型等）时，两者的对比优势极其明显：

| 维度 | 传统 `@property` 机制 | 描述符（Descriptor）机制 |
| :--- | :--- | :--- |
| **代码冗余度** | **高**。每个属性都需要单独定义一对 `@property` (getter) 和 `@property.setter`。当属性增多时，存在大量重复的验证模板代码。 | **低**。校验逻辑被封装在描述符类中，宿主类中只需将属性声明为描述符实例，即可实现逻辑复用。 |
| **可扩展性** | 属性每增加一个，代码量线性增长（$N$ 个属性需要 $N$ 个 getter + $N$ 个 setter）。 | 属性每增加一个，仅需在宿主类中增加一行声明代码。 |
| **构造拦截** | **局限性**。普通的 setter 仅在属性显式赋值时生效。如果宿主类的构造函数 `__init__` 中没有合理触发 setter，或者校验逻辑在构造时未被合理设计，可能会绕过拦截；此外，往往需要在 `__init__` 中编写冗余的初始化拦截逻辑。 | **原生支持**。只要 `__init__` 中执行了 `self.attr = value` 赋值，便会自动触发描述符的 `__set__`，在对象创建伊始就强力拦截非法输入。 |

---

## 代码示例：正数数值校验描述符

下面是一个标准的正数数值校验描述符实现，以及在宿主类中的使用示例：

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        # 自动保存宿主类中的属性名，例如 "price" 或 "quantity"
        self.private_name = f"_{name}"

    def __set__(self, instance, value):
        # 拦截赋值操作，并执行正数校验
        if not isinstance(value, (int, float)):
            raise TypeError(f"属性 {self.private_name[1:]} 必须是数值类型")
        if value <= 0:
            raise ValueError(f"属性 {self.private_name[1:]} 必须是正数 (当前值: {value})")
        # 将值存储在实例的私有属性字典中，避免无限递归
        instance.__dict__[self.private_name] = value

    def __get__(self, instance, owner):
        # 当通过类直接访问时（如 Product.price），返回描述符本身
        if instance is None:
            return self
        # 从实例字典中获取对应的数据
        return instance.__dict__.get(self.private_name)


class Product:
    # 声明描述符代理
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, name, price, quantity):
        self.name = name
        # 初始化赋值会自动触发描述符的 __set__ 校验
        self.price = price
        self.quantity = quantity


# ==================== 使用测试 ====================
if __name__ == "__main__":
    # 1. 正常创建对象
    p = Product("笔记本电脑", 5999.0, 10)
    print(f"商品: {p.name}, 价格: {p.price}, 数量: {p.quantity}")

    # 2. 构造时校验拦截（传入负数价格）
    try:
        invalid_p = Product("低价平板", -100, 5)
    except ValueError as e:
        print(f"构造拦截成功: {e}")

    # 3. 赋值时校验拦截（修改数量为非数值）
    try:
        p.quantity = "很多"
    except TypeError as e:
        print(f"赋值拦截成功: {e}")
```

## 来源
- [[wiki/sources/2025-11-20_Descriptors-in-Python_19aa2d|Descriptors in Python]]

## 关联
- [[概念_Python进阶特性]]


---

## 扩展：Python 对象协议与常用魔术方法（Dunder Methods）全景

描述符本身即是特定魔术方法（`__get__`、`__set__`、`__delete__`、`__set_name__`）的实例化协议。在 Python 面向对象生态中，魔术方法定义了类与语言内置操作（运算符、类型转换、生命周期、容器访问等）的绑定规范：

### 1. 生命周期分配与初始化区别
- **`__new__(cls, *args, **kwargs)`**：负责**内存物理分配**，是类级别静态构造器，必须显式返回实例对象；可用于底层内存拦截或实现单例（Singleton）模式。
- **`__init__(self, *args, **kwargs)`**：负责**属性初始化**，在 `__new__` 返回实例后被触发，无返回值。

### 2. 常用对象协议分类速查
- **对象表示与转换**：`__str__`（人类可读展示）、`__repr__`（调试机读表示）、`__int__`、`__bool__`、`__len__`。
- **容器协议**：`__getitem__`（索引取值）、`__setitem__`（索引赋值）、`__delitem__`、`__contains__`（`in` 操作符）、`__iter__`（可迭代循环）。
- **运算符重载**：`__eq__` / `__ne__` / `__lt__`（逻辑比较）、`__add__` / `__mul__`（算术运算）、`__call__`（可调用对象）。
