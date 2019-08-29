import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

#Define the process name here only once
mc_proc_name = 'BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-'

config = config()

config.General.requestName     = 'run_1'
config.General.workArea        = 'BPhysics_gen'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'

#this is needed to configure the job output
config.JobType.psetName   = 'PSet.py'

config.JobType.numCores = 1

config.JobType.scriptExe = 'job.sh'

#does not support "-" character in argument name due to some crab REST API issue (?)
#config.JobType.scriptArgs = [mc_proc_name,]
config.JobType.maxJobRuntimeMin = 4*60

#this gen fragment will be placed directly in the starting directory 
config.JobType.inputFiles = [os.environ["CMSSW_BASE"] + '/src/Configuration/GenProduction/python/{0}_13TeV-pythia8-evtgen_cfi.py'.format(mc_proc_name)]

config.Data.outputPrimaryDataset = 'BPhysics'
config.Data.inputDBS             = 'global'

#
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 20000
config.Data.totalUnits           = 20 * config.Data.unitsPerJob 

config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = mc_proc_name

config.Site.storageSite = 'T2_US_Caltech'
