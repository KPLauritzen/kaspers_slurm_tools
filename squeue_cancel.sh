#!/bin/bash

grep -E -e '^[0-9]+' -o < /dev/stdin | xargs scancel
