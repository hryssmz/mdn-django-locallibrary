#!/bin/sh
git_dir=`dirname "$0"`/../.git

rm -rf "${git_dir}/hooks/pre-commit"
ln -s "../../pre-commit.sh" "${git_dir}/hooks/pre-commit"
