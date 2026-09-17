---
type: source
tags:
- Skill/python
summary: 作者分享了一套在生产环境中支撑 500+ 并发用户的 FastAPI 标准项目结构。
sources:
- raw/playbooks/FastAPI 架构指南：用这份模版打造可扩展又安全的系统（附实战经验）.md
updated: '2026-07-01'
date: 2025-10-28
---
# FastAPI 架构指南：项目模板与实战经验

## 来源信息

- **标题**：FastAPI架构指南：用这份模版打造可扩展又安全的系统（附实战经验）
- **作者**：brianobot / PyTorch研习社
- **URL**：https://mp.weixin.qq.com/s/K7bbrvMRdUejCJu-vLlE-g



## 核心内容

作者分享了一套在生产环境中支撑 500+ 并发用户的 FastAPI 标准项目结构。

### 项目结构概览

App 目录为应用核心，包含以下关键模块：

| 模块 | 作用 |
|------|------|
| `api_router.py` | 统一管理全部路由，支持版本控制（/v1/、/v2/） |
| `logger.py` | JSON 格式日志 + TimedRotatingFileHandler 按天归档 |
| `main.py` | 应用入口，安全策略集中配置 |
| `settings.py` | pydantic BaseSettings 管理环境变量，启动时类型验证 |
| `dependencies.py` | 集中管理自定义路由依赖（如 get_db） |
| `middlewares.py` | 集中管理自定义中间件 |

### 目录组织原则

- **Routers 目录**：按逻辑分组（auth.py / products.py / admin.py），路由函数不超过 2 行，只声明路由和依赖
- **Schemas 目录**：pydantic models，与路由模块一一对应
- **Services 目录**：实际业务逻辑（第三方API调用、数据库查询），实现关注点分离

### 安全策略（main.py 配置）

- CORSMiddleware：跨域白名单
- GZipMiddleware：响应压缩（minimum_size=100）
- TrustedHostMiddleware：限制可托管域名
- slowapi Limiter：基于 IP 的速率限制（防 DDoS）
- 全局异常处理：HTTPException 结构化返回 + Exception 兜底日志

### 工程实践

- 使用 Makefile 简化常用命令（`make run-local`、`make test-local`）
- pydantic-settings 的 ConfigDict 支持 .env 文件
- asynccontextmanager 管理应用生命周期（lifespan）

## 关联概念

- [[概念_FastAPI项目结构模式]]
- [[概念_Python_async_await并发]]

---
> 📎 **物理文献**：[[raw/playbooks/FastAPI 架构指南：用这份模版打造可扩展又安全的系统（附实战经验）.md]]

- 关联实体：[[entities/实体_FastAPI|FastAPI]]
