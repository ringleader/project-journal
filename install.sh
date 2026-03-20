#!/usr/bin/env bash
# project-journal install script
# Installs /log, /brief, and /orient skills for Claude Code + gstack
# Usage: bash install.sh

set -e

SKILLS_DIR=""

# Detect gstack install location
if [ -d "$HOME/.claude/skills/gstack" ]; then
  SKILLS_DIR="$HOME/.claude/skills/gstack"
elif [ -d ".claude/skills/gstack" ]; then
  SKILLS_DIR=".claude/skills/gstack"
else
  echo "❌  gstack not found."
  echo ""
  echo "project-journal requires Claude Code + gstack."
  echo "Install gstack first: https://github.com/garrytan/gstack"
  exit 1
fi

echo "Installing project-journal skills to $SKILLS_DIR..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for skill in log brief orient; do
  src="$SCRIPT_DIR/skills/$skill/SKILL.md"
  dest="$SKILLS_DIR/$skill"

  if [ ! -f "$src" ]; then
    echo "⚠️  Missing $src — skipping $skill"
    continue
  fi

  mkdir -p "$dest"
  cp "$src" "$dest/SKILL.md"
  echo "✓  /$(basename $dest)"
done

echo ""
echo "✅  Installed. Restart Claude Code if it's running, then:"
echo ""
echo "   /log decision \"Your first load-bearing decision\""
echo "   /brief"
echo "   /orient"
echo ""
echo "Add /log entries any time during a session."
echo "Run /brief at the end of a session to synthesize."
echo "Run /orient at the start of any new session to reload context."
