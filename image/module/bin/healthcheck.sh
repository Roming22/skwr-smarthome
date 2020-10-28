#!/bin/bash

PROJECT_DIR=$(cd $(dirname $0)/..; pwd)

ps -ef | grep module | grep -q control.py || exit 1
