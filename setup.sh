#!/bin/bash

HERE=$(dirname "$(readlink --canonicalize "${BASH_SOURCE[0]}")")

die() {
  echo "$@" >&2
  exit 1
}

echo "Clone BugsInPy repository"
git clone https://github.com/soarsmu/BugsInPy "$HERE/Analysis/BugsInPy" || die 'Unable to clone BugsInPy'

cp -f "$HERE/SBFL/bugsinpy-faultloc" "$HERE/Analysis/BugsInPy/framework/bin"
echo "Add path to bashrc"
echo 'export PATH="$PATH:$HERE/Analysis/BugsInPy/framework/bin"' >> ~/.bashrc

echo 'Please run `source ~/.bashrc` to apply the changes in the environment' >&2
mv -f "$HERE/Analysis/get_bug-fixes.py" "$HERE/Analysis/BugsInPy/projects"
