# VPS 部署

使用 Python 3.10+、Node.js 22.13+、Caddy 和 systemd。以下示例沿用原部署的服务名与路径，避免影响已有运行数据。

## 首次部署

1. 在 VPS 准备服务账户 `wangke-site`，将仓库克隆到 `/opt/wangke-site/current`。代码由部署用户维护，服务账户只需要读取权限。
2. 运行 `node scripts/build.mjs`。
3. 创建 `/var/lib/wangke-site`，将其所有者设为 `wangke-site:wangke-site`。如迁移已有数据，先备份再合并，不能覆盖线上新数据。
4. 创建 `/etc/wangke-site.env`，权限设为 `600`，使用以下内容并填入独立生成的 Token：

```dotenv
SITE_HOST=127.0.0.1
SITE_PORT=8080
SITE_DATA_DIR=/var/lib/wangke-site
SITE_PUBLIC_URL=https://example.com
SITE_API_TOKEN=replace-with-a-generated-secret
```

5. 将 `deploy/wangke-site.service` 安装到 `/etc/systemd/system/`，执行 `sudo systemctl daemon-reload` 和 `sudo systemctl enable --now wangke-site`。
6. 修改 `deploy/Caddyfile` 的 `example.com` 为真实域名，配置 DNS 后合并到 VPS 的 Caddy 配置中。保留其他网站配置，并确保日志目录可写；验证 Caddy 配置后 reload。
7. 检查 `curl -f http://127.0.0.1:8080/api/v1/bootstrap`，以及公网首页和 `/api/openapi.json`。

已有 VPS 应先用 `systemctl cat wangke-site` 检查实际配置。可以继续使用原域名；务必在 `SITE_PUBLIC_URL` 中填写同一地址。

## 后续更新

Mac 上提交并推送代码后，在 VPS checkout 中执行：

```bash
cd /opt/wangke-site/current
git status --short
git pull --ff-only
python3 -m unittest discover -s tests -v
node scripts/build.mjs
sudo systemctl restart wangke-site
sudo systemctl status wangke-site --no-pager
curl -f http://127.0.0.1:8080/api/v1/bootstrap
```

工作区存在本地改动时先处理；拉取或验证失败时停止后续步骤。首次将旧的手工上传目录接入 Git 时，将其备份后建立干净 checkout，不在旧目录强制覆盖。

## 数据和备份

- `documents/`：Paper Pool、任务提示词等文档。
- `daily-learning/`：阅读笔记，单篇为 `<slug>/README.md`，索引和计划为 `README.md` 与 `PLAN.md`。
- `files/`：上传附件。
- `backups/`：API 覆盖文件前的备份。

默认均位于 `/var/lib/wangke-site`。额外路径可用 `SITE_LEARNING_DIR`、`SITE_TASK_PROMPT_FILE` 指定，同时相应调整 systemd 的 `ReadWritePaths`。定期独立备份数据目录和环境配置；Git 只管理代码。回滚代码不会回滚内容数据。
