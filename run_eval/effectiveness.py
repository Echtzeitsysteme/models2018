#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import subprocess
import json
from pprint import pprint
from timeit import default_timer as timer
import csv

boundanalyzer = os.path.abspath('../tool/boundanalyzer-0.0.1.jar')


def main(arguments):
    specFileDir = os.path.abspath('../subj_systems')
    specs = ['EDM', 'BMM', 'BC', 'PerR', 'TnT', 'TM']
    for spec in specs:
        specFile = os.path.join(specFileDir, spec + '.cfr')
        evalBoundanalyzer(specFile,spec)


def evalBoundanalyzer(specFile, specName):
    FNULL = open(os.devnull, 'w')
    start = timer()
    output = os.path.join('../eval/raw/', specName + '.json')
    subprocess.call(['java','-jar',boundanalyzer,'-k','BOUND','-t','ALL','-c','ALL','-i',specFile,'-o',output])


if __name__ == '__main__':
    sys.exit(main(sys.argv[0:]))