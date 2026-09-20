# Paper Pool

> Paper Pool 已按月份拆分，避免单文件持续膨胀。永久去重只需读取 `paperpool_short.md`；详细信息默认只读取当前月份文件。

## 文件

- `paperpool_short.md`：所有已精读论文标题，仅用于快速永久去重。
- `paperpool_202608.md`：2026 年 8 月完整记录。
- `paperpool_202609.md`：2026 年 9 月完整记录与当前待精读列表。

## 维护规则

- 每完成一篇精读：把论文标题追加到 `paperpool_short.md`，把完整条目写入当月 `paperpool_YYYYMM.md`。
- 日常运行不再扫描全部历史详细记录；先用 short 去重，再读当前月份详细文件。
- 跨月时新建新的 `paperpool_YYYYMM.md`，旧月份保持归档。
- `paperpool.md` 只作为轻量入口/说明，不再保存论文完整条目。
