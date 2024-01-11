#!/bin/sh
set -x

cd site && python -m http.server 8001
