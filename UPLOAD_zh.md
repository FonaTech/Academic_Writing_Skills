# 上传与安装 2.3.1

此目录是完整仓库内容，不是只包含六个 SKILL.md 的简包。上传时应保留 skills、tools、tests、validation、三个客户端说明、VERSION、校验和，以及隐藏的 .claude-plugin、.github 和 .gitignore。

## 推荐上传方式

1. 解压 Academic_Writing_Skills_v2.3.1.zip。
2. 将版本目录中的内容放到 GitHub 仓库工作区的根目录，不要再嵌套一层 Academic_Writing_Skills_v2.3.1。
3. 保留自己仍需使用的私人 provenance/；它未包含在公开技能包中。对正在编辑的同名文件先归档。
4. 运行下面的验证命令，再通过 GitHub Desktop 或 git 提交和推送。此包没有替你上传。

```bash
python3 tools/sync_plugin_manifests.py
python3 tools/validate_skills.py
python3 -m unittest discover -s tests -v
python3 tools/checksums.py
```

采用网页拖拽时，确认隐藏目录也进入仓库；仅上传可见文件会漏掉标准插件入口。可见 claude-plugin/plugin.json 与 marketplace.json 为镜像，漏传后在仓库工作区执行 python3 tools/sync_plugin_manifests.py --write，再把生成的 .claude-plugin 加入提交。

如果使用随包交付的 Git 补丁：在基于 086d3a5cc8d1a002a1f0dcb8df4d193b8423eb1f 的干净克隆中，先执行 git apply --check PATCH，再执行 git apply --binary PATCH。补丁包含隐藏文件；有本地修改时应先比较并保留，不强行覆盖。

GitHub Actions 配置在推送/PR 后检查两个 Python 版本的结构、行为与校验和。此处只提供配置；首次托管运行结果以 GitHub 实际记录为准。

## 安装到本机

先运行 python3 tools/install.py --status --targets codex。确认选择的发现目录后执行 python3 tools/install.py --targets codex --no-inject。省略 --no-inject 会更新标记规范块；旧技能先移入时间戳备份目录。

如果 .agents/skills 与 .codex/skills 都存在同名六个技能，状态命令会提示。自行保留一套活动副本，另一套移出技能发现路径并保留归档；安装器不会擅自清理。Claude Code/OpenCode 可分别选择 --targets claude / opencode。安装后新开会话检查。

有意编辑发布内容后重新运行验证，再用 python3 tools/checksums.py --write 更新清单。不要直接修改 SHA256SUMS 来掩盖未验证的源码变化。

此包合入 1.3.0 写作链，保留 2.1 构建与证据能力。本机 .codex 中的 1.3.0 已与输入包一致；本次不会自动安装或修改全局目录。
