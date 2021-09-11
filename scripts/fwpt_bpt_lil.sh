#!/bin/bash

gsed -i \
    -e 's/FWPT/LIL/g' \
    -e 's/BTX/BPT/g' \
    season*/*.json
