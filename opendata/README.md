
#Open data, RunIISummer16MiniAODv2

- QCD_Pt-15to7000: http://opendata.cern.ch/record/12021

# NanoAOD

Summary on how to produce NanoAOD: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

```bash
cmsDriver.py myNanoProdMc -s NANO --mc --eventcontent NANOAODSIM \
  --datatier NANOAODSIM --no_exec \
  --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v8 \
  --era Run2_2016,run2_miniAOD_80XLegacy
```

Add this to the end of the file `myNanoProdMc2016_NANO.py`:
```python
import sys
process.maxEvents.input = cms.untracked.int32(-1)
process.source.fileNames = cms.untracked.vstring(sys.argv[2:])
process.NANOAODSIMoutput.fileName = cms.untracked.string('out.root')
```
