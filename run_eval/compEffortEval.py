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

# UPDATE FOLLOWING PATHS ACCORDING TO YOUR LOCAL SETUP
claferIG = '<SET_PATH_TO_CLAFER_INSTALLATION>/clafer/claferIG'
chocosolver = '<SET_PATH_TO_CLAFER_INSTALLATION>/clafer/chocosolver.jar'
#-----------------------------------------------------------------
#-----------------------------------------------------------------

boundanalyzer = os.path.abspath('../tool/boundanalyzer-0.0.1.jar')
boundAnalyzerOutput = os.path.abspath("../eval/raw/compEfficiency/compEfficiency.json")
runs = 5

def main(arguments):
    specFileDir = os.path.abspath('../subj_systems')
    specs = ['EDM', 'BMM', 'BC', 'PerR', 'TnT', 'TM']
    baseLangSpecFile = os.path.abspath('../eval/raw/compEfficiency/tmp.cfr')

    with open('../eval/compEffortData.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        header = ['system','alloy','choco','bound']
        writer.writerow(header)

        for spec in specs:
            row = []
            
            specFile = os.path.join(specFileDir, spec + '.cfr')
            # transform to base lang
            subprocess.call(['java','-jar',boundanalyzer,'-b',baseLangSpecFile,'-i',specFile,])

            measureAlloy = []
            measureChoco = []
            measureBound = []
            # run for 5 times and take minimum value
            for run in range(0,runs):
                # due to a specification error for spec EDM, do not use to base language.
                inputSpec = specFile if spec in ['EDM','BC'] else baseLangSpecFile
                measureAlloy.append(evalAlloyIG(inputSpec) if spec not in ['BC'] else '*')
                measureChoco.append(evalChocosolver(inputSpec))
                measureBound.append(evalBoundanalyzer(inputSpec))
            row.append(spec)
            row.append(round(min(measureAlloy),3) if isinstance(min(measureAlloy), float) else min(measureAlloy))
            row.append(round(min(measureChoco),4))
            row.append(round(min(measureBound),4))
            writer.writerow(row)


def evalAlloyIG(specFile):
    FNULL = open(os.devnull, 'w')
    start = timer()
    ps = subprocess.Popen(('echo', 'q'), stdout=subprocess.PIPE)
    output = subprocess.call([claferIG, specFile], stdin=ps.stdout)
    ps.wait()
    end = timer()
    return end - start

def evalChocosolver(specFile):
    FNULL = open(os.devnull, 'w')
    start = timer()
    subprocess.call(['java','-Xmx3g', '-jar',chocosolver, '--maxint=10000','-n','1','--noprint','--file',specFile])
    end = timer()
    return end - start

def evalBoundanalyzer(specFile):
    FNULL = open(os.devnull, 'w')
    start = timer()
    subprocess.call(['java','-jar',boundanalyzer,'-k','SCOPE','-t','CMULT','-c','ROOT','-i',specFile,'-o',boundAnalyzerOutput])
    end = timer()
    jsonSpec = json.load(open(boundAnalyzerOutput))
    # We only consider lower scope check, so remove redundant time for upper scope check from measurement
    timeUpperBound = jsonSpec['analysisResults'][0]['ubIlpRes']['statistics']['duration']
    return (end - start) - timeUpperBound/1000


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))