#!/usr/bin/bash
root_dir=$(cd `dirname $0`; pwd)
cd $root_dir/../

python main.py --port 8080 --workers 1 -v