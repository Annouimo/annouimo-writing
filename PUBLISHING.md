# 自动发布配置

推送 `main` 后，GitHub Actions 会读取本仓库，并从私有的 `Annouimo/annouimo-blog` 获取 Hugo 工程。只有文章 Front Matter 中 `publish: true`（布尔值）的文章才会发布；`draft: true` 仍然阻止发布。缺少 publish 的文件不会公开。

## 首次设置

在 **Annouimo-writing → Settings → Secrets and variables → Actions** 配置：

- `BLOG_REPO_TOKEN`：有权读取私有 `Annouimo/annouimo-blog` 的细粒度 GitHub PAT（该仓库 Contents: Read）。
- `CLOUDFLARE_API_TOKEN`：有权限部署对应 Worker 的 Cloudflare API Token。
- `CLOUDFLARE_ACCOUNT_ID`：Cloudflare 账户 ID。

**未配置密钥前，自动部署不会成功。** 请先配置，再在 Actions → Publish blog 手动触发一次，检查构建与部署结果。

## 发布约定

```yaml
---
标题: 示例文章
发表日期: 2026-11-14
slug: example-post
publish: true
---
```

栏目由顶层目录决定：`随笔 → blog`、`研究 → research`、`个人经历 → about`、`社会 → society`。新目录若要发布，须先在博客工程的 `deploy/sync_config.toml` 添加映射。

发布流程只读写作源文件；缺失 slug、重复 slug、缺失图片或无法转换的 Obsidian 链接都会导致部署中止。为了避免意外泄露，图片只允许位于**当前文章所在目录或其子目录**。若多篇文章引用不同目录下的同名图片，也会中止。

GitHub Actions 负责云端校验；本地 pre-commit 只是辅助检查。文章发布后不要随意更改 slug，否则旧链接可能失效。

首次配置前请确认 Hugo 工程的主题、模块、Wrangler 和 Cloudflare 权限可在 GitHub Actions 环境中正常运行。
