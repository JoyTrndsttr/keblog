# 从 Mac 拷贝目录迁移

本次整理将 `Daily Plan/personal-site` 中的有效应用代码提升至仓库根目录。

- 移出外围阅读资料、PDF、聊天历史和提示词。
- 移出未参与当前构建的 Next/React 模板、旧依赖和锁文件、Sites 空配置、Mac 缓存及一次性聊天导入脚本。
- 原始资料及被移出的模板保存在仓库旁的 `keblog-import-backup-<时间>/`，不进入 Git。
- 已有本地阅读数据迁移到纳入 Git 的 `content/daily-learning/`，原 `content` 一并保留。
- 不删除网站中的 `/daily-learning/` 页面或相关 API。

VPS 上的数据仍以当前服务的数据目录为准。不要将本地笔记自动覆盖到线上。需要导入时，先备份双方并比较时间与内容，再通过 API 或人工合并。

旧仓库的 Git 历史和 origin 保持原样。本次整理不会重建 Git 仓库或改写历史。
