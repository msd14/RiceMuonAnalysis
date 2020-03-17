# -*- coding: utf-8 -*-
import FWCore.ParameterSet.Config as cms
		
process = cms.Process("SKIM")
#initialize MessageLogger 
process.load("FWCore.MessageService.MessageLogger_cfi")
	
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:step0.root")
)
process.maxEvents = cms.untracked.PSet ( input = cms.untracked.int32 ( -1 ) )

process.myfilter = cms.EDFilter("FilterSample2GenMu")

process.filterPath = cms.Path(process.myfilter)

process.output = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string( "Filter.root" ),
    SelectEvents = cms.untracked.PSet(
	SelectEvents = cms.vstring("filterPath")
    )
)
	
process.out = cms.EndPath( process.output )
