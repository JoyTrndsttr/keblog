# keblog

个人网站与论文阅读归档项目。前端使用原生 HTML、CSS、JavaScript，后端使用 Python 标准库，支持个人主页、研究方向、论文列表、Paper Pool 和阅读笔记。

Research 页面从私有 `JoyTrndsttr/causal-review` 仓库同步 `documents/研究记录.md` 到 VPS 本地缓存后展示。VPS 使用仓库级只读 Deploy Key；GitHub 暂时不可用时继续展示上一次成功同步的版本，其他仓库文件均不提供网页或 API 入口。

项目仍在持续开发中。当前前端入口为 `src-static/`，构建只是将静态文件复制到 `dist/`，没有第三方运行依赖，也不需要安装 Next.js、React 或 node_modules。

## 本地开发

需要 Python 3.10+；可用 Python 构建；如使用 Node 构建则需要 Node.js 22.13+（`.nvmrc` 指定 22 系列）。

```bash
git clone https://github.com/JoyTrndsttr/keblog.git
cd keblog
cp .env.example .env
# 按需编辑 .env，再导入环境变量
set -a
. ./.env
set +a
python3 server/content_server.py --dev
```

访问 http://127.0.0.1:8080 。编辑 `src-static/` 或 `content/` 后刷新页面即可。Paper Pool、精读索引和精读正文均直接读取 Git 跟踪的 Markdown。

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
# 使用构建产物启动（先按上文导入环境变量）
python3 server/content_server.py
```

也可使用 `npm run dev`、`npm run build`、`npm test` 和 `npm start`；无需执行 `npm install`。

## 目录

```text
src-static/     网站页面、样式与浏览器脚本
server/         Python HTTP 服务与只读内容接口
scripts/        静态构建脚本
tests/          后端单元测试
deploy/         Caddy 与 systemd 配置示例
docs/          部署及迁移说明
content/        初始论文池、阅读笔记与计划
dist/          构建产物（不提交）
```

GitHub 仓库是公开内容的唯一事实源。计划任务同时维护 `content/documents/paperpool.md`、`content/daily-learning/README.md` 和当日精读正文，commit/push 后由 GitHub Webhook 通知 VPS 拉取、构建并重启。Research 页面继续使用 VPS 上私有研究仓库的只读缓存。

## Git 与部署

在 Mac 或 ChatGPT GitHub 连接器中完成修改后 commit / push；VPS 使用独立 checkout 拉取代码、构建并重启服务。

- [VPS 部署与更新](docs/deployment.md)
- [旧目录迁移说明](docs/migration.md)
- [只读内容接口](API.md)
- [ChatGPT 每日任务工作流](docs/chatgpt-task.md)
- [贡献说明](CONTRIBUTING.md)

## 许可

当前重建版本暂未指定开源许可证；公开代码不等同于授予开源使用许可。发布正式版本前由维护者确定许可证，并核对复用代码和素材的授权。
