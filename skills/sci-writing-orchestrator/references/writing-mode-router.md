# Writing mode router

Pick one primary mode from the request, then load only the references for that mode. Secondary modes (for example a rebuttal that also needs new figures) add their skill's references when that part of the work starts.

In every mode, each paragraph that is drafted or rewritten follows sci-prose-style references/human-line-of-thought.md. Its section 4 gives the chain of reasoning for each genre and section type, and its checklist is part of done.

| Signal in the request | Mode | Preset | Load first |
|---|---|---|---|
| 综述, review, perspective, tutorial review, roadmap, book chapter | `review` | presets/review.json or perspective.json | review-architecture.md |
| 研究论文, article, letter, communication, 投稿 | `article` | presets/article-nature.json or letter.json | article-architecture.md |
| conference paper, proceedings, 会议论文 | `article` | presets/conference-paper.json | article-architecture.md |
| 润色, polish, rewrite, 去AI味, 去叠甲, shorten sentences, 统一术语 | `revision` | none | sci-prose-style SKILL.md |
| 降AI率, AIGC 检测报告, AI-detector report, flagged paragraphs | `revision` | none | sci-manuscript-review references/ai-detector-reports.md, sci-prose-style references/human-line-of-thought.md |
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
| every mode | each drafted or rewritten paragraph passes the human-line-of-thought checklist; prose_lint shows no `number-run`, `question-voice`, `thinking-aloud` or `zh-template` hits and explanation connectives near 8 per 100 sentences or fewer |
| review | reads as the field's progress; every section argues one point with sourced comparisons; applications state property → function → evidence → next decisive result; subsection endings synthesise and bridge; outlook gives measurable targets |
| article | each Results subsection has a noun-phrase heading that names what it shows, and one main figure; claims match the data; methods reproducible; limitations stated |
| revision | meaning preserved, facts and quantifiers checked, lint clean, no defensive sentences, terminology unified, both languages and every length variant aligned; triage table for any outside review |
| rebuttal | every comment answered, every promised change present, tone direct and courteous |
| proposal | aims, significance, feasibility and deliverables consistent; preliminary data sourced; risks with alternatives |
| thesis | chapters connect through stated questions; each chapter reusable as a paper; no duplicated literature review |


## Preserved runtime and scope safeguards

# Mode selection

| Mode | Scientific dependency | Structure choice |
|---|---|---|
| Narrative review/perspective | Transparent scope, balanced selected evidence and interpretive contribution | Organize by questions, mechanisms, chronology, methods, debates or applications when each fits the question |
| Systematic review | Protocol, reproducible search/selection, bias/quality appraisal and defensible synthesis | Use the field's reporting standard; PRISMA is a reporting framework, not the research method |
| Scoping review | Clear mapping question, eligibility, transparent selection and charting | Map evidence/gaps; use applicable PRISMA-ScR guidance; do not imply pooled causal certainty |
| Original research | Raw data, actual design, analysis, controls, uncertainty and reproducibility | Use the venue's structure; results follow the actual design, evidence and question |
| Revision/polish | Existing authoritative source and requested depth | Use bounded prose/structure passes; do not mandate new searches or a generator |
| Proposal | Literature, real preliminary results, feasible aims and risks | Clearly label planned analyses and projected outcomes |
| Thesis | Chapter contribution and relationship to the whole thesis | Respect institutional template and authored chapters |
| Rebuttal | Exact reviewer comments and real changes | Answer point by point, with verified locations |

Optional venue/field presets suggest structures; they do not prescribe word/figure counts unless verified venue instructions require them.


All paragraph drafting follows [human-line-of-thought.md](../../sci-prose-style/references/human-line-of-thought.md). Named venue/agency structures are optional scaffolds until checked against the actual current instructions; scientific content is never invented to complete a template. Method-case numbers refer to case-studies/methods/; default generic presets and the separate domain cases are retained.
