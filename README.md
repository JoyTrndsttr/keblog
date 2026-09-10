# keblog

个人网站与论文阅读归档项目。前端使用原生 HTML、CSS、JavaScript，后端使用 Python 标准库，支持个人主页、研究方向、论文列表、博客、Paper Pool 和阅读笔记。

Research 页面从私有 `JoyTrndsttr/causal-review` 仓库同步并只公开 `documents/研究记录.md`。VPS 使用仓库级只读 Deploy Key，其他仓库文件均不提供网页或 API 入口。

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
python3 server/server.py --dev
```

访问 http://127.0.0.1:8080 。编辑 `src-static/` 后刷新页面即可。开发模式以 `content/` 中的旧 Markdown 为首次迁移来源，并在其中生成被 Git 忽略的 `paperpool.sqlite3`。写入 API 需要自行设置 `SITE_API_TOKEN`；留空时禁止写入。

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
# 使用构建产物启动（先按上文导入环境变量）
python3 server/server.py
```

也可使用 `npm run dev`、`npm run build`、`npm test` 和 `npm start`；无需执行 `npm install`。

## 目录

```text
src-static/     网站页面、样式与浏览器脚本
server/         Python HTTP 服务与文档 API
scripts/        静态构建脚本
tests/          后端单元测试
deploy/         Caddy 与 systemd 配置示例
docs/          部署及迁移说明
content/        初始论文池、阅读笔记与计划
dist/          构建产物（不提交）
```

首次启动会把 `content/` 中的论文池、阅读笔记、计划和提示词迁移到 SQLite。之后数据库是唯一事实源，网站展示的 Markdown 由数据库生成，客户端无需修改表格或索引文件。VPS 数据位于 `/var/lib/wangke-site`，Git 更新不会覆盖线上数据库。

## Git 与部署

在 Mac 上开发并完成测试后 commit / push；VPS 使用独立 checkout 拉取代码、构建并重启服务。线上数据保存在 `/var/lib/wangke-site`，不随源码更新覆盖。

- [VPS 部署与更新](docs/deployment.md)
- [旧目录迁移说明](docs/migration.md)
- [API 文档](API.md)
- [ChatGPT 每日任务接口说明](docs/chatgpt-task.md)
- [贡献说明](CONTRIBUTING.md)

## 许可

当前重建版本暂未指定开源许可证；公开代码不等同于授予开源使用许可。发布正式版本前由维护者确定许可证，并核对复用代码和素材的授权。
