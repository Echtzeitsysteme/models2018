# Boundanalyzer

## Required third-party software
Following dependencies must be installed:
* MILP Solver - IBM CPLEX (at least in Version 12.7.1) freely available as academic edition 
* Clafer Compiler (at least in Verion 4.3) see: https://github.com/gsdlab/clafer

## Setup 

* To setup the CPLEX solver the environment variable `CPLEX_LIB_PATH` must be set. For example for setting the environment execute following command from the command line:

`export CPLEX_LIB_PATH=/Users/user1/Applications/IBM/ILOG/CPLEX_Studio1263/cplex/bin/x86-64_osx/`

* To setup the Clafer compiler the environment variable `CLAFER_COMPILER_PATH`must be set. The path must point to the Clafer compiler executable. For example for setting the environment execute following command from the command line:

`export CLAFER_COMPILER_PATH=/Users/user1/Applications/Clafer/clafer`

## Usage
To run *Boundanalyzer* execute following command from the command line to retrieve available command line options:

`java -jar boundanalyzer-0.1.1.jar -h`

**Output:**
```
usage: boundanalyzer
 -b,--base <arg>      Transform to base language and output to file.
 -c,--clafer <arg>    path to clafer to be analyzed or ALL for all clafers
 -f,--flatten <arg>   Perform flattening and output to file.
 -i,--input <arg>     input Clafer file path
 -k,--kind <arg>      kind of analysis; either BOUND or SCOPE
 -o,--output <arg>    output CSV file for statistics
 -t,--target <arg>    target of analysis, available options: REF, GMULT,
                      CMULT or ALL
```
