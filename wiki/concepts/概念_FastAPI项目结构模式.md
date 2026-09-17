---
type: concept
tags:
- Skill/python
summary: 一套生产可用的 FastAPI 标准项目组织模式，核心思想是 Routers / Schemas / Services 三层分离，按业务组件一一对应。
sources:
- wiki/sources/Docker化Flask_Django应用从pip切换到uv.md
- wiki/sources/FastAPI架构指南_项目模板与实战经验.md
- wiki/sources/Python并发_async_await与FastAPI.md
updated: '2026-07-06'
---


# 概念_FastAPI项目结构模式

## 定义

一套生产可用的 FastAPI 标准项目组织模式，核心思想是 **Routers / Schemas / Services 三层分离**，按业务组件一一对应。

## 三层分离

| 层 | 职责 | 约束 |
|----|------|------|
| Routers | 声明路由、定义依赖与请求参数 | 函数尽量不超过 2 行 |
| Schemas | pydantic models（请求/响应数据模型） | 与路由模块对应 |
| Services | 实际业务逻辑（DB 查询、第三方 API） | 与路由模块对应 |

例如 auth 组件：`routers/auth.py` + `schemas/auth.py` + `services/auth.py`。

## 核心模块

- `api_router.py`：统一管理路由，支持版本控制（APIRouter prefix="/v1"）
- `settings.py`：pydantic-settings BaseSettings 管理环境变量，启动时类型验证
- `dependencies.py`：集中自定义依赖（如 get_db 返回 AsyncSession）
- `middlewares.py`：集中自定义中间件
- `logger.py`：JSON 格式日志 + TimedRotatingFileHandler 按天归档

## 安全与中间件配置（main.py）

- CORSMiddleware / GZipMiddleware / TrustedHostMiddleware
- slowapi Limiter：基于 IP 速率限制，防 DoS
- 全局异常处理：HTTPException 结构化返回 + Exception 兜底

## 价值

模块化结构带来可预期、合理的功能组织，提升长期可维护性与开发者体验。

## 来源

- [[FastAPI架构指南_项目模板与实战经验]]

## 关联

- [[概念_Python_async_await并发]]
- [[概念_uv包管理器]]

- 关联实体：[[entities/实体_FastAPI|FastAPI]]
