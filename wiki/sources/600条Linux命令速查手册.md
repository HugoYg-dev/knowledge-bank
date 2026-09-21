---
type: source
tags:
- Skill/linux
summary: 本文将日常运维中常用的 Linux 命令按功能分为 28 大类进行整理，涵盖从系统信息到网络配置、从文件管理到软件包管理的全方位速查。全文约 600
  条命令，号称"能用到退休"，可解决日常 99% 的问题。
sources:
- raw/playbooks/能用到“退休”的 600条 Linux 命令，可以解决日常99%的问题~.md
updated: '2026-07-01'
cubox_url: https://cubox.pro/web/card/7159452574557406140
date_collected: 2024-02-20
---
# 600条Linux命令速查手册

## 来源信息

- **标题**：600条Linux命令速查手册
- **作者**：冰河（码小辫转载）
- **URL**：https://mp.weixin.qq.com/s/_T1WNfnTd5OoEA_RkgRThg



## 概述

本文将日常运维中常用的 Linux 命令按功能分为 28 大类进行整理，涵盖从系统信息到网络配置、从文件管理到软件包管理的全方位速查。全文约 600 条命令，号称"能用到退休"，可解决日常 99% 的问题。

## 28大分类目录

| 序号 | 分类 | 核心命令示例 |
|------|------|------|
| 1 | 基本命令 | uname/dmidecode/hdparm/cat /proc/* |
| 2 | 关机 | shutdown/init 0/reboot/logout |
| 3 | 文件和目录 | cd/ls/mkdir/cp/mv/rm/ln |
| 4 | 文件搜索 | find/locate/whereis/which |
| 5 | 挂载文件系统 | mount/umount/fuser |
| 6 | 磁盘空间 | df/du |
| 7 | 用户和群组 | useradd/userdel/groupadd/passwd/chage |
| 8 | 文件权限 | chmod/chown/chgrp |
| 9 | 文件特殊属性 | chattr/lsattr |
| 10 | 打包和压缩 | tar/gzip/bzip2/zip/unzip |
| 11 | RPM 包 | rpm -ivh/-e/-qa/-qi |
| 12 | YUM 软件包升级器 | yum install/update/remove/search |
| 13 | DEB 包 | dpkg/apt-get |
| 14 | 查看文件内容 | cat/more/less/head/tail |
| 15 | 文本处理 | grep/sed/awk/sort/cut/paste/tr |
| 16 | 字符设置和文件格式转换 | iconv/dos2unix |
| 17 | 文件系统分析 | fdisk/fsck |
| 18 | 初始化文件系统 | mkfs/mke2fs |
| 19 | SWAP文件系统 | mkswap/swapon/swapoff |
| 20 | 备份 | dump/restore/rsync/dd |
| 21 | 光盘 | cdrecord/mkisofs |
| 22 | 网络 | ifconfig/ip/route/netstat/ss/iptables |
| 23 | 列出目录内容 | ls -la/tree |
| 24 | 查看文件类型 | file |
| 25 | 复制文件目录等操作 | cp/scp/rsync |
| 26 | 系统常用命令 | ps/top/free/kill/systemctl |
| 27 | VIM | vi/vim 操作快捷键 |
| 28 | 软件包管理命令(RPM) | 安装/删除/升级/更新/查询 |

## 使用建议

- 该文适合作为**日常运维速查手册**，不适合从零学习 Linux
- 命令按场景分组，查找效率高
- 文中部分命令有简短中文说明（如 `uname -m 显示机器的处理器架构`）

## 关联
- 概念：Linux命令分类速查
- 相关来源：无（本 wiki 首个 Skill/linux 来源页）

---
> 📎 **物理文献**：[[raw/playbooks/能用到“退休”的 600条 Linux 命令，可以解决日常99%的问题~.md]]