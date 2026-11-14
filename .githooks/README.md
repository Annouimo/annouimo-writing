# 本地提交检查

本仓库使用只读的 pre-commit 检查：只有 `publish: true` 且未标记 `draft: true` 的 Markdown 文章才需要有效的 `slug`。缺少 slug 时会输出可复制给 AI 的批量提示词并阻止提交。

首次克隆后，在仓库根目录运行一次：

```sh
git config --local core.hooksPath .githooks
```

需要 Mac 上的 `python3`。VS Code 等图形界面会在 Git 输出中显示失败原因；hook 不进行任何交互，也不修改文件。

校验使用 Git **暂存区** 的内容，因此修改 Front Matter 后请重新暂存。也可手动运行 `python3 scripts/check_publish.py`。

注意：本地 hook 不会随克隆自动启用，也可被绕过。正式部署工作流仍应运行相同的校验。当前冲突检测按顶层目录和 slug 组合判断，部署端应以最终 Hugo section 映射为准。

`publish: true` 必须使用未加引号的布尔值；`publish` 缺失或为 `false` 的文章不会发布。当前检查器专门读取 Front Matter 的简单顶层标量字段，不是完整 YAML 解析器。
