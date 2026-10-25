# OpenCode

OpenCode (1.1.x) loads skills from `~/.config/opencode/{skill,skills}/**/SKILL.md` and, unless `OPENCODE_DISABLE_CLAUDE_CODE` or `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` is set, also from `~/.claude/skills/**/SKILL.md`. For global rules it reads `~/.config/opencode/AGENTS.md` if present, otherwise `~/.claude/CLAUDE.md`.

```bash
python3 tools/install.py --targets claude opencode
```
installs once into `~/.claude/skills` (seen by both tools) and injects the block into `~/.claude/CLAUDE.md`. If `~/.config/opencode/AGENTS.md` exists, the block is added there too, because that file takes precedence. With Claude compatibility disabled, the installer copies the skills to `~/.config/opencode/skills` instead.

Check: `opencode debug skill` lists the six skills.
