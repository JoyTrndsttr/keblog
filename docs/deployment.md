# Git 仓库部署（lab-vps）

网站：https://keblog.lol 。Caddy 转发到 `127.0.0.1:8080`。

## 当前布局

- `/opt/keblog`：GitHub `JoyTrndsttr/keblog` 的 Git checkout。
- `keblog.service`：从 checkout 的 `dist/` 提供页面与 Python API。
- `/etc/keblog.env`：服务器私有环境变量与原有 Token，不进入 Git。
- `/var/lib/wangke-site`：保留的线上数据目录，API 新内容不被 git pull 覆盖。
- `/opt/keblog-migration-backup-*`：迁移前代码、数据和服务配置备份。

旧 `wangke-site.service` 已停用；旧手工上传 release 目录移入迁移备份，不再用于日常部署。服务账户沿用 `wangke-site`，以保持数据权限兼容。

## 更新

本地开发、测试并由维护者明确提交和推送后：

```bash
ssh lab-vps
sudo bash /opt/keblog/deploy/update.sh
```

脚本要求工作区干净，使用 `git pull --ff-only`，运行测试与 Python 静态构建，再更新 systemd 配置并重启 `keblog`，最后检查 API。

首次迁移时部署脚本和文档作为尚未提交的本地改动同步到了 VPS。维护者提交并推送同样改动后，先备份 VPS 的这些文件，再将 checkout 对齐对应提交，之后才使用更新脚本；不要直接覆盖不明本地改动。

## 构建

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

VPS 仅需 Python 3.10+、Git、curl、Caddy 和 systemd。`node scripts/build.mjs` 仍可用于 Mac 开发，输出相同静态文件，不需要在 VPS 安装 Node。

## 内容同步

Git 中的 `content/` 是可发布内容，线上 API 使用 `/var/lib/wangke-site`。首次迁移只补充缺失文件，保留已存在的线上文档。之后需要发布内容时，比较并合并这两个目录，再重启或刷新；不要以 git pull 覆盖 API 产生的新数据。Token、上传附件和 API 备份不进入代码仓库。

## 检查与恢复

```bash
sudo systemctl status keblog --no-pager
sudo journalctl -u keblog -n 50 --no-pager
curl -f https://keblog.lol/api/v1/bootstrap
```

更新失败时先查看日志。代码可切回上一已验证提交，重新构建并重启；操作前保存本地改动。数据应独立备份，代码回滚不回滚数据。迁移备份中的旧服务和 release 可用于首次切换故障恢复。

## HTTPS

Caddy 为 `keblog.lol` 自动申请并续期证书，HTTP 自动跳转 HTTPS。旧域名 `38-76-161-31.sslip.io` 保留可用。`SITE_PUBLIC_URL=https://keblog.lol`。`www.keblog.lol` 尚未配置 DNS，不在当前站点配置中。
