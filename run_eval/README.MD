# Reproduce Results
This directory contains the scripts to reproduce results from the experiments.

## RQ1: Effectiveness
The script `effectiveness.py` produces effectiveness measurements for RQ1.

## RQ2: Efficiency
The script `compEffortEval.py` produces runtime measurements for Alloy, Chocosolver, and Boundanalyzer.

To run the script update the paths in the header according to you local setup:
```
claferIG = '<SET_PATH_TO_CLAFER_INSTALLATION>/clafer/claferIG'
chocosolver = '<SET_PATH_TO_CLAFER_INSTALLATION>/clafer/chocosolver.jar'
```