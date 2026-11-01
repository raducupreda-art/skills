#!/bin/sh
# Rebuild this repo from upstream main, keeping .github and .radu, then unlock the listed skills.
set -eu
git fetch --depth=1 https://github.com/mattpocock/skills.git main
find . -mindepth 1 -maxdepth 1 ! -name .git ! -name .github ! -name .radu -exec rm -rf {} +
git archive FETCH_HEAD | tar -x --exclude=.github
python3 .radu/unlock.py skills
