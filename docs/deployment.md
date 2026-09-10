# Git 仓库部署（lab-vps）

网站：https://keblog.lol 。Caddy 转发到 `127.0.0.1:8080`。

## 当前布局

- `/opt/keblog`：GitHub `JoyTrndsttr/keblog` 的 Git checkout。
- `keblog.service`：从 checkout 的 `dist/` 提供页面与 Python API。
- `/etc/keblog.env`：服务器私有环境变量与原有 Token，不进入 Git。
- `/var/lib/wangke-site`：线上数据目录；`paperpool.sqlite3` 是论文、精读和任务配置的事实源。
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
