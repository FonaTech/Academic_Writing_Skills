# 学术写作技能包（Academic Writing Skills）

面向 Claude Code、Codex 与 OpenCode 的科研写作技能系统：综述、研究论文、快报、审稿回复、学位论文与基金申请书的规划、文献与证据、英文与中文写作、构建、绘图和审查。

本技能包提炼自胡老师课题组 2026 年 CNT 类脑综述（第 4–7 章）的完整重构过程，以及对课题组文献库中 137 篇论文的写作分析。核心做法：先审查再动笔；每个数字都能追溯到原文页码；中英文共用同一份内容源；图像模型只画示意图；交付前做对抗式审查。

## 六个技能

| 技能 | 用途 |
|---|---|
| `sci-writing-orchestrator` | 任何论文项目的总控：模式路由、设计确认、写作计划、里程碑、子代理分工、完成标准 |
| `sci-literature-evidence` | 文献检索（OpenAlex）、文献库整理、带页码的全文抽取、证据表、引文原句复核、Crossref DOI 核验、引用审查、公平比较规则 |
| `sci-prose-style` | 顶刊风格英文与同步中文：写作规范、分轮修改、去 AI 味词表、分章节写作指南与范例库、术语表、文本检查脚本 |
| `sci-figure-design` | 图表规划、按印刷尺寸绘制的数据子图、图规格文件、Nano Banana Pro 提示词、不改动数据像素的拼图与校验、图注与表格 |
| `sci-manuscript-build` | 单一内容源生成中英 Word 文档：引用自动编号、图表自动就位、原生公式、专栏、章节交叉引用、无引用版与参考文献版、检查与页面渲染 |
| `sci-manuscript-review` | 十维度审查、反驳复核、投稿就绪评分、模拟审稿、审稿意见回复 |

## 安装

```bash
python3 tools/install.py            # 同时安装到 Claude Code、Codex、OpenCode，并注入全局说明
python3 tools/install.py --status   # 查看安装位置
python3 tools/install.py --uninstall
```

- Claude Code：`~/.claude/skills/`，全局说明写入 `~/.claude/CLAUDE.md` 的标记块。
- OpenCode：原生读取 `~/.claude/skills` 和 `~/.claude/CLAUDE.md`，无需重复安装；仅当关闭了 Claude 兼容时才复制到 `~/.config/opencode/skills`。
- Codex：`~/.codex/skills/`，全局说明写入 `~/.codex/AGENTS.md` 的标记块。

首次修改前会备份原文件；重复安装只替换标记块，不会重复追加。

## 新建项目

```bash
python3 skills/sci-manuscript-build/scripts/new_project.py ~/Papers/MyReview --slug MyReview --type review --chapter 4
cd ~/Papers/MyReview && python3 build_manuscript.py && python3 check_manuscript.py
```

然后对代理说：“用 sci-writing-orchestrator 根据本目录的草稿和 ../Library 的文献规划第 4–7 章。”

## 依赖
Python 3.9+、python-docx、lxml、PyMuPDF、Pillow、matplotlib、numpy、PyYAML、requests；文献库 Excel 表需 openpyxl；rapidfuzz 可选（标题匹配更快）；图像校验需 scikit-image；公式需 pandoc（或 pypandoc-binary）；离线会议转写需 transformers、torch、ffmpeg；页面渲染需 Word 或 LibreOffice。OpenAlex 匿名额度按 IP 共享，建议设置 `OPENALEX_API_KEY`。

## 写作规则的唯一来源

句长目标、词频上限和禁用词都在 `skills/sci-prose-style/assets/style_limits.json`。文本检查脚本 prose_lint.py 和稿件检查脚本 check_manuscript.py 读取同一份规则；稿件工具包里有一份相同的副本，校验脚本会检查两者是否一致。单个项目可在 `manuscript.json` 的 `style.overrides` 中按条目名称调整。

## 校验与溯源

`python3 tools/validate_skills.py` 检查元数据、所有引用文件、截断与未闭合代码块、脚本可运行性、插件清单和共享规则副本。`provenance/craft-corpus/` 记录语料分析的来源与方法，不随技能安装；其中含对具体论文的批评性笔记，公开仓库前请先审阅。
