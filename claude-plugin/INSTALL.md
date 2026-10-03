# Claude Code target

Inspect python3 tools/install.py --status --targets claude. To copy only the six skills, run python3 tools/install.py --targets claude --no-inject. Omit --no-inject when intentionally updating the marked standing instructions. The script targets ~/.claude/skills/ and, when requested, ~/.claude/CLAUDE.md; existing destination skills are preserved in timestamped backups.

For a project-local copy use python3 tools/install.py --targets claude --project /path/to/paper --no-inject. Choose one discovery location rather than keeping duplicate skill names. A .claude-plugin marketplace/manifest is included as an optional distribution format; JSON structure was checked, but actual client loading, discovery precedence and plugin CLI behavior were not executed here. Follow the installed client's current documentation and verify its discovered skill list.
