# 写作仓库发布说明

本仓库保存写作原稿；博客由独立的 `Annouimo/annouimo-publishing` 工程构建。构建只导入 Front Matter 中 `publish: true` 且未标为草稿的文章。

## 日常发布

- 正式博客：<https://blog.annouimo.com/>。
- `main` 上的文章 Markdown、讲义以外的写作 Markdown和图片有更新时，`.github/workflows/publish-astro.yml` 会自动导入发布内容、读取 Astro 工程当前锁定的讲义和共享样式版本、构建并部署博客。
- 该工作流也可以在 GitHub Actions 中手动运行，供讲义更新后发布。

## 发布讲义更新

讲义由 `Annouimo/annouimo-notes` 管理，博客不会自动追踪其最新提交：

1. 将审阅通过的讲义合入 `annouimo-notes/main`。
2. 在 `annouimo-publishing` 更新 `notes.lock`，写入讲义仓库的完整 40 位提交 SHA，并先检查博客预览。
3. 合入锁文件更新后，在本仓库 GitHub Actions 中手动运行 **Publish Astro blog**。工作流读取最新的 `annouimo-publishing/main` 与该锁定版本，再发布生产站。

这样每次讲义发布都能对应到明确审核过的源码提交。

## 文章约定

```yaml
---
标题: 示例文章
发表日期: 2026-11-14
slug: example-post
publish: true
---
```

栏目由顶层目录决定：`随笔 → blog`、`研究 → research`、`个人经历 → about`、`社会 → society`。缺失或重复的 slug、缺失图片、无法转换的 Obsidian 链接会让构建失败。为避免意外公开，图片只允许位于当前文章目录或其子目录。

已发布文章不要随意更改 slug，否则旧链接可能失效。旧 Hugo 工作流已退役；生产发布只走 Astro 工作流。
