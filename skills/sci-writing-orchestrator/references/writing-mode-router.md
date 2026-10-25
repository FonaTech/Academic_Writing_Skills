# Writing mode router

Pick one primary mode from the request, then load only the references for that mode. Secondary modes (for example a rebuttal that also needs new figures) add their skill's references when that part of the work starts.

| Signal in the request | Mode | Preset | Load first |
|---|---|---|---|
| 综述, review, perspective, tutorial review, roadmap, book chapter | `review` | presets/review.json or perspective.json | review-architecture.md |
| 研究论文, article, letter, communication, 投稿 | `article` | presets/article-nature.json or letter.json | article-architecture.md |
| conference paper, proceedings, 会议论文 | `article` | presets/conference-paper.json | article-architecture.md |
| 润色, polish, rewrite, 去AI味, 去叠甲, shorten sentences, 统一术语 | `revision` | none | sci-prose-style SKILL.md |
| 外部评审意见, external or co-author review of a draft, author's own rewrite to compare | `revision` | none | sci-manuscript-review references/rebuttal-letters.md (triage), sci-prose-style SKILL.md |
| 25%/50%/100% 版本, shorter or longer variant, sync variants | `revision` | none | review-architecture.md, section 8; sci-prose-style bilingual-consistency.md |
| 审稿意见, response to reviewers, rebuttal, 修改说明 | `rebuttal` | presets/rebuttal.json | sci-manuscript-review references/rebuttal-letters.md |
| cover letter, 投稿信, highlights, TOC text | `revision` | none | sci-manuscript-review references/rebuttal-letters.md, sci-prose-style titles-abstracts.md |
| 基金, proposal, NSFC, RGC GRF, fellowship | `proposal` | presets/proposal-nsfc.json or proposal-rgc.json | proposal-and-thesis.md |
| 学位论文, thesis, dissertation chapter | `thesis` | presets/thesis-chapter.json | proposal-and-thesis.md |
| meeting recording, 组会录音, supervisor comments | intake for any mode | none | meeting-to-decisions.md |
| figures only, Nano Banana, 示意图, 数据图 | figure task | none | sci-figure-design SKILL.md |
| check references, 核查数据, citation audit | audit task | none | sci-literature-evidence citation-audit.md |
| pre-submission check, 模拟审稿 | review task | none | sci-manuscript-review SKILL.md |

## Depth
Ask once when unclear, otherwise infer:

| Depth | What changes | Typical request |
|---|---|---|
| light polish | wording only; structure and claims untouched | "润色一下这一段" |
| deep revision | sentence and paragraph rewrite, terminology, captions; claims checked | "深度优化英文稿" |
| structural revision | sections merged, split or added; figures replanned; evidence extended | "应用部分要大幅扩充" |
| rebuild | new generator, full evidence base, all figures and both languages | "重构整篇手稿" |

## Mode-specific success criteria

| Mode | Done when |
|---|---|
| review | reads as the field's progress; every section argues one point with sourced comparisons; applications state property → function → evidence → next decisive result; subsection endings synthesise and bridge; outlook gives measurable targets |
| article | each Results subsection has a noun-phrase heading that names what it shows, and one main figure; claims match the data; methods reproducible; limitations stated |
| revision | meaning preserved, facts and quantifiers checked, lint clean, no defensive sentences, terminology unified, both languages and every length variant aligned; triage table for any outside review |
| rebuttal | every comment answered, every promised change present, tone direct and courteous |
| proposal | aims, significance, feasibility and deliverables consistent; preliminary data sourced; risks with alternatives |
| thesis | chapters connect through stated questions; each chapter reusable as a paper; no duplicated literature review |
