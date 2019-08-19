#!/bin/bash

#https://cms-pdmv.cern.ch/mcm/requests?produce=%2FGluGluToHHTo2B2G_node_SM_TuneCP5_PSWeights_13TeV-madgraph-pythia8%2FRunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1%2FNANOAODSIM&page=0&shown=127
#https://cms-pdmv.cern.ch/mcm/requests?dataset_name=GluGluToHHTo2B2G_node_SM_TuneCP5_PSWeights_13TeV-madgraph-pythia8&page=0&shown=127
#https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIFall18wmLHEGS-00732

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_6/src ] ; then 
 echo release CMSSW_10_2_6 already exists
else
scram p CMSSW CMSSW_10_2_6
fi
cd CMSSW_10_2_6/src
eval `scram runtime -sh`

curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIIFall18wmLHEGS-00732 --retry 2 --create-dirs -o Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-00732-fragment.py 
[ -s Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-00732-fragment.py ] || exit $?;

scram b
cd ../../
seed=$(date +%s)
cmsDriver.py Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-00732-fragment.py --fileout file:HIG-RunIIFall18wmLHEGS-00732.root --mc --eventcontent RAWSIM,LHE --datatier GEN-SIM,LHE --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename HIG-RunIIFall18wmLHEGS-00732_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${seed}%100)" -n 884 || exit $? ; 

