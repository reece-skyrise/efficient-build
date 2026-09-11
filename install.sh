#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
skill_src="$root/skills/efficient-build"
skill_dst="$HOME/.cursor/skills/efficient-build"
agents_dst="$HOME/.cursor/agents"

mkdir -p "$HOME/.cursor/skills" "$agents_dst"

if [ -e "$skill_dst" ] && [ ! -L "$skill_dst" ]; then
  rm -rf "$skill_dst"
fi
ln -sfn "$skill_src" "$skill_dst"

for f in frontier-architect.md frontier-escalation.md frontier-reviewer.md; do
  dest="$agents_dst/$f"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    rm -f "$dest"
  fi
  ln -sfn "$root/agents/$f" "$dest"
done

echo "Installed:"
echo "  $skill_dst -> $skill_src"
ls -l "$agents_dst"/frontier-architect.md "$agents_dst"/frontier-escalation.md "$agents_dst"/frontier-reviewer.md
