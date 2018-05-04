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

claferIG = '/Users/markus/Developer/bin/clafer/claferIG'
chocosolver = '/Users/markus/Developer/bin/clafer/chocosolver.jar'
boundanalyzer = '/Users/markus/Developer/Projects/Cardygan/boundanalyzer/build/libs/boundanalyzer-0.0.1.jar'
boundAnalyzerOutput = "/Users/markus/Work/Research/Projects/Paper/2017-08-28_MODELS2018/MODELS18_Repo/eval/jupyter/data/compEfficiency/compEfficiency.json"
runs = 5

def main(arguments):
    specFileDir = '/Users/markus/Developer/Projects/Cardygan/boundanalyzer/src/test/resources/clafer/eval/'
    specs = ['EDM', 'BMM', 'BC', 'PerR', 'TnT', 'TM']
    baseLangSpecFile = '/Users/markus/Work/Research/Projects/Paper/2017-08-28_MODELS2018/MODELS18_Repo/eval/jupyter/data/compEfficiency/tmp.cfr'

    with open('compEffortData.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        header = ['system','alloy','choco','bound']
        writer.writerow(header)

        for spec in specs:
            row = []
            
            specFile = specFileDir + spec + '.cfr'
            # transform to base lang
            subprocess.call(['java','-jar',boundanalyzer,'-b',baseLangSpecFile,'-i',specFile,])

            measureAlloy = []
            measureChoco = []
            measureBound = []
            # run for 5 times and take minimum value
            for run in range(0,runs):
                # due to a specification error for spec EDM_Intro, do not use to base language.
                inputSpec = specFile if spec in ['EDM_Intro','driverPowerWindow'] else baseLangSpecFile
                measureAlloy.append(evalAlloyIG(inputSpec) if spec not in ['driverPowerWindow'] else '*')
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


    # call(["echo 'q' | /Users/markus/Developer/bin/clafer/claferIG", "/Users/markus/Developer/Projects/Cardygan/boundanalyzer/src/test/resources/clafer/eval/EDM_Intro.cfr"])
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    # parser.add_argument('-o', '--outfile', help="Output file",
    #                     default=sys.stdout, type=argparse.FileType('w'))

    # args = parser.parse_args(arguments)

    # print(args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))