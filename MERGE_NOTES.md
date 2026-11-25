# Current merge: 2.3.1

See [MERGE_2.3.1.md](MERGE_2.3.1.md) for the current selective integration. Earlier notes below retain their historical version scopes.

# Prior merge: 2.2.0

The current 1.3 authoring / 2.1 runtime merge is documented in [MERGE_1.3.0.md](MERGE_1.3.0.md). The notes below describe the historical 2.1 packaging stage before its later GitHub push.

# 2.1.0 合并说明

日期：2026-11-01。此包由用户请求制作，未代替用户推送 GitHub，也未更新真实的全局技能目录。

## 来源与选择

| 来源 | 实际情况 | 本版处理 |
|---|---|---|
| 本机 .agents/skills 六个技能 | 安装标记 1.0.0，较旧；保留部分私人领域案例 | 读取比较，不覆盖；不把私人语料放入公开包 |
| 本机 .codex/skills 六个技能与当前本地源目录 | 安装标记 1.1.0；89 个共享文件与 GitHub main 一致 | 保留通用写作规范及有用的详细流程；不继承旧实现的回归 |
| GitHub b759d8779d731b10f13133830313c4c30629738d | 混合版本；共有文件为 1.1，残留 39 个新增 v2 文件；33 项回归中 14 通过、17 失败、2 报错 | 按功能选择合并；不把 main 整体覆盖为安装版 |
| GitHub 0457e77 历史快照 | Generic v2 核心 33 项行为测试全部通过；隐藏插件清单缺失 | 作为程序/数据契约基线，补齐打包问题 |

上述结论来自下载快照、文件哈希比较和本机执行，不依据仓库旧验证记录推断。参考：[当前快照](https://github.com/FonaTech/Academic_Writing_Skills/tree/b759d8779d731b10f13133830313c4c30629738d)、[v2 基线](https://github.com/FonaTech/Academic_Writing_Skills/tree/0457e77)。

## 保留与补回

- 六个技能与逐领域角色、原始/推导数据证据、声明式分节源、preview/release、双语逐格检查、源/审查哈希、精确图像拼接、16 个教学案例。
- 综述问题与领域进展叙事、研究论文论证结构、量词/条件/口径与算术检查、连贯短句、术语、图注缩写和有依据的展望。
- 十二维审查；外部意见/作者重写按采纳、部分采纳、拒绝分流；仅同步用户请求的长短与语言版本。
- 表格自动年份列与单元格年份；年份来自参考元数据，原始列索引稳定，显式总宽度不增加，缺失有效年份失败。
- 行内标准数学函数正体；未闭合脚标组立即报错。构建前统一检查 Word 锁文件，保留已有输出。
- schematic 自定义 hints、标签白名单和无文字回退；数据面板不进入模型布局输入。
- prose_lint 的 --known、句子断裂/短段落提示与四种 profile 同时工作，保持建议性质。
- 安装备份、重复发现状态提示、统一版本、隐藏插件清单及可见恢复镜像、全文件校验和、CI 配置。

## 明确没有照搬的内容

不把一篇旧私人研究稿当成跨领域默认案例；不把固定篇幅/图数当成期刊规定；不为所有小修改强制建生成器或双语稿；不删除正当的不确定性；不把叙述性综述偏好用于压掉系统综述的筛选方法与数量；不把脚本结果或 AI 自审写成人类专家批准。

用户原有七条写作规范保留在 tools/global_instructions.md，并补充原创/推导数据溯源方式。现有 AGENTS.md 的优先级不变；--no-inject 安装不会改它。

## 升级方式

先核对 VALIDATION.md 与上传说明。旧 Python 项目继续显式选 source.format=python；新项目默认 JSON/Markdown。不要把新模板直接复制覆盖作者正在编辑的项目。归档旧源后迁移，重建并重查所需语言/版本。全局重复安装应另行备份、择一处理，本包不静默删除另一套。

Current 2.3.1 selection and preservation details are in [MERGE_2.3.1.md](MERGE_2.3.1.md). Earlier merge notes retain their historical version scopes.
