# 每日任务的 keblog 接口说明

前提：执行任务的客户端已连接可调用 HTTPS API 的工具，并将 `SITE_API_TOKEN` 存在工具的 Bearer 认证配置中。普通浏览工具不能代替带认证的写入工具；不要把 Token 写进任务提示词。

以下可作为任务说明中的发布部分：

```text
keblog 基础地址：https://keblog.lol
接口定义：https://keblog.lol/api/openapi.json

1. 首先 GET /api/v2/context，读取研究方向、计划、候选和近期完成记录。
   context.apiInstructions 与 OpenAPI 是接口依据；旧导入计划中的 v1 写入路径已停用。
2. 为新选题查重时，将至多 50 个 DOI/arXiv/标题合成一次 POST /api/v2/papers/lookup。
   已读论文不再选择，除非用户明确要求重读。
3. 生成完整、有来源、区分事实和推断的中文精读 Markdown。
4. POST /api/v2/readings 一次提交：已有论文用 paperId，新论文用 paper 对象；
   同时传 slug、date、content。不要下载并手工重写 Paper Pool 表格。
5. 为本次提交固定一个 Idempotency-Key，网络失败时用原键和原 JSON 重试。
   201 为创建成功，200 且 replayed=true 为此前已经成功。
   409 需检查是已读、重复 slug、版本冲突还是键冲突，不得换键盲目重发。
6. 最终报告成功返回的阅读链接；没有服务器成功响应就明确说“尚未保存”。
7. 如果需要保存当天简报，PUT /api/v2/briefs/YYYY-MM-DD，首次用 version:0。
   修改笔记或简报先 GET 取得 version，再 PUT；不调用 DELETE。
```

常规精读只需要读取上下文和提交结果两个请求；新论文可增加一个批量查重请求。需要获取论文原文时由客户端自行检索，keblog 不负责下载、阅读或生成论文内容。

这些接口提供任务所需的数据读写能力，不会自动赋予 ChatGPT 网页计划调用权限，也不会在 VPS 创建计划任务。
