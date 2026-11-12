#!/bin/sh
set -eu

set -- "$@" ':(icase,glob)**/prompt.md' ':(icase,glob)**/prompt.txt'
case "$#" in
    2)
        matches=$(git ls-files -- "$1" "$2")
        ;;
    3)
        matches=$(git log --full-history -1 --format=%H "$1" -- "$2" "$3")
        ;;
    *)
        echo "Usage: $0 [commit]" >&2
        exit 2
        ;;
esac

if [ -n "$matches" ]; then
    printf '%s\n' 'Private prompt files are forbidden in Git.' "$matches" >&2
    exit 1
fi
