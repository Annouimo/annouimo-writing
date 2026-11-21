# 写作仓库发布说明

本仓库保存写作原稿；博客站点由独立的 `Annouimo/annouimo-publishing` 工程构建。发布脚本只导入 Front Matter 中 `publish: true` 且未标为草稿的文章。

## 当前流程

- 正式博客入口：<https://blog.annouimo.com/>。
- 写作源稿更新后，由发布工程导入并构建；写作仓库本身不直接发布生产站点。
- `migration/astro` 的 PR #1 是尚未合并的迁移验证草稿，负责生成短期构建产物与隔离预览，不会更新生产。
- `.github/workflows/publish.yml` 是已停用的旧 Hugo 发布流程，不要手动触发。

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

已发布文章不要随意更改 slug，否则旧链接可能失效。发布前在独立发布工程中检查生成页面与预览结果。
