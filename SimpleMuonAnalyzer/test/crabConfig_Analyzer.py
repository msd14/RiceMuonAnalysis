# -*- coding: utf-8 -*-
#CRAB configuration to do processing of Monte Carlo. Inputs a dataset from previous step of processing chain.
#Note: Filenames in psetName must match filenames of input dataset.

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'SingleMu2017C_hits'
config.General.transferLogs = True
config.General.transferOutputs = True


config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runSimpleMuonAnalyzer_cfg.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.numCores = 8
#config.JobType.maxMemoryMB = 10000   #Use approx (1+1*ncores)GB


config.Data.inputDataset = '/SingleMuon/madecaro-SingleMuon_Run2017C-17Nov2017-v1_useParent-a6e7263c0d89399e8b4a6de9abe20c62/USER'
config.Data.inputDBS = 'phys03'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
config.Data.publication = True
config.Data.outputDatasetTag = 'CRAB3_SingleMu2017C_hits'


config.Site.storageSite = 'T3_US_FNALLPC'

 
