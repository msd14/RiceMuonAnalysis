# -*- coding: utf-8 -*-
#A simple script for running an analyzer interactively.
#Ideally run analyzer through CRAB3; only use this script as a backup.

import os
import subprocess

for i in range(1,519):  #Max number of EDM files from dataset.  
  with open('runSimpleMuonAnalyzer_cfg.py', 'r') as file:
    data = file.readlines()

  data[24] = """   fileNames = cms.untracked.vstring('/store/user/mdecaro/SingleMuon/SingleMuon_Run2017C-17Nov2017-v1_useParent/200103_210545/0000/Filter_"""+str(i)+""".root'),\n """

  with open('runSimpleMuonAnalyzer_cfg.py', 'w') as file:
    file.writelines( data )

  os.system('cmsRun runSimpleMuonAnalyzer_cfg.py')
  os.system('mv out_ana.root L1Ntuple_'+str(i)+'.root')
  os.system('mv L1Ntuple_'+str(i)+'.root L1Ntuples')

