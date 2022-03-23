#!/usr/bin/env bash
yq -r '"\(.package.name),\(.affects.ranges[].repo)"' "$1"/**/*.yaml
