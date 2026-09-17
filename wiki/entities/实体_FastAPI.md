---
type: entity
tags:
- Skill/python
summary: '- 类型：Python Web 框架'
sources:
- wiki/sources/FastAPI架构指南_项目模板与实战经验.md
- wiki/sources/FastAPI生产部署ASGI_WSGI避坑指南.md
- wiki/sources/Python并发_async_await与FastAPI.md
- wiki/sources/五个鲜为人知的Python功能.md
updated: '2026-07-06'
---
# 实体_FastAPI

## 基本信息

- **类型**：Python Web 框架
- **作者**：Sebastián Ramírez（tiangolo）
- **底层**：基于 Starlette（ASGI）+ Pydantic（数据验证）
- **特点**：高性能、原生 async/await、自动 OpenAPI 文档

## 核心技术特征

- 路径操作函数支持 `async def` 和普通 `def`（后者自动放入线程池）
- 基于 AnyIO 实现（兼容 asyncio 和 Trio）
- 性能与 Go 不相上下、优于多数 NodeJS 框架（归功于 Starlette）
- 原生集成 pydantic BaseModel 做请求/响应验证
- pydantic-settings BaseSettings 管理环境变量
- typing.Literal 等类型注解原生支持

## 生产项目结构

三层分离模式：Routers（路由声明）/ Schemas（数据模型）/ Services（业务逻辑），按业务组件一一对应。

## 安全中间件

CORSMiddleware / GZipMiddleware / TrustedHostMiddleware / slowapi 速率限制。

## 来源

- [[FastAPI架构指南_项目模板与实战经验]]
- [[Python并发_async_await与FastAPI]]

## 关联

- [[concepts/概念_uv包管理器|uv]]
- [[概念_FastAPI项目结构模式]]
- [[概念_Python_async_await并发]]