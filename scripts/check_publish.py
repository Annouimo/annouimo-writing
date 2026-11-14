#!/usr/bin/env python3
"""Validate publishable Markdown from the Git index; never modify files."""
import re
import subprocess
import sys
from collections import defaultdict

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY = re.compile(r"^([\w\u4e00-\u9fff-]+):(?:\s*(.*))?$")
MAX_WORDS = 6


def git(*args):
    return subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def scalar(raw):
    value = raw.strip()
    if value.startswith(("'", '"')) and len(value) >= 2 and value[-1] == value[0]:
        value = value[1:-1]
    else:
        value = value.split(" #", 1)[0].strip()
    return value


def frontmatter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}
    fields = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = KEY.match(line)
        if match:
            key, raw = match.groups()
            if key in fields:
                raise ValueError(f"重复字段 {key}")
            fields[key] = scalar(raw or "")
    return fields


def main():
    try:
        paths = [p.decode("utf-8") for p in git("ls-files", "--cached", "-z", "--", "*.md").split(b"\0") if p]
    except (subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        print(f"[publish-check] 无法读取 Git 暂存区: {exc}", file=sys.stderr)
        return 1

    errors, missing, collisions = [], [], defaultdict(list)
    for path in paths:
        try:
            data = git("show", f":{path}")
            meta = frontmatter(data.decode("utf-8-sig"))
        except (subprocess.CalledProcessError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{path}: 无法解析元数据 ({exc})")
            continue

        publish = meta.get("publish")
        if publish is None or publish.lower() == "false":
            continue
        if publish != "true" or re.search(r"^publish:\\s*[\\\"\x27]", data.decode("utf-8-sig"), re.MULTILINE):
            errors.append(f"{path}: publish 必须是 YAML 布尔值 true 或 false（不能加引号）")
            continue
        if meta.get("draft", "").lower() == "true":
            continue
        slug = meta.get("slug", "")
        if not slug:
            missing.append((path, meta.get("副标题") or meta.get("subtitle") or meta.get("标题") or meta.get("title") or path.rsplit("/", 1)[-1].removesuffix(".md")))
            continue
        if not SLUG.fullmatch(slug) or len(slug.split("-")) > MAX_WORDS:
            errors.append(f"{path}: slug 不合规: {slug!r}（小写字母、数字、连字符，最多 6 段）")
            continue
        # Current Hugo mappings: directory name -> section.
        section = path.split("/", 1)[0]
        collisions[(section, slug)].append(path)

    for (section, slug), items in collisions.items():
        if len(items) > 1:
            errors.append(f"slug 冲突 {section}/{slug}: " + ", ".join(items))

    if not errors and not missing:
        print("[publish-check] 公开文章 slug 检查通过")
        return 0
    print("\n[publish-check] 提交已阻止：公开文章元数据检查未通过。", file=sys.stderr)
    for err in errors:
        print("  错误: " + err, file=sys.stderr)
    if missing:
        print("\n缺少 slug 的文章：", file=sys.stderr)
        for i, (path, title) in enumerate(missing, 1):
            print(f"  {i}. {path} — {title}", file=sys.stderr)
        print("\n========== 可复制给 AI 的提示词 ==========", file=sys.stderr)
        print(f"请为以下 {len(missing)} 个中文标题生成简短、准确的英文 URL slug。", file=sys.stderr)
        print("要求：只使用小写英文字母、数字和连字符；不超过 6 个单词；优先表达主题而非逐字翻译。", file=sys.stderr)
        print("严格输出 JSON 对象，键为序号字符串，值为 slug，不要附加解释。\n", file=sys.stderr)
        for i, (_, title) in enumerate(missing, 1):
            print(f"{i}. {title}", file=sys.stderr)
        print("========================================", file=sys.stderr)
    print("\n请在对应文章 Front Matter 中补充或修正 slug，重新暂存后提交。", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
