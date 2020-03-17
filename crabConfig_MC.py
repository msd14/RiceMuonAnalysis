# -*- coding: utf-8 -*-
from CRABClient.UserUtilities import config
config = config()


config.General.requestName = 'MSSMD_EMTFpp_step0_GENSIM_12_test'
config.General.transferLogs = True

config.JobType.maxMemoryMB = 10000
config.JobType.pluginName = 'PrivateMC'
config.JobType.inputFiles = ['MSSMD_100k_50mm_1.lhe', 'MSSMD_100k_50mm_2.lhe']
config.JobType.numCores = 8
config.JobType.generator = 'lhe'
config.JobType.psetName = 'Pythia8_CP5_HadronizerFilter_13TeV_cfi_GEN_SIM.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 10000   #Use approx (1+1*ncores)GB

config.Data.totalUnits = 200000  #number of prefiltered events in input file
config.Data.unitsPerJob = 10000
config.Data.outputPrimaryDataset = 'MSSMD_EMTFpp_step0_GENSIM_12_test'
config.Data.splitting = 'EventBased'
config.Data.outputDatasetTag = 'MSSMD_EMTFpp_step0_GENSIM_12_test'


config.Site.storageSite = 'T3_US_FNALLPC'

