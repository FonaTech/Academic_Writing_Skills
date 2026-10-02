# OpenCode target

The installer provides an opencode target and Claude-compatible discovery options. Inspect python3 tools/install.py --status --targets opencode and the installed client's actual discovery settings before installation. Use one discovery location to avoid duplicated skill names.

python3 tools/install.py --targets opencode --no-inject installs skills without changing standing instructions. Omit --no-inject to update the marked instruction block. Existing destination skills are preserved in timestamped backups. External-client discovery and plugin behavior were not executed in this validation environment.
