# Codex installation

Inspect tools/install.py --status --targets codex. To install only the skills, run python3 tools/install.py --targets codex --no-inject. To also update the marked standing instructions, omit --no-inject. The installer uses CODEX_HOME/skills (default ~/.codex/skills); project-local installation uses --project DIR --no-inject and .agents/skills.

Use one skill-discovery directory per installation. If both ~/.agents/skills and ~/.codex/skills contain the same six names, inspect and resolve the duplicate deliberately; this installer does not delete another discovery directory. Existing destination skills are saved under timestamped .academic-writing-backups folders. Start a new session after installation. Exact discovery behavior depends on the host/client configuration.
