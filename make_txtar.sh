#!/usr/bin/env bash

rm -rf /tmp/minortop
rm -f /tmp/minortop.tar
rm -f /tmp/filelist.txt

rm -f pytest.log
pytest >pytest.log 2>&1
rg --no-ignore --files . |
    grep -iE 'test_skeleton.py|src|pytest.log|setup.cfg' |
    grep -viE '__init__.py' |
    grep -viE '__pycache' |
    grep -vF .egg |
    tee /tmp/filelist.txt

tar -cf /tmp/minortop.tar -T /tmp/filelist.txt
mkdir -p /tmp/minortop
tar xf /tmp/minortop.tar -C /tmp/minortop
rg --files /tmp/minortop
txtar-c /tmp/minortop | pbcopy
