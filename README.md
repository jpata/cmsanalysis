# Overview

This is my notebook for CMS related projects and various small code snippets.

### Contents

- crab: scripts to work with [CRAB](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile), the CMS grid submission tool
  - mcgen_userscript: run CMS MC generation from step1 (GEN-SIM) to MINIAOD (step4) in one job.
- opendata: scripts to work with [CERN open data](http://opendata.cern.ch)

## Misc stuff
### Finding the PU configuration of a MC sample
The true distribution of pileup vertices for a CMS MC sample can be extracted from the configuration fragment. 

  - Enter the sample DAS name (AODSIM) to PdmV to find the production campaigns: [link](https://cms-pdmv.cern.ch/mcm/requests?produce=%2FVBFHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8%2F*%2FAODSIM&page=0&shown=127)
  - Get the setup command for a particular campaign: [link](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIFall17DRPremix-04026)
  - Find the premixed MC sample: [link](https://cms-pdmv.cern.ch/mcm/requests?produce=%2FNeutrino_E-10_gun%2FRunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1%2FGEN-SIM-DIGI-RAW&page=0&shown=127)
  - Get the premix setup conf: [link](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/PPD-RunIISummer17PrePremix-00010)
  - From there, find the pileup configuration: `--pileup 2018_25ns_JuneProjectionFull18_PoissonOOTPU`
  - The pileup confs can be found in the folder `$CMSSW_RELEASE_BASE/src/SimGeneral/MixingModule/python`
  - This [script](https://github.com/UHH2/UHH2/blob/master/scripts/makeMCPileupHist.py) can be used to extract the MC pileup histogram.

### Internal presentations in chronological order

- 2019-08-29, Hmm JEC validation, [slides](https://indico.cern.ch/event/843650/contributions/3544420/attachments/1898929/3133828/2019_08_28_jecvalidation.pdf) [indico](https://indico.cern.ch/event/843650/)
- 2019-08-26, Hmm JEC validation, [slides](https://indico.cern.ch/event/843251/contributions/3539954/attachments/1897274/3130575/slides.pdf) [indico](https://indico.cern.ch/event/843251)
- 2019-08-14, Hmm JEC validation, [slides](https://indico.cern.ch/event/840943/contributions/3529969/attachments/1893494/3123355/slides.pdf) [indico](https://indico.cern.ch/event/840943)


### PFAlgo debugging

Add this to the end of the `step3.py` to enable logging and debug outputs.
```python
process.MessageLogger.categories += ["PFAlgo", "PFCandConnector", "PFBlockAlgo"]
process.MessageLogger.debugModules = cms.untracked.vstring("particleFlowTmp")
process.MessageLogger.debugs = cms.untracked.PSet(
     INFO =  cms.untracked.PSet(limit = cms.untracked.int32(0)),
     DEBUG   = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     PFAlgo = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     PFCandConnector = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     PFBlockAlgo = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     threshold = cms.untracked.string('DEBUG')
)

#To keep low-level inputs
clusters = [
  'keep recoPFClusters_particleFlowClusterECAL_*_*', 
  'keep recoPFClusters_particleFlowClusterHCAL_*_*', 
  'keep recoPFClusters_particleFlowClusterHO_*_*', 
  'keep recoPFClusters_particleFlowClusterHF_*_*', 
  'keep recoPFClusters_particleFlowClusterPS_*_*',
  'keep recoTracks_generalTracks_*_*',
  'keep recoTrackExtras_generalTracks_*_*',
  'keep TrackingRecHitsOwned_generalTracks_*_*',
  'keep recoGenParticles_prunedGenParticles_*_*'
]
 
process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step3_AOD.root'),
    outputCommands = process.AODSIMEventContent.outputCommands + clusters,
    splitLevel = cms.untracked.int32(0)
)
```

Compiling and running a test workflow.
```bash
scram b -j8 USER_CXXFLAGS+="-DEDM_ML_DEBUG" USER_CXXFLAGS+="-O" USER_CXXFLAGS+="-g"
runTheMatrix.py -l 38
```

### Selecting a subset of events in a file

```bash
cmsRun $CMSSW_RELEASE_BASE/src/PhysicsTools/Utilities/configuration/copyPickMerge_cfg.py inputFiles=root://cms-xrd-global.cern.ch///store/relval/CMSSW_11_0_0_pre12/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_110X_mcRun3_2021_realistic_v5-v1/20000/7CCD50E3-D786-4044-9CEF-793F6EC79183.root maxEvents=10
```


### Dump a Global Tag


```bash
conddb copy --destdb 110X_mcRun3_2021_realistic_v5.db 110X_mcRun3_2021_realistic_v5
```

In CMSSW configuration
```python
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, "110X_mcRun3_2021_realistic_v5", "")
process.GlobalTag.connect = "sqlite_file:110X_mcRun3_2021_realistic_v5.db"
```


### CMSSW gdb

```bash
scram b -j8 USER_CXXFLAGS+="-DEDM_ML_DEBUG" USER_CXXFLAGS+="-O0" USER_CXXFLAGS+="-g" USER_CXXFLAGS+="-fno-omit-frame-pointer"
```

### MessageLogger 


```python
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = "DEBUG"
process.MessageLogger.debugModules = ["*"]
```
