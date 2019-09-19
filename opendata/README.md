
# Open data


## RunI, Summer12

- DY2JetsToLL_M-50: http://opendata.cern.ch/record/7720, http://opendata.cern.ch/record/7721 

## RunIISummer16MiniAODv2

- QCD_Pt-15to7000: http://opendata.cern.ch/record/12021

# NanoAOD from AOD using the outreach tool

Recipe here: https://github.com/cms-opendata-analyses/AOD2NanoAODOutreachTool

# NanoAOD from MiniAOD

Summary on how to produce NanoAOD: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

```bash
cmsDriver.py myNanoProdMc -s NANO --mc --eventcontent NANOAODSIM \
  --datatier NANOAODSIM  --no_exec \
  --conditions 102X_mcRun2_asymptotic_v7 \
  --era Run2_2016,run2_miniAOD_80XLegacy \
  --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))"
```

Add this to the end of the file `myNanoProdMc2016_NANO.py`:
```python
import sys
process.maxEvents.input = cms.untracked.int32(-1)
process.source.fileNames = cms.untracked.vstring(sys.argv[2:])
process.NANOAODSIMoutput.fileName = cms.untracked.string('out.root')
```
