#!/bin/sh
set -e

export NUMJOB=$1

#get the N-th row
head -n$((NUMJOB+1)) inputs.txt | tail -1 > files_to_process.txt

#get the first word in the row
OUTLFN=`awk '{print $1;}' < files_to_process.txt`

source /cvmfs/cms.cern.ch/cmsset_default.sh
cp $X509_USER_PROXY /tmp/x509_up`id -u`
export SCRAM_ARCH=slc6_amd64_gcc700

#setup the environment
scramv1 project CMSSW CMSSW_10_2_18
cd CMSSW_10_2_18
eval `scramv1 runtime -sh`
cd ..

cmsRun -e -j fjr.xml myConf.py $NUMJOB

eval `scram unsetenv -sh`

## Stageout
#mkdir -p `dirname $OUTLFN`
#cp myNanoProdMc2018_NANO.root $OUTLFN 

gfal-copy myNanoProdMc2018_NANO.root gsiftp://transfer.ultralight.org/$OUTLFN
