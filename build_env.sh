#!/bin/bash
set -e

if [ -d .venv ]; then
    rm -r .venv
fi
python3.6 -m venv .venv
source .venv/bin/activate
pip install -U pip==9.0.1
pip install numpy==1.10.4
pip install scipy==0.16.0
pip install  -r requirements.txt

echo "Use \"source .venv/bin/activate\" to enter virtual environment"
