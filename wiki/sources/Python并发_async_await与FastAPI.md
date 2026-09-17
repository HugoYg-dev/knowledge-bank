---
type: source
tags:
- Skill/python
summary: FastAPI 官方对异步编程、并发与并行的完整讲解。
sources:
- raw/playbooks/Py中的并发 async _ await - FastAPI.md
updated: '2026-07-01'
date: 2025-06-27
---
# Python 并发 async/await 与 FastAPI

## 来源信息

- **标题**：Py中的并发 async / await - FastAPI
- **作者**：FastAPI 官方文档（Sebastián Ramírez）
- **URL**：https://fastapi.tiangolo.com/zh/async/



## 核心内容

FastAPI 官方对异步编程、并发与并行的完整讲解。

### 路径操作函数选择规则

| 场景 | 推荐写法 | 原因 |
|------|----------|------|
| 第三方库支持 await | `async def` + `await` | 利用异步 I/O |
| 第三方库不支持 await | 普通 `def` | FastAPI 自动放入线程池 |
| 无需等待外部通信 | `async def` | 避免线程池开销 |
| 不确定 | `def` | 安全默认 |

### 并发 vs 并行（汉堡比喻）

- **并发**（Concurrency）：一个收银员+一个厨师，你下单后去聊天等叫号 → I/O 密集型，适合 Web
- **并行**（Parallelism）：8 个收银员同时做，你必须站着等 → CPU 密集型，适合 ML/CV

### 技术细节

- 协程（Coroutine）：`async def` 返回的对象，可暂停可恢复
- FastAPI 基于 AnyIO（兼容 asyncio 和 Trio）
- `def` 路径操作函数运行在外部线程池中（不会阻塞事件循环）
- `async def` 路径操作函数直接在事件循环中运行
- 依赖项（dependencies）同理：`def` 走线程池，`async def` 走事件循环

### FastAPI 性能定位

- 与 NodeJS 异步相同原理
- 并发 + 并行兼具：Web 用异步，ML 用多进程
- 性能与 Go 不相上下（归功于 Starlette）

## 关联概念

- [[概念_Python_async_await并发]]
- [[概念_FastAPI项目结构模式]]

---
> 📎 **物理文献**：[[raw/playbooks/Py中的并发 async _ await - FastAPI.md]]

- 关联实体：[[entities/实体_FastAPI|FastAPI]]
