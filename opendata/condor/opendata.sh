#!/bin/bash
set -e

NUMJOB=$1

export FILE=`sed "${NUMJOB}q;d" inputs2.txt`

export WORKDIR=`pwd`

env

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd /storage/user/jpata/cmsanalysis/opendata/condor/CMSSW_10_2_15
eval `scram runtime -sh`
cd $WORKDIR

cmsRun /storage/user/jpata/cmsanalysis/opendata/condor/CMSSW_10_2_15/myNanoProdMc_NANO.py $FILE
cp out.root /storage/user/jpata/cmsanalysis/opendata/`basename $FILE`
