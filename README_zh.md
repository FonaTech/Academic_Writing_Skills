# Academic Writing Skills 学术写作技能包

**2.1.0 合并版，2026-11-01。** 六个写作技能，支持不同学科的综述、研究论文、学位论文、申请书和审稿回复；按需求生成英文或中英文稿。

本版以通过测试的 Generic v2 实现为基础，合入本机 1.1 与 GitHub 当前版本中有用的写作规则和构建功能。恢复详细综述叙事、文章结构、审稿意见分流、长短稿联动、自动年份和数学函数排版，同时保留严格证据溯源、声明式内容源、双语检查和真实审查记录。具体取舍见 [合并说明](MERGE_NOTES.md)，实测范围见 [验证记录](VALIDATION.md)。

| 技能 | 负责内容 |
|---|---|
| sci-writing-orchestrator | 问题、范围、专业视角、论证、模式路由和持续更新的写作计划 |
| sci-literature-evidence | 检索筛选、来源身份、原话页码、原始数据与推导溯源 |
| sci-prose-style | 逐节起草、连贯短句、术语、数量表述和对齐翻译 |
| sci-figure-design | 图表论点、代码数据图、示意图提示词、图注与确定性拼图 |
| sci-manuscript-build | JSON/Markdown 与可信旧 Python 内容源、编号、公式、年份、变体和审查新鲜度 |
| sci-manuscript-review | 十二维审查、反证、外部意见分流、逐条回复和版本同步 |

## 默认写作规则

默认 precise：一句一个主要论断，一段围绕一个问题，主题句优先；英文中位句长目标 16–20 词，上限约 30 词。避免夸张、空泛套话和写作过程元评论。保留必要条件、否定、误差和技术含义；不为了通过风格诊断删掉科学限定。compact、explanatory、generic 仅按需启用，不能放宽证据要求，也不保证 AI 检测结果。

叙述性综述写领域的发展、分歧与综合；系统/范围综述仍需如实报告检索、筛选和评价方法。用户已有 AGENTS.md 规范优先；中英文、长短稿只在请求时生成，生成后保持科学含义和事实同步。

## 安装

需要 Python 3.10+。在包根目录执行：

```bash
python3 -m pip install -r requirements-core.txt
python3 tools/install.py --status --targets codex
python3 tools/install.py --targets codex --no-inject
```

Claude Code / OpenCode 分别使用 --targets claude / --targets opencode。--no-inject 保留已有全局规范；只有有意更新标记规范块时才省略。旧技能移入带时间戳的备份目录；安装器会提示 Codex 重复发现位置，不自动删除另一套。无参数安装仍兼容，面向三个客户端。项目级安装增加 --project DIR --no-inject。

Claude Code 支持相应插件命令的版本可使用：

```text
/plugin install academic-writing-skills --marketplace FonaTech/Academic_Writing_Skills
```

安装后新开会话，检查实际发现列表。[Codex](codex/INSTALL.md)、[Claude Code](claude-plugin/INSTALL.md)、[OpenCode](opencode/INSTALL.md) 有单独说明。

## 新建项目与构建

```bash
python3 skills/sci-manuscript-build/scripts/new_project.py ./Paper --slug Paper --type article --languages en zh
cd Paper
# 根据真实材料编辑配置、分节内容、图表、证据和参考文献
python3 pipeline.py --stage preview
```

第一种语言决定编号，程序不自动翻译。默认只生成请求的主要文档；无引用和纯参考文献版本在 manuscript.json 中按需启用。正文放在有序 JSON 块或引用的 Markdown 段落中；可信旧版 content.py / floats.py 仍可使用。已有 Word 小改、短 Markdown 稿或期刊指定 LaTeX 模板不强制迁移。

表格支持 year_column 和 year_inline，由 references.json 自动生成年份；缺失有效年份时失败。行内 \ln、\exp 等函数保持正体；复杂原生展示公式仍需 Pandoc。构建器先检查所有目标 DOCX 的 Word 锁文件，再开始写入。

用构建技能的 render_check.py 渲染当前 DOCX，并查看每一页。实际完成科学与视觉审查后，用 record_review.py 记录真实审查者、范围和局限，再执行 python3 pipeline.py --stage release。源文件变化会使旧构建/审查过期；脚本通过、AI 自审和人工作者验收分别记录。

## 证据、图表与风格工具

文献数字保留完整原话与页码；原创/推导结果保留原始文件哈希、定位、方法、代码和输入链。结果方法、来源角色、访问状态分开记录。有 DOI 的文献先核验 Crossref；无 DOI 来源保留稳定标识和人工身份核对路径。相同数字或哈希不能证明引文语义正确。

数据图由代码从来源值生成。图像模型只处理示意图和不含数据的数据槽布局；最终数据面板由代码拼入，按 RGB/哈希精确核对。提示词保留标签白名单、无文字回退和项目自定义图形提示。

```bash
python3 skills/sci-prose-style/scripts/prose_lint.py draft.md --json --known DNA,RNA
```

--known 与四种风格可同时使用，短段落/断裂短句只作建议。例外词表不免除图注中的独立缩写定义。可选文献/PDF/绘图依赖见 requirements-research.txt。[16 个案例](skills/sci-writing-orchestrator/case-studies/INDEX.md)为教学情境及历史公开来源访问记录，不是已执行研究或专家质量基准。

## 验证与上传

```bash
python3 tools/sync_plugin_manifests.py
python3 tools/validate_skills.py
python3 -m unittest discover -s tests -v
python3 tools/checksums.py
```

ZIP 包含隐藏 .claude-plugin 与 .github 文件。上传到仓库根目录时保留隐藏文件，不要多嵌套一层版本目录。网页上传漏掉隐藏插件清单时，可核对可见镜像后运行 python3 tools/sync_plugin_manifests.py --write。每次有意修改源码后重新验证，再运行 python3 tools/checksums.py --write。

详见 [上传说明](UPLOAD_zh.md)。已附 GitHub Actions 配置，托管运行等待上传后执行。原有两份 MIT 署名均保留于 [LICENSE](LICENSE)。
