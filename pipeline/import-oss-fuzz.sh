#!/usr/bin/env bash
if [ $# -ne 1 ]; then
	echo "usage: $0 /path/to/oss/fuzz/vulns"
	exit 2
fi

./scripts/oss-fuzz-srcs.sh "$1" | sort -u > meta/oss-fuzz-srcs.csv
parallel -j1 --bar --result logs/add-remote-oss-fuzz --colsep ',' './scripts/add-remote.py oss-fuzz {1} {2}' < meta/oss-fuzz-srcs.csv
