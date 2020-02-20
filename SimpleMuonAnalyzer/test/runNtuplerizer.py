# -*- coding: utf-8 -*-
import os
import subprocess

i=3
while i<4:  
  with open('runSimpleMuonAnalyzer_cfg.py', 'r') as file:
    data = file.readlines()

  #data[25] = """   fileNames = cms.untracked.vstring('/store/user/mdecaro/SingleMuon/SingleMuon_Run2017C-17Nov2017-v1_Parent/200204_181709/0000/Filter_"""+str(i)+""".root'),\n """

  data[25] = """   fileNames = cms.untracked.vstring('/store/user/mdecaro/step1/step2/step2_"""+str(i)+""".root'),\n """

  with open('runSimpleMuonAnalyzer_cfg.py', 'w') as file:
    file.writelines( data )


  os.system('cmsRun runSimpleMuonAnalyzer_cfg.py')
  os.system('mv out_ana.root L1Ntuple_'+str(i)+'.root')
  #os.system('xrdcp -f L1Ntuple_'+str(i)+'.root root://cmseos.fnal.gov//store/user/mdecaro/SMNtuples')

  os.system('mv L1Ntuple_'+str(i)+'.root L1NtuplesMC')

  i+=1

