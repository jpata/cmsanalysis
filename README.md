# Overview

This is my notebook for CMS related projects and misc code.

# Internal presentations in chronological order

- 2019-08-29, Hmm JEC validation, [slides](https://indico.cern.ch/event/843650/contributions/3544420/attachments/1898929/3133828/2019_08_28_jecvalidation.pdf) [indico](https://indico.cern.ch/event/843650/)
- 2019-08-26, Hmm JEC validation, [slides](https://indico.cern.ch/event/843251/contributions/3539954/attachments/1897274/3130575/slides.pdf) [indico](https://indico.cern.ch/event/843251)
- 2019-08-14, Hmm JEC validation, [slides](https://indico.cern.ch/event/840943/contributions/3529969/attachments/1893494/3123355/slides.pdf) [indico](https://indico.cern.ch/event/840943)

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

