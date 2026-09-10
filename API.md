# keblog 只读内容接口

Base URL：`https://keblog.lol`。

GitHub 仓库中的 `content/` 是 Paper Pool、每日计划和论文精读的唯一事实源。HTTP 服务只负责把当前 checkout 中的 Markdown 提供给网站，不接受内容写入，也不使用 SQLite。

## 接口

| Method | URL | 内容 |
|---|---|---|
| GET | `/api/health` | 服务状态与内容来源 |
| GET | `/api/documents/paperpool.md` | `content/documents/paperpool.md` |
| GET | `/api/daily-learning` | 扫描精读目录生成的元数据列表 |
| GET | `/api/daily-learning/{slug}` | 指定精读的 Markdown |
| GET | `/api/daily-learning/index` | `content/daily-learning/README.md` |
| GET | `/api/daily-learning/plan` | `content/daily-learning/PLAN.md` |
| GET | `/api/v1/prompt` | `content/support/prompt.txt` |
| GET | `/api/v1/bootstrap` | 兼容读取：论文池、计划、提示词和精读列表 |
| GET | `/api/research/document` | VPS 私有研究仓库缓存中的《研究记录.md》 |

所有 `POST`、`PUT`、`PATCH` 和 `DELETE` 请求返回 `405 Method Not Allowed`。`/api/v2/*` 已移除。

## 发布流程

计划任务通过 GitHub 连接器完成一次每日发布：

1. 读取 `content/documents/paperpool.md` 与 `content/daily-learning/README.md`。
2. 按 DOI、arXiv ID、规范化标题依次查重。
3. 创建 `content/daily-learning/YYMMDD-FirstAuthor-ShortName/README.md`。
4. 同步更新精读索引和 Paper Pool。
5. Commit 并 push 到 `master`。
6. GitHub Webhook 触发 VPS 的 `deploy/update.sh`，完成 pull、测试、构建和重启。

Webhook 不携带文章正文，不解析 Markdown，也不写数据库。Git 历史提供版本记录与恢复能力。
