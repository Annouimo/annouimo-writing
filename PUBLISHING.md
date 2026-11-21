# 写作站点发布

本仓库保存写作原稿；站点构建在独立的 `Annouimo/annouimo-publishing` 仓库中完成。发布脚本只导入 Front Matter 中 `publish: true` 且未标为草稿的文章。

## 预览

`migration/astro` 分支的 GitHub Actions 会检出固定版本的 Astro 站点，导入本分支已发布文章并构建静态资源，供预览发布使用。写作仓库中的旧 Hugo 生产工作流已退役，不会再部署生产页面。

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

已发布文章不要随意更改 slug，否则旧链接可能失效。生产发布由后续独立发布流程负责；预览构建不会部署到生产。
