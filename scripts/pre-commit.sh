#!/bin/sh
clear && \
    coverage run && \
    coverage report --fail-under=100 && \
    black --check . && \
    flake8 --quiet . && \
    isort --check . && \
    mypy .
