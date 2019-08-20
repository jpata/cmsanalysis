#!/bin/bash

set -e

export WORKDIR=`pwd`

env

cd /afs/cern.ch/user/j/jpata/work/nano/CMSSW_10_2_15
eval `scram runtime -sh`
cd $TMPDIR

cp $WORKDIR/inputs.txt ./

export FILE=`sed "${NUMJOB}q;d" inputs.txt`
cmsRun /afs/cern.ch/user/j/jpata/work/nano/CMSSW_10_2_15/myNanoProdMc2016_NANO.py $FILE
cp out.root /afs/cern.ch/user/j/jpata/work/nano/out.root
