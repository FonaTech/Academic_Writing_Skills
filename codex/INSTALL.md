# Codex CLI

```bash
python3 tools/install.py --targets codex
```
Copies the skills to `$CODEX_HOME/skills` (default `~/.codex/skills`) and adds the instruction block to `~/.codex/AGENTS.md`. Each skill ships `agents/openai.yaml` with a display name, a short description and a default prompt (`$sci-writing-orchestrator`, …). Start a new Codex session; invoke explicitly with `$skill-name` or let Codex match the description.

Codex 0.159 also reads `~/.agents/skills`. Do not install there as well (`--targets agents` together with `codex` is refused), or every skill appears twice. Use `--targets agents` only for other Agent-Skills tools, without `codex`.
