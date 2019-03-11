#!/bin/bash
set -e
set -v

#get the
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTopic#Running_a_user_script_with_CRAB
#To be precise, CRAB job wrapper will execute scriptExe jobId <scriptArgs> where scripExe is the name passed in CRAB configuration, jobId is the number of this job in the task, and <scriptArgs> indicate optional additional arguments which can be specified in CRAB configuration file via the JobType.scriptArgs parameter
job_id=$1
process_name="BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-"

N_evts=`python -c "import PSet; print PSet.process.maxEvents.input.value()"`
#N_seed=`python -c "import PSet; print PSet.process.source.firstEvent.value()"`
N_seed=$job_id


initial_dir=`pwd`
echo "N_evts=$N_evts"
echo "N_seed=$N_seed"
echo "process_name=$process_name"

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh

#set up CMSSW
#cmsrel
scramv1 project CMSSW CMSSW_10_2_3
cd CMSSW_10_2_3/src

#cmsenv
eval `scramv1 runtime -sh`

#Configuration fragment has to live in a subdirectory and get compiled for cmsDriver to find it
mkdir -p Configuration/GenProduction/python
cp $initial_dir/*cfi.py Configuration/GenProduction/python/ 
scram b

#go back to starting directory
cd $initial_dir

#have a look at the PSet just in case
echo "PSet dump"
python -c "import PSet; print PSet.process.dumpPython()"

cmsDriver.py Configuration/GenProduction/python/BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-_13TeV-pythia8-evtgen_cfi.py --fileout file:out_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v12 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 1 --geometry DB:Extended --era Run2_2018 --python_filename step1_${process_name}_GEN-SIM_cfg.py --no_exec -n $N_evts

#reconfigure the random generator seed
echo "process.RandomNumberGeneratorService.generator.initialSeed = $N_seed" >> step1_${process_name}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 1000" >> step1_${process_name}_GEN-SIM_cfg.py
cmsRun step1_${process_name}_GEN-SIM_cfg.py

#step2
cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v12 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 1 --era Run2_2018 --filein file:out_GEN-SIM.root --fileout file:out_RAW.root --python_filename step2_${process_name}_RAW_cfg.py --no_exec -n -1

cmsRun step2_${process_name}_RAW_cfg.py


#step3
cmsDriver.py --filein file:out_RAW.root --fileout file:out_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v12 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 1 --era Run2_2018 --python_filename step3_${process_name}_AODSIM_cfg.py --no_exec -n -1

cmsRun step3_${process_name}_AODSIM_cfg.py


#step4
cmsDriver.py --filein file:out_AODSIM.root --fileout file:out_MINIAODSIM.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 102X_upgrade2018_realistic_v12 --step PAT --era Run2_2018 --nThreads 1 --python_filename step4_${process_name}_MINIAODSIM_cfg.py --no_exec -n -1

#here need to create the FrameworkJobReport.xml which gets propagated to crab
cmsRun -j FrameworkJobReport.xml step4_${process_name}_MINIAODSIM_cfg.py
