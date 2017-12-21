#!/bin/bash

version=$(python --version 2>&1)

if [ "${version/Python 3.3}" != "$version" ]; then
    exit 0
fi

tox
r=$?

if [ $r -ne 0 ]; then
    echo "Tox failed."
    exit $r
fi

tox -e check
r=$?

if [ $r -ne 0 ]; then
    echo "Tox check failed."
    exit $r
fi
