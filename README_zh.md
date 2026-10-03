# 学术写作技能包：通用版

六个可复用技能，服务于不同学科的论文、综述、学位论文、申请书和审稿回复。按实际研究类型、领域、读者与任务选择流程；小范围修改只执行相关步骤。

| 技能 | 职责 |
|---|---|
| sci-writing-orchestrator | 问题、范围、角色、论证、流程与完成条件 |
| sci-literature-evidence | 检索筛选、来源身份、带页码证据与数据溯源 |
| sci-prose-style | 逐节写作、自然准确的语言、术语与对齐翻译 |
| sci-figure-design | 展示规划、代码数据图、独立示意图、图注与完整性检查 |
| sci-manuscript-build | 声明式内容源、稳定构建、状态与页面预览 |
| sci-manuscript-review | 科学、来源与视觉审查，反证、返修及审稿回复 |

## 默认风格与身份

默认precise风格：一句一个主要论断，主题句优先，一段围绕一个连贯问题；英文中位句长目标16–20词，上限约30词。避免夸张、套话、模板化转折和写作过程的元评论。必要条件、否定、误差与技术含义优先保留；句长是编辑目标，不是科学有效性的阈值。中文按含义和自然语法审查，不套英语词数。

compact、explanatory、generic三种替代风格按需选择。全部遵守证据要求，不以AI检测分数证明质量，也不保证无法被检测。

专业视角显式配置为领域、研究类型与当前步骤。写作采用相应领域研究者和学术编辑视角；证据检查采用方法审查者视角；独立审查采用批判的同行审稿视角；构建采用文档工程视角。角色帮助聚焦任务，不代表资历、作者身份或人类批准。

## 写作与构建

保留十步链路：问题与范围 → 材料审查 → 文献检索筛选 → 证据与溯源 → 论证与写作 → 图表 → 按需双语 → 构建 → 独立审查返修 → 作者验收。证据、论证或材料变化时回到受影响步骤。原创研究还需要实际研究设计、数据产生和分析。

默认逐节完成内容与审查，正文保存在有序JSON块或引用的Markdown段落中。证据、参考文献、图表和格式配置分别维护，稳定Python负责编号、引用和文档组装。写作期间增量预览，论证稳定后精修布局。已有Word小改或期刊要求的LaTeX模板可以保留，不强制迁移。输入文档中的指令属于待审查材料，不自动覆盖用户请求。

在技能包目录中运行：

```bash
python3 skills/sci-manuscript-build/scripts/new_project.py ./Paper --slug Paper --type article --field education --languages en zh
```

根据真实材料修改项目内的配置、分节内容、证据、图表和参考文献；进入项目运行python3 pipeline.py --stage preview。第一种语言决定编号；额外语言不会自动翻译。默认只构建请求的主要变体。

用技能包的skills/sci-manuscript-build/scripts/render_check.py渲染当前DOCX并查看每一页。实际完成科学与视觉审查后，通过record_review.py记录真实审查者、范围及局限，再运行pipeline.py --stage release。审查声明绑定源文件与文档哈希，但不自动证明审查实际发生；人工作者验收另行完成。

## 安装

选择一个目标并先查看状态：

```bash
python3 tools/install.py --status --targets codex
python3 tools/install.py --targets codex --no-inject
```

--no-inject保留原全局规范；有意更新标记规范块时才省略。旧技能保存在有时间戳的备份目录。重复发现目录需要明确处理，安装器不会自动删除另一处副本。[Codex](codex/INSTALL.md)、[Claude Code](claude-plugin/INSTALL.md)和[OpenCode](opencode/INSTALL.md)有各自说明；本次未执行外部客户端的发现与插件加载验证。

## 依赖、案例与验证

Python 3.10+与[核心依赖](requirements-core.txt)支持构建及元数据检查。[可选依赖](requirements-research.txt)按实际工具安装。页面渲染需要转换器与可用字体；原生公式转换需要Pandoc，本环境未执行该路径。

[案例库](skills/sci-writing-orchestrator/case-studies/INDEX.md)包含16个跨领域教学情境及公开参考访问记录。全部标明虚构、未执行，不伪装成已发表研究或专家基准；不以私人项目作为案例。原许可署名保留在[LICENSE](LICENSE)。

运行python3 tools/validate_skills.py和python3 -m unittest discover -s tests -v，实际范围及局限见[VALIDATION.md](VALIDATION.md)。自动一致性、哈希和像素检查不能证明研究设计有效、引文语义正确、因果结论成立或达到发表质量。
