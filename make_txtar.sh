#!/usr/bin/env bash

rm -rf /tmp/minortop
rm -f /tmp/minortop.tar
rm -f /tmp/filelist.txt

rm -f pytest.log
pytest >pytest.log 2>&1
rg --no-ignore --files . |
    grep -iE 'test_skeleton.py|src|pytest.log|setup.cfg' |
    grep -vF .code-workspace |
    grep -viE '__pycache' |
    grep -vF .egg |
    grep -vF soundex.py |
    grep -vF portflower.py |
    grep -vF cropera |
    grep -vF bootfamily.py |
    grep -vF britishcouch.py |
    grep -vF reasonlabel.py |
    grep -vF steadyforever |
    grep -vF refuseapprove.py |
    grep -vF chat_recipe.txt |
    grep -vF chat_instructions.txt |
    grep -vF template.tmpl |
    grep -vF steadyforever.code-workspace |
    grep -vF template.j2 |
    grep -vF requirements.txt |
    grep -vF pytest.log |
    tee /tmp/filelist.txt

tar -cf /tmp/minortop.tar -T /tmp/filelist.txt
mkdir -p /tmp/minortop
tar xf /tmp/minortop.tar -C /tmp/minortop
rg --files /tmp/minortop
txtar-c /tmp/minortop | pbcopy
