#!/bin/sh

if [ -z `python --version 2>&1 | grep 2.6` ]; then
    flake8
fi
