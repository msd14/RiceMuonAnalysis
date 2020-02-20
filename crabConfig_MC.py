# -*- coding: utf-8 -*-
from CRABClient.UserUtilities import config
config = config()


config.General.requestName = 'MSSMD_step0_GENSIM_test'
config.General.transferLogs = True

config.JobType.maxMemoryMB = 10000
config.JobType.pluginName = 'PrivateMC'
#config.JobType.inputFiles = ['MSSMD_100k_50mm_1.lhe', 'MSSMD_100k_50mm_2.lhe', 'MSSMD_100k_50mm_3.lhe', 'MSSMD_100k_50mm_4.lhe','MSSMD_100k_50mm_5.lhe', 'MSSMD_100k_50mm_6.lhe','MSSMD_100k_50mm_7.lhe', 'MSSMD_100k_50mm_8.lhe','MSSMD_100k_50mm_9.lhe', 'MSSMD_100k_50mm_10.lhe']
config.JobType.inputFiles = ['MSSMD_100k_50mm_1.lhe']
config.JobType.numCores = 8
config.JobType.generator = 'lhe'
config.JobType.psetName = 'Pythia8_CP5_HadronizerFilter_13TeV_cfi_GEN_SIM.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.totalUnits = 100000  #number of prefiltered events in input file
config.Data.unitsPerJob = 5000
config.Data.outputPrimaryDataset = 'MSSMD_step0_GENSIM_test'
config.Data.splitting = 'EventBased'
config.Data.outputDatasetTag = 'MSSMD_step0_GENSIM_test'


config.Site.storageSite = 'T3_US_FNALLPC'

