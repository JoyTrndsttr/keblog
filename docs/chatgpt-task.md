# ChatGPT 每日任务的 GitHub 工作流

前提：ChatGPT 计划任务已连接 GitHub，并获准读取和修改 `JoyTrndsttr/keblog`。计划任务不调用 keblog API，也不需要 Bearer Token。

每次执行：

1. 从 `master` 读取 `content/documents/paperpool.md` 和 `content/daily-learning/README.md`。
2. 以 DOI、arXiv ID、规范化标题为优先级完成永久去重，再选择当天论文。
3. 生成完整精读到 `content/daily-learning/YYMMDD-FirstAuthor-ShortName/README.md`。
4. 在精读索引顶部增加对应行，并更新归档数量与日期范围。
5. 在 Paper Pool 中登记为已精读；若原来是候选，移除或关闭活跃候选项。
6. 提交前重新读取目标文件，避免覆盖任务开始后产生的新提交。三个文件必须保持一致。
7. Commit 并 push 到 `master`，建议消息：`content(daily-learning): add YYYY-MM-DD paper reading`。
8. 只有 GitHub 返回成功后才报告发布成功。Webhook 会自动通知 VPS 部署，任务不需要访问或等待 keblog 页面。

完整选题和论文讲解不清楚时，使用 `content/support/prompt.txt`。不得提交 GitHub 凭据、Webhook Secret、邮件内容或其他私密信息。
