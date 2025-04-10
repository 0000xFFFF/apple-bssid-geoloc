#!/bin/bash
cat bssids.txt | xargs -I {} abgl "{}" | tee abgl_output.csv
