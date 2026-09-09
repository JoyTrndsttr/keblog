# 贡献说明

请先通过 Issue 说明问题或提议，再创建主题分支提交修改。一次 PR 聚焦一个问题，说明行为变化及验证结果。

```bash
git switch -c feat/your-change
python3 -m unittest discover -s tests -v
node scripts/build.mjs
```

页面与样式在 `src-static/`，后端在 `server/`。保持项目无需第三方运行依赖；新增依赖时说明必要性。API 行为变更同步更新 `API.md` 和相应测试。

不要提交 `.env`、Token、运行数据、聊天记录、论文附件或构建产物。贡献中引用第三方代码或素材时保留来源和许可说明。
