import FWCore.ParameterSet.Config as cms

process = cms.Process("SimpleMuon")

## Standard sequence
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi')
process.load('TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.source = cms.Source(
  "PoolSource",
  fileNames = cms.untracked.vstring(
      '/store/user/mdecaro/SingleMuon/SingleMuon_Run2017C-17Nov2017-v1_useParent/200103_210545/0000/Filter_1.root'
  ),
)

process.SimpleMuonAnalyzer = cms.EDAnalyzer(
    "SimpleMuonAnalyzer",
    verbose = cms.bool(False),
    cscSegments = cms.InputTag("cscSegments"),
    muons = cms.InputTag("muons"),
    emtf = cms.InputTag("gmtStage2Digis","EMTF"),
)

process.TFileService = cms.Service(
  "TFileService",
  fileName = cms.string("out_ana.root")
)

process.p = cms.Path(process.SimpleMuonAnalyzer)

## messages
print
print 'Input files:'
print '----------------------------------------'
print process.source.fileNames
print
print 'Output file:'
print '----------------------------------------'
print process.TFileService.fileName
print
