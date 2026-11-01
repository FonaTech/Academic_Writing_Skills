# Claude Code

Run from the package root:

```bash
python3 tools/install.py --status --targets claude
python3 tools/install.py --targets claude --no-inject
```

Omit --no-inject only to update the marked standing instructions. Existing destination skills are preserved in timestamped backups. Use --project DIR --no-inject for a project-local copy; avoid simultaneously discovering the same skill from multiple locations.

The canonical plugin manifests are .claude-plugin/plugin.json and marketplace.json. Visible claude-plugin/*.json files mirror them for browser-upload recovery; tools/sync_plugin_manifests.py --write restores the hidden copies. The installed local Claude CLI validated this release's manifests. Actual plugin installation/account discovery was not performed.

For a client supporting marketplace installation:

```text
/plugin install academic-writing-skills --marketplace FonaTech/Academic_Writing_Skills
```

Start a new session and inspect the discovered skill list. Do not install both the plugin and file copies unless the client's discovery setup intentionally separates them.
