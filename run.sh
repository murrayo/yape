#!/bin/bash

cd /
./extract_pButtons.py -o /data /data/$1
./graph_pButtons.py -o /data/charts /data
