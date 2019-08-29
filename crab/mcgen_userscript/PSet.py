import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("EmptySource",
    firstEvent = cms.untracked.uint32(1),
    firstLuminosityBlock = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(1),
    numberEventsInLuminosityBlock = cms.untracked.uint32(100)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

process.maxSecondsUntilRampdown = cms.untracked.PSet(
    input = cms.untracked.int32(-60)
)

process.output = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('out_MINIAODSIM.root'),
    logicalFileName = cms.untracked.string('')
)


process.CPU = cms.Service("CPU")


process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
    jobReportOutputOnly = cms.untracked.bool(True)
)


process.Timing = cms.Service("Timing",
    summaryOnly = cms.untracked.bool(True)
)


process.out = cms.EndPath(process.output)
