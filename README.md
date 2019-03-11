Recipes on how to use CRAB.

- mcgen_userscript: run CMS MC generation from step1 (GEN-SIM) to MINIAOD (step4) in one job.


### Finding the PU configuration of a MC sample
The true distribution of pileup vertices for a CMS MC sample can be extracted from the configuration fragment. 

  - Enter the sample DAS name (AODSIM) to PdmV to find the production campaigns: [link](https://cms-pdmv.cern.ch/mcm/requests?produce=%2FVBFHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8%2F*%2FAODSIM&page=0&shown=127)
  - Get the setup command for a particular campaign: [link](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIFall17DRPremix-04026)
  - Find the premixed MC sample: [link](https://cms-pdmv.cern.ch/mcm/requests?produce=%2FNeutrino_E-10_gun%2FRunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1%2FGEN-SIM-DIGI-RAW&page=0&shown=127)
  - Get the premix setup conf: [link](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/PPD-RunIISummer17PrePremix-00010)
  - From there, find the pileup configuration: `--pileup 2018_25ns_JuneProjectionFull18_PoissonOOTPU`
  - The pileup confs can be found in the folder `$CMSSW_RELEASE_BASE/src/SimGeneral/MixingModule/python`
  - This [script](https://github.com/UHH2/UHH2/blob/master/scripts/makeMCPileupHist.py) can be used to extract the MC pileup histogram.

