# 2.3.1 验证记录

日期：2026-11-25。基线为 GitHub 2.2.0 提交 4c374565d29f8143d63f0da9336fb15aeec76633。本版选择合入原始 2.3.0 的校验与目录组织改进，保留 2.2 规则、代码与回归修复。

| 检查 | 本次实际结果 |
|---|---|
| Python 3.10 回归 | 68 项通过，0 失败、0 报错、0 跳过 |
| Python 3.12 回归 | 65 项通过，3 项因缺少可选 PDF/文献依赖跳过，0 失败、0 报错 |
| 六个技能结构/链接/共享副本/写作链 | 0 errors、0 warnings |
| 官方 skill-creator quick_validate | 六个全部通过 |
| Claude 插件清单校验 | 通过，可选市场图标提示不影响结果 |
| 临时安装与再次安装 | 六个安装成功，旧六套均备份，版本 2.3.1；未注入真实全局规范 |
| 方法案例迁移 | 16 个正文文件与 2.2 逐字节相同，内部链接有效，旧索引保留跳转 |
| 2.2 runtime/配置保留 | 所有技能 Python/资产配置及安装/哈希工具逐文件核对；除新项目版本常量外保持原字节 |

新增 9 项测试包含每个 profile 的英文/中文坏正则、默认表的坏中文模式、缺失/空值/错误类型的 rhythm 与 zh 块、案例仅出现名称但没有链接、无效编号链接、缺少索引、移除 checker 实际调用，以及真实 CLI 对无效 profile 的非零退出。原有 59 项回归继续覆盖短问句、连接词实际次数、Figure 引用开头的正文、完整规则表、证据/构建/备份等。

日志和机器结果在 validation/logs 与 validation/test_results.json。Python 3.12 的新增校验测试需要 PyYAML；首次运行发现工作区 runtime 缺少该核心依赖，随后在隔离 venv 内补齐并复测，没有修改全局 Python。测试中的 missing.docx/no converter 是受控负例，不是本次交付渲染失败。

## 范围与未执行项

本次没有全局安装，没有新建交付 DOCX/PDF，没有执行新的视觉审查、商业 AI 检测器、线上检索/Crossref/PDF 全链路、Pandoc 展示公式转换或独立领域专家审查。32 个方法/领域案例仍是教学材料，不作为真实研究或专家质量验证。历史 2.1 与 2.2 的审查/测试分别保留于 validation/history，不能作为本次独立审查。

风格诊断需语义审查，不能证明作者身份、科学有效性或保证投稿/检测结果。GitHub 托管 CI 的结果以本次推送后对应提交的实际运行记录为准。

复现：python3 tools/validate_skills.py；python3 -m unittest discover -s tests -v；python3 tools/sync_plugin_manifests.py；python3 tools/checksums.py。
