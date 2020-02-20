# -*- coding: utf-8 -*-
#CRAB configuration to do processing of Monte Carlo. Inputs a dataset from previous step of processing chain.
#Note: Filenames in psetName must match filenames of input dataset.

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = '2017C_Ntuples'
config.General.transferLogs = True
config.General.transferOutputs = True


config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runSimpleMuonAnalyzer_cfg.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.numCores = 8
#config.JobType.maxMemoryMB = 10000   #Use approx (1+1*ncores)GB


#config.Data.inputDataset = '/MSSMD_step0_GENSIM_FilterTest/madecaro-CRAB3_MSSMD_step2_FilterTest-9c4d99cb477481928df9743d72420af7/USER'
config.Data.inputDataset = '/SingleMuon/madecaro-SingleMuon_Run2017C-17Nov2017-v1_Parent-a6e7263c0d89399e8b4a6de9abe20c62/USER'
config.Data.inputDBS = 'phys03'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.publication = True
config.Data.outputDatasetTag = 'CRAB3_2017C'


config.Site.storageSite = 'T3_US_FNALLPC'

 