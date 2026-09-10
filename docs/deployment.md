# Git 仓库部署（lab-vps）

网站：https://keblog.lol 。Caddy 转发到 `127.0.0.1:8080`。

## 当前布局

- `/opt/keblog`：GitHub `JoyTrndsttr/keblog` 的 Git checkout。
- `keblog.service`：从 checkout 的 `dist/` 提供页面与 Python API。
- `/etc/keblog.env`：服务器私有环境变量与原有 Token，不进入 Git。
- `/var/lib/wangke-site`：线上数据目录；`paperpool.sqlite3` 是论文、精读和任务配置的事实源。
- `/var/lib/wangke-site/research-source`：私有 `causal-review` 仓库的稀疏只读副本，仅同步 `documents/`。
- `/var/lib/wangke-site/research-cache/research-record.md`：Research 页面使用的稳定本地缓存。
- `/opt/keblog-migration-backup-*`：迁移前代码、数据和服务配置备份。

旧 `wangke-site.service` 已停用；旧手工上传 release 目录移入迁移备份，不再用于日常部署。服务账户沿用 `wangke-site`，以保持数据权限兼容。

## 更新

本地开发、测试并由维护者明确提交和推送后：

```bash
ssh lab-vps
sudo bash /opt/keblog/deploy/update.sh
```

脚本要求工作区干净，使用 `git pull --ff-only`，运行测试与 Python 静态构建，再更新 systemd 配置并重启 `keblog`，最后检查 API。

首次迁移时部署脚本和文档作为尚未提交的本地改动同步到了 VPS。维护者提交并推送同样改动后，先备份 VPS 的这些文件，再将 checkout 对齐对应提交，之后才使用更新脚本；不要直接覆盖不明本地改动。

## GitHub Webhook 自动部署

GitHub 向 `POST https://keblog.lol/github-webhook` 发送 `master` 分支的 push 事件。独立的 `keblog-webhook.service` 在 `127.0.0.1:8090` 验证 `X-Hub-Signature-256`、仓库名和分支，然后异步启动 `keblog-update.service`。Webhook 不接收文章正文，也不修改 SQLite；更新仍由 `deploy/update.sh` 完成。

Secret 只保存在权限为 `600` 的 `/etc/keblog-webhook.env`。GitHub Webhook 配置使用相同 Secret、`application/json`、仅 Push events，并保持 SSL verification 启用。检查服务与部署日志：

```bash
sudo systemctl status keblog-webhook --no-pager
sudo journalctl -u keblog-webhook -n 50 --no-pager
sudo journalctl -u keblog-update -n 100 --no-pager
```

未签名的公网 POST 应返回 `401`。GitHub 的签名 ping 应返回 `200 pong`，目标分支 push 应返回 `202 deployment queued`。论文与精读状态仍以 SQLite `/api/v2/` 为事实源；Webhook 不恢复旧 Markdown 写入流程。

## 构建

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

VPS 仅需 Python 3.10+、Git、curl、Caddy 和 systemd。`node scripts/build.mjs` 仍可用于 Mac 开发，输出相同静态文件，不需要在 VPS 安装 Node。

## 数据与迁移

首次运行 v2 API 时，服务把 `/var/lib/wangke-site/documents/paperpool.md`、`daily-learning/`、计划和提示词一次性迁移到 `/var/lib/wangke-site/paperpool.sqlite3`。迁移标记阻止重复导入，旧 Markdown 留作历史副本。

上线后通过 `/api/v2/` 维护论文、精读和简报。不要再把 Git 中的 `content/` 覆盖到线上，也不要直接编辑旧 Paper Pool 表格。Token、SQLite 数据库、上传附件和 API 备份不进入代码仓库。

备份 SQLite 时，优先停止 `keblog` 后复制数据库，或使用 SQLite backup API；不要在写入过程中只复制单个 WAL 模式文件。API v2 首次迁移前的完整备份位于 `/opt/keblog-api-v2-backup-*`。

## 检查与恢复

```bash
sudo systemctl status keblog --no-pager
sudo journalctl -u keblog -n 50 --no-pager
curl -f https://keblog.lol/api/v2/context
curl -f https://keblog.lol/api/openapi.json
```

更新失败时先查看日志。代码可切回上一已验证提交，重新构建并重启；操作前保存本地改动。数据应独立备份，代码回滚不回滚数据。迁移备份中的旧服务和 release 可用于首次切换故障恢复。

## HTTPS

Caddy 为 `keblog.lol` 自动申请并续期证书，HTTP 自动跳转 HTTPS。旧域名 `38-76-161-31.sslip.io` 保留可用。`SITE_PUBLIC_URL=https://keblog.lol`。`www.keblog.lol` 尚未配置 DNS，不在当前站点配置中。

## Research 文档同步

VPS 的 `/root/.ssh/causal_review_deploy` 是 GitHub 仓库级只读 Deploy Key，权限为 `600`。SSH 别名 `github-causal-review` 强制使用该身份和严格主机校验；GitHub 主机键来自其官方公布的 Ed25519 主机键。

`keblog-research-sync.timer` 每 5 分钟运行 `deploy/sync-research.sh`，以 `git pull --ff-only` 更新稀疏 checkout，再原子替换本地缓存。同步失败不会删除或截断现有缓存，页面继续展示上次成功版本。手工检查：

```bash
sudo systemctl start keblog-research-sync.service
sudo systemctl status keblog-research-sync.service --no-pager
sudo systemctl list-timers keblog-research-sync.timer --no-pager
```

应用从同步副本读取文档，但只通过固定的 `/api/research/document` 公开 `研究记录.md`。接口不接受文件名或路径，`README.md`、`writings.md`、`dialog*.md` 和其他文件均不提供公网路由。撤销访问时，在 GitHub 仓库 Deploy keys 中删除 `lab-vps keblog research sync`，再删除 VPS 私钥并停用 timer。
