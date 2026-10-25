# Claude Code

## Recommended: user skills
```bash
python3 tools/install.py --targets claude
```
Copies the six skills to `~/.claude/skills/` and adds the instruction block to `~/.claude/CLAUDE.md`. Restart Claude Code or start a new session; the skills appear in the skill list and are invoked automatically when a task matches their description.

## As a plugin
The repository root is a valid plugin marketplace (`claude plugin validate .`):
```bash
claude plugin marketplace add "/path/to/Academic_Writing_Skills"
claude plugin install academic-writing-skills@academic-writing-skills
```
Use either the user-skill install or the plugin, not both, to avoid duplicate skill names.

## Project-local
```bash
python3 tools/install.py --targets claude --project /path/to/paper --no-inject
```
creates `/path/to/paper/.claude/skills/` (and `.agents/skills/` when Codex is targeted) for a repository that should carry its own copy. Use it instead of, not in addition to, the user-level install; both would make each skill appear twice.
