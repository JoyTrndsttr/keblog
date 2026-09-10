# GitHub Webhook 部署（lab-vps）

网站：`https://keblog.lol`。Caddy 将普通流量转发到 `127.0.0.1:8080`，将 `/github-webhook` 转发到仅监听回环地址的 `127.0.0.1:8090`。

## 当前布局

- `/opt/keblog`：`JoyTrndsttr/keblog` 的干净 Git checkout。
- `content/`：Paper Pool、精读索引、每日计划和精读正文的唯一事实源。
- `keblog.service`：提供静态页面和只读内容接口。
- `keblog-webhook.service`：验证 GitHub HMAC、仓库名和 `master` 分支。
- `keblog-update.service`：运行 `deploy/update.sh`。
- `/etc/keblog-webhook.env`：GitHub Webhook Secret，权限 `600`，不进入 Git。
- `/var/lib/wangke-site/research-source`：私有 `causal-review` 仓库的稀疏只读副本。
- `/var/lib/wangke-site/research-cache/research-record.md`：Research 页面的稳定缓存。

`keblog.service` 通过 `RESEARCH_DOCUMENT_FILE` 明确读取上述缓存，避免内容服务切换后回退到 checkout 内不存在的研究文档。

旧 SQLite 文件可以作为历史备份保留，但服务不再读取或写入它。

## 自动更新

GitHub 向 `POST https://keblog.lol/github-webhook` 发送 push 事件。接收器验证 `X-Hub-Signature-256`、`JoyTrndsttr/keblog` 和 `refs/heads/master` 后，异步启动 `keblog-update.service`。更新脚本要求 checkout 干净，然后执行：

```text
git pull --ff-only
python3 -m unittest discover -s tests -v
python3 scripts/build.py
systemctl restart keblog
GET /api/health
```

GitHub Webhook 使用 `application/json`、仅 Push events，并启用 SSL verification。Webhook 不传递或解析文章正文。

## 手工更新与检查

```bash
sudo systemctl start keblog-update.service
sudo systemctl status keblog keblog-webhook --no-pager
sudo journalctl -u keblog-update -n 100 --no-pager
sudo journalctl -u keblog-webhook -n 50 --no-pager
curl -f https://keblog.lol/api/health
curl -f https://keblog.lol/api/documents/paperpool.md
```

未签名的 Webhook POST 应返回 `401`，GitHub ping 应返回 `200 pong`，目标分支 push 应返回 `202 deployment queued`。

## Research 文档同步

`keblog-research-sync.timer` 每 5 分钟使用仓库级只读 Deploy Key 更新私有 `causal-review` 的稀疏 checkout，再原子替换缓存。失败时保留上一次成功内容。应用只公开固定的 `/api/research/document`，不接受文件名或路径。

```bash
sudo systemctl start keblog-research-sync.service
sudo systemctl status keblog-research-sync.service --no-pager
sudo systemctl list-timers keblog-research-sync.timer --no-pager
```
