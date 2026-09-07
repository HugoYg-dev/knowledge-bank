---
type: concept
tags:
- AI-Agent/tool-calling
summary: 保障智能体在执行代码与调用外部系统时的安全隔离环境，通过工作区隔离、网络白名单、资源限额（cgroup）、受限运行时及系统调用拦截构建多层防御体系。
sources:
- wiki/sources/DeepSeek AI Infra 一面，面爽了！！！.md
- wiki/sources/美团AI全栈Agent一面，笑着聊完挂了！！！.md
- wiki/sources/DeepSeek Agent开发岗三面，再面一轮就offer啦！！！.md
updated: "2026-09-07"
---

# 概念：Agent 工具调用沙箱

## 定义

**Agent 工具调用沙箱（Agent Tool-Calling Sandbox）** 是智能体系统中用于安全执行大模型生成代码、调用外部脚本与执行系统命令的强隔离运行环境。由于大模型生成的代码和调用的工具属于**不可信输入/产物**，具备非确定性与潜在安全攻击风险，沙箱旨在将执行风险严格限制在受控边界内，杜绝越权访问宿主机、网络横向渗透、资源耗尽（DoS）或恶意篡改等高危后果。

## 核心安全威胁与防范目标

1. **宿主环境越权与文件篡改**：模型生成恶意路径遍历（如 `../../etc/passwd`）或直接执行 `rm -rf /`；
2. **内网横向探测（SSRF）**：模型调用网络工具探测内部集群 IP（如 `127.0.0.1`、`192.168.x.x`）或元数据服务；
3. **计算资源耗尽（Fork 炸弹 / 死循环）**：无节制占用 CPU、内存或磁盘 I/O 导致宿主机崩溃；
4. **任意命令注入与提权**：通过脚本隐蔽调用 `os.system()`、`subprocess` 派生子进程或执行敏感系统调用。

## 多层立体沙箱防御架构

根据 DeepSeek 与美团等工业级 Agent Infra 的工程实践，生产级工具沙箱由以下五道防线协同构成：

### 1. 文件系统隔离层（Filesystem Isolation）
- 为每个工具调用或会话分配专有的临时工作目录；
- 采用 **Docker Volume** 单独挂载、`chroot` 或只读挂载（Read-Only Mounts）机制，严格禁止访问宿主敏感目录与系统配置。

### 2. 网络边界控制层（Network Boundary Control）
- 实施严格的 **DNS 与 IP 访问白名单**；
- 在网关层或通过 Linux `iptables` 强力阻断私有网段（`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`），防范内网扫描与未授权数据回传。

### 3. 计算资源硬配额层（Resource Quotas via cgroups）
- 利用 Linux **cgroups**（控制组）设置严格的 CPU 核心配额与内存物理上限；
- 当脚本内存占用超出阈值时立即触发内核级 OOM-kill，防范内存泄露与 DoS 攻击；
- 在应用层（如 Python `resource` 模块）配合设置进程执行时间软硬上限（Timeout）。

### 4. 运行时受限与系统调用拦截（Runtime & Syscall Filtering）
- **严禁裸跑原生 `exec()` / `eval()`**：脚本执行必须依托受限执行环境（如 RestrictedPython、微容器沙箱或 WebAssembly）；
- **系统调用过滤（seccomp）**：利用 Linux **seccomp-bpf** 机制审查并拦截危险系统调用（如直接禁用 `execve`、`fork`、`clone`、`ptrace` 等），彻底阻断反弹 Shell 和子进程逃逸。

### 5. 静态分析与人工审批门禁（Static Analysis & HITL）
- **离线静态代码审查**：集成 Semgrep、SonarQube 等静态分析引擎，在代码投递执行前扫描 SQL 注入、硬编码密钥与危险调用模式；
- **分级审批（Human-in-the-loop）**：针对涉及支付交易、用户权限修改、数据库批量删除等不可逆高危操作，强制转入人工确认流程，绝不放行全自动直通执行。

## 代表实践

- [[entities/实体_DeepSeek|DeepSeek]]：在 AI Infra 中提出三层沙箱隔离与 seccomp 系统调用拦截；
- [[entities/实体_美团|美团]]：在 AI Coding 与生活服务智能体中部署“静态审查 + 沙箱单测 + 人工复核”的三道防线；
- [[entities/实体_Claude_Code|Claude Code]]：依托只读分析与受控 Bash 权限审批机制实现工作区安全护栏。

## 关联概念与来源

- [[concepts/概念_Harness_Engineering|Harness Engineering]]
- [[concepts/概念_HITL_MCP|HITL MCP]]
- [[concepts/概念_级联清理安全边界|级联清理安全边界]]
- 来源：
  - [[sources/DeepSeek AI Infra 一面，面爽了！！！]]
  - [[sources/美团AI全栈Agent一面，笑着聊完挂了！！！]]
  - [[sources/DeepSeek Agent开发岗三面，再面一轮就offer啦！！！]]
