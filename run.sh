#!/bin/bash

clear_env() {
    for ldir in "dist" "mdconv.egg-info" ".venv" "mdconv/__pycache__" "mdlang/__pycache__" "pychar/__pycache__"
    do
        rm -rf $ldir
    done
}

case "$1" in
"")
# ERROR
    echo "$1 arg need: setenv, pypipub, gitpush"
    exit 1
    ;;
"clear")
    clear_env
    ;;
"setenv")
    clear_env
    uv venv
    source .venv/bin/activate
    uv sync
    ;;
"pypipub")
    clear_env
    if [ "$PYPI_TOKEN" == "" ]; then
        echo "env: 'PYPI_TOKEN' not found"
        exit 1
    fi
    uv build
    uv publish --token $PYPI_TOKEN
    ;;
"gitpush")
    git add .
    git commit -m "push in $(date)"
    git push
    ;;
esac