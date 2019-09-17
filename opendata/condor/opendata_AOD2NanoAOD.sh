#!/bin/bash
set -e
env

ls -al

NUMJOB=$1
#make the variable 1-based
NUMJOB=$((NUMJOB + 1))

INFILE=Summer12_DR53X_DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph.txt
mv $INFILE input.txt
export FILE=`sed "${NUMJOB}q;d" input.txt`

export WORKDIR=`pwd`

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd /storage/user/jpata/cmsanalysis/opendata/condor/CMSSW_5_3_32
eval `scram runtime -sh`
cd $WORKDIR

cmsRun /storage/user/jpata/cmsanalysis/opendata/condor/CMSSW_5_3_32/src/workspace/AOD2NanoAOD/configs/simulation_cfg.py $FILE
cp output.root /storage/user/jpata/cmsanalysis/opendata/`basename $FILE`
