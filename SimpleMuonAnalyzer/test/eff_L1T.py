#! /usr/bin/env python
# -*- coding: utf-8 -*-

print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
import Helper as h

print '------> Importing Root File'

## Configuration settings
MAX_EVT  = -1 ## Maximum number of events to process
PRT_EVT  = 10000 ## Print every Nth event

## L1NTuple branches
evt_tree  = TChain('SimpleMuonAnalyzer/Events')

dir1 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/SingleMuon_Run2018A-17Sep2018-v2_AOD/191004_152709/0000/Ntuples/'
dir2 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018B-17Sep2018-v2_AOD/191003_214638/0000/Ntuples/'
dir3 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018C-17Sep2018-v2_AOD/191003_214758/0000/Ntuples/'
dir4 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018D-PromptReco-v2_AOD/191003_214926/0000/Ntuples/'
run_str = '_2018D'


## Load input files
#i = 1
#while i<300:
    #file_name = dir1+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

i = 1
while i<256:
    file_name = dir2+"L1Ntuple_"+str(i)+".root"
    print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    evt_tree.Add(file_name)
    i+=1

#i = 1
#while i<262:
    #file_name = dir3+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

#i = 1
#while i<80:
    #file_name = dir4+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

## ================ Histograms ======================
scale_pt_temp = [0, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30, 35, 45, 60, 75, 100, 140, 150]
scale_pt = array('f', scale_pt_temp)
max_pt = scale_pt_temp[len(scale_pt_temp) - 1] - 0.01

sector_boundries = [0.261799, 1.309, 2.35619, 3.40339, 4.45059, 5.49779]
sector_boundries_fixed=[]
i=0
while i<len(sector_boundries):
  sector_boundries_fixed.append(sector_boundries[i] - np.pi)
  i+=1

eta_bins = [256, -2.8, 2.8]
phi_bins = [129, -np.pi, np.pi]


h_nEmtf = TH1D('h_nEmtf', '', 8, 0, 8)
h_nReco = TH1D('h_nReco', '', 8, 0, 4)

h_emtf_pt = TH1D('h_emtf_pt', '', 70, 0, 300)
h_emtf1_pt = TH1D('h_emtf1_pt', '', 70, 0, 300)
h_emtf2_pt = TH1D('h_emtf2_pt', '', 70, 0, 300) 
h_emtf3_pt = TH1D('h_emtf3_pt', '', 70, 0, 300)
h_emtf_eta = TH1D('h_emtf_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf1_eta = TH1D('h_emtf1_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf2_eta = TH1D('h_emtf2_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf3_eta = TH1D('h_emtf3_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf_phi = TH1D('h_emtf_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf1_phi = TH1D('h_emtf1_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf2_phi = TH1D('h_emtf2_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf3_phi = TH1D('h_emtf3_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf_charge = TH1D('h_emtf_charge', '', 4, -2, 2)
h_emtf1_charge = TH1D('h_emtf1_charge', '', 4, -2, 2)
h_emtf2_charge = TH1D('h_emtf2_charge', '', 4, -2, 2)
h_emtf3_charge = TH1D('h_emtf3_charge', '', 4, -2, 2)
h_emtf_quality = TH1D('h_emtf_quality', '', 16, 0, 16)
h_emtf1_quality = TH1D('h_emtf1_quality', '', 16, 0, 16)
h_emtf2_quality = TH1D('h_emtf2_quality', '', 16, 0, 16)
h_emtf3_quality = TH1D('h_emtf3_quality', '', 16, 0, 16)


h_reco_pt = TH1D('h_reco_pt', '', 256, 0, 1000)
h_reco1_pt = TH1F('h_reco1_pt', '', 256, 0, 1000)
h_reco2_pt = TH1F('h_reco2_pt', '', 256, 0, 250)
h_reco_eta = TH1D('h_reco_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco1_eta = TH1D('h_reco1_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco2_eta = TH1D('h_reco2_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco_phi = TH1D('h_reco_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_reco1_phi = TH1D('h_reco1_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_reco2_phi = TH1D('h_reco2_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_reco_charge = TH1D('h_reco_charge', '', 4, -2, 2)
h_reco1_charge = TH1D('h_reco1_charge', '', 4, -2, 2)
h_reco2_charge = TH1D('h_reco2_charge', '', 4, -2, 2)


none_count       = 0
reco_med_count   = 0
reco_pT_count    = 0
match_count      = 0

## ================================================
# Loop over over events in TFile
for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  #dR < 0.1 pre-selection may not have been applied properly, so check first.
  if (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) > 3.14:  dPhiNorm = (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) - (2*3.14)
  if (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) < -3.14: dPhiNorm = (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) + (2*3.14)
  if (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) <= 3.14 and (evt_tree.reco_phi[0] - evt_tree.reco_phi[1]) >= -3.14: dPhiNorm = (evt_tree.reco_phi[0] - evt_tree.reco_phi[1])

  if evt_tree.reco_eta[0] < -90 or evt_tree.reco_eta[1] < -90: continue
  if evt_tree.reco_phi[0] < -90 or evt_tree.reco_phi[1] < -90: continue

  #if h.CalcDR(evt_tree.reco_eta[0], evt_tree.reco_eta[1], dPhiNorm) > 0.1: continue

  #Ignore events with offline reco muons near the sector boundries, due to duplicate tracks. (15, 75, 135, 195, 255, 315 degrees)
  check=0
  i=0
  while i<len(sector_boundries_fixed):
    if abs(evt_tree.reco_phi[0]-sector_boundries_fixed[i]) < 0.0872665: check+=1
    if abs(evt_tree.reco_phi[1]-sector_boundries_fixed[i]) < 0.0872665: check+=1
    i+=1
  if check!=0: continue

  none_count+=1 

  h_nReco.Fill(evt_tree.nRecoMuon)

  reco_pT = [] #First muon = leading, second muon = subleading
  reco_eta = []
  reco_phi = []

  if evt_tree.reco_pt[0] > evt_tree.reco_pt[1]: 
    reco_pT.append(evt_tree.reco_pt[0])
    reco_pT.append(evt_tree.reco_pt[1])
    reco_eta.append(evt_tree.reco_eta[0])
    reco_eta.append(evt_tree.reco_eta[1])
    reco_phi.append(evt_tree.reco_phi[0])
    reco_phi.append(evt_tree.reco_phi[1])
  if evt_tree.reco_pt[0] < evt_tree.reco_pt[1]:
    reco_pT.append(evt_tree.reco_pt[1])
    reco_pT.append(evt_tree.reco_pt[0])
    reco_eta.append(evt_tree.reco_eta[1])
    reco_eta.append(evt_tree.reco_eta[0])
    reco_phi.append(evt_tree.reco_phi[1])
    reco_phi.append(evt_tree.reco_phi[0])

  #Fill nEmtf after ignoring duplicate tracks.
  i,j=0,0
  while i<len(evt_tree.emtf_pt):
    if i==0: j+=1
    if i==1 and abs(evt_tree.emtf_phi[1] - evt_tree.emtf_phi[0])>0.2: j+=1
    if i==2 and abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[0])>0.2 and abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[1])>0.2: j+=1
    if i==3 and abs(evt_tree.emtf_phi[3] - evt_tree.emtf_phi[0])>0.2 and abs(evt_tree.emtf_phi[3] - evt_tree.emtf_phi[1])>0.2 and abs(evt_tree.emtf_phi[3] - evt_tree.emtf_phi[2])>0.2: j+=1
    if i==4 and abs(evt_tree.emtf_phi[4] - evt_tree.emtf_phi[0])>0.2 and abs(evt_tree.emtf_phi[4] - evt_tree.emtf_phi[1])>0.2 and abs(evt_tree.emtf_phi[4] - evt_tree.emtf_phi[2])>0.2 and abs(evt_tree.emtf_phi[4] - evt_tree.emtf_phi[3])>0.2: j+=1
    i+=1
  h_nEmtf.Fill(j)


  h_reco1_pt.Fill(reco_pT[0])
  h_reco1_eta.Fill(evt_tree.reco_eta[0])
  h_reco1_phi.Fill(evt_tree.reco_phi[0])
  h_reco1_charge.Fill(evt_tree.reco_charge[0])

  h_reco2_pt.Fill(reco_pT[1])
  h_reco2_eta.Fill(evt_tree.reco_eta[1])
  h_reco2_phi.Fill(evt_tree.reco_phi[1])
  h_reco2_charge.Fill(evt_tree.reco_charge[1])

  j=0
  while j<len(evt_tree.reco_pt):
    h_reco_pt.Fill(reco_pT[j])
    h_reco_eta.Fill(evt_tree.reco_eta[j])
    h_reco_phi.Fill(evt_tree.reco_phi[j])
    h_reco_charge.Fill(evt_tree.reco_charge[j])
    j+=1


  #Fills emtf tracks quantities and checks for duplicate tracks by matching track etas. Does not fill duplicates.
  j=0
  while j<len(evt_tree.emtf_pt):
    if j==0: 
      #print "trk 1 pT, eta phi:", evt_tree.emtf_pt[j], evt_tree.emtf_eta[j], evt_tree.emtf_phi[j]
    
      h_emtf_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf1_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf1_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf1_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf1_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf_quality.Fill(evt_tree.emtf_quality[j])
      h_emtf1_quality.Fill(evt_tree.emtf_quality[j])
    if j==1 and abs(evt_tree.emtf_eta[1] - evt_tree.emtf_eta[0])>0.2 and abs(evt_tree.emtf_phi[1] - evt_tree.emtf_phi[0])>0.2:
      #print "trk 2 pT, eta phi:", evt_tree.emtf_pt[j], evt_tree.emtf_eta[j], evt_tree.emtf_phi[j]
      #print abs(evt_tree.emtf_eta[1] - evt_tree.emtf_eta[0])

      h_emtf_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf2_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf2_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf2_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf2_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf_quality.Fill(evt_tree.emtf_quality[j])
      h_emtf2_quality.Fill(evt_tree.emtf_quality[j])
    if j==2 and abs(evt_tree.emtf_eta[2] - evt_tree.emtf_eta[0])>0.2 and abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[0])>0.2 and (abs(evt_tree.emtf_eta[2] - evt_tree.emtf_eta[1])>0.2) and (abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[1])>0.2):
      #print "trk 3 pT, eta phi:", evt_tree.emtf_pt[j], evt_tree.emtf_eta[j], evt_tree.emtf_phi[j]

      h_emtf_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf3_pt.Fill(evt_tree.emtf_pt[j])
      h_emtf3_eta.Fill(evt_tree.emtf_eta[j])
      h_emtf3_phi.Fill(evt_tree.emtf_phi[j])
      h_emtf3_charge.Fill(evt_tree.emtf_charge[j])

      h_emtf_quality.Fill(evt_tree.emtf_quality[j])
      h_emtf3_quality.Fill(evt_tree.emtf_quality[j])
    j+=1


  if evt_tree.reco_isMediumMuon[0] != 1 or evt_tree.reco_isMediumMuon[1] != 1: continue
  
  reco_med_count+=1

  if reco_pT[0] < 26 or reco_pT[1] < 26: continue

  reco_pT_count+=1

  #print '-------------------------------'

print '-----------'
print 'Preselection only:', none_count
print 'Both reco muons medium:', reco_med_count
print 'Both reco muons pT > 26 GeV:', reco_pT_count
#match_count
print '-----------'


############################################################
### Write output file with histograms and efficiencies 
############################################################

#c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_pt.SetMinimum(1)
#h_reco_pt.Draw()
#h_reco_pt.SetTitle('All offline reco muon pT')
#h_reco_pt.GetXaxis().SetTitle('pT (GeV)')
#h_reco_pt.Write()
#c1.SaveAs("trees/reco_pT.png")
#c1.Close()

#c2 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco1_pt.SetMinimum(1)
#h_reco1_pt.Draw()
#h_reco1_pt.SetTitle('First offline reco muon pT')
#h_reco1_pt.GetXaxis().SetTitle('pT (GeV)')
#h_reco1_pt.Write()
#c2.SaveAs("trees/reco1_pT.png")
#c2.Close()

#c3 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_pt.SetMinimum(1)
#h_reco2_pt.Draw()
#h_reco2_pt.SetTitle('Second offline reco muon pT')
#h_reco2_pt.GetXaxis().SetTitle('pT (GeV)')
#h_reco2_pt.Write()
#c3.SaveAs("trees/reco2_pT.png")
#c3.Close()

#c4 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_eta.SetMinimum(1)
#h_reco_eta.Draw()
#h_reco_eta.SetTitle('All offline reco muon #eta')
#h_reco_eta.GetXaxis().SetTitle('#eta')
#h_reco_eta.Write()
#c4.SaveAs("trees/reco_eta.png")
#c4.Close()

#c5 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco1_eta.SetMinimum(1)
#h_reco1_eta.Draw()
#h_reco1_eta.SetTitle('First offline reco muon #eta')
#h_reco1_eta.GetXaxis().SetTitle('#eta')
#h_reco1_eta.Write()
#c5.SaveAs("trees/reco1_eta.png")
#c5.Close()

#c5 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_eta.SetMinimum(1)
#h_reco2_eta.Draw()
#h_reco2_eta.SetTitle('Second offline reco muon #eta')
#h_reco2_eta.GetXaxis().SetTitle('#eta')
#h_reco2_eta.Write()
#c5.SaveAs("trees/reco2_eta.png")
#c5.Close()

#c6 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_phi.SetMinimum(1)
#h_reco_phi.Draw()
#h_reco_phi.SetTitle('All offline reco muon #phi')
#h_reco_phi.GetXaxis().SetTitle('#phi')
#h_reco_phi.Write()
#c6.SaveAs("trees/reco_phi.png")
#c6.Close()

#c7 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco1_phi.SetMinimum(1)
#h_reco1_phi.Draw()
#h_reco1_phi.SetTitle('First offline reco muon #phi')
#h_reco1_phi.GetXaxis().SetTitle('#phi')
#h_reco1_phi.Write()
#c7.SaveAs("trees/reco1_phi.png")
#c7.Close()

#c8 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_phi.SetMinimum(1)
#h_reco2_phi.Draw()
#h_reco2_phi.SetTitle('Second offline reco muon #phi')
#h_reco2_phi.GetXaxis().SetTitle('#phi')
#h_reco2_phi.Write()
#c8.SaveAs("trees/reco2_phi.png")
#c8.Close()

#c9 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_charge.SetMinimum(1)
#h_reco_charge.Draw()
#h_reco_charge.SetTitle('All offline reco muon charge')
#h_reco_charge.GetXaxis().SetTitle('charge')
#h_reco_charge.Write()
#c9.SaveAs("trees/reco_charge.png")
#c9.Close()

#c10 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco1_charge.SetMinimum(1)
#h_reco1_charge.Draw()
#h_reco1_charge.SetTitle('First offline reco muon charge')
#h_reco1_charge.GetXaxis().SetTitle('charge')
#h_reco1_charge.Write()
#c10.SaveAs("trees/reco1_charge.png")
#c10.Close()

#c11 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_charge.SetMinimum(1)
#h_reco2_charge.Draw()
#h_reco2_charge.SetTitle('Second offline reco muon charge')
#h_reco2_charge.GetXaxis().SetTitle('charge')
#h_reco2_charge.Write()
#c11.SaveAs("trees/reco2_charge.png")
#c11.Close()

c12 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_pt.SetMinimum(1)
h_emtf_pt.Draw()
h_emtf_pt.SetTitle('All EMTF Tracks pT')
h_emtf_pt.GetXaxis().SetTitle('pT (GeV)')
h_emtf_pt.Write()
c12.SaveAs("trees/emtf_pT.png")
c12.Close()

c13 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf1_pt.SetMinimum(1)
h_emtf1_pt.Draw()
h_emtf1_pt.SetTitle('First Emtf track pT')
h_emtf1_pt.GetXaxis().SetTitle('pT (GeV)')
h_emtf1_pt.Write()
c13.SaveAs("trees/emtf1_pT.png")
c13.Close()

c14 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_pt.SetMinimum(1)
h_emtf2_pt.Draw()
h_emtf2_pt.SetTitle('Second Emtf track pT')
h_emtf2_pt.GetXaxis().SetTitle('pT (GeV)')
h_emtf2_pt.Write()
c14.SaveAs("trees/emtf2_pT.png")
c14.Close()

c15 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf3_pt.SetMinimum(1)
h_emtf3_pt.Draw()
h_emtf3_pt.SetTitle('Third Emtf track pT')
h_emtf3_pt.GetXaxis().SetTitle('pT (GeV)')
h_emtf3_pt.Write()
c15.SaveAs("trees/emtf3_pT.png")
c15.Close()

c16 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_eta.SetMinimum(1)
h_emtf_eta.Draw()
h_emtf_eta.SetTitle('All EMTF tracks #eta')
h_emtf_eta.GetXaxis().SetTitle('#eta')
h_emtf_eta.Write()
c16.SaveAs("trees/emtf_eta.png")
c16.Close()

c17 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf1_eta.SetMinimum(1)
h_emtf1_eta.Draw()
h_emtf1_eta.SetTitle('First Emtf track #eta')
h_emtf1_eta.GetXaxis().SetTitle('#eta')
h_emtf1_eta.Write()
c17.SaveAs("trees/emtf1_eta.png")
c17.Close()

c18 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_eta.SetMinimum(1)
h_emtf2_eta.Draw()
h_emtf2_eta.SetTitle('Second Emtf track #eta')
h_emtf2_eta.GetXaxis().SetTitle('#eta')
h_emtf2_eta.Write()
c18.SaveAs("trees/emtf2_eta.png")
c18.Close()

c19 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf3_eta.SetMinimum(1)
h_emtf3_eta.Draw()
h_emtf3_eta.SetTitle('Third Emtf track #eta')
h_emtf3_eta.GetXaxis().SetTitle('#eta')
h_emtf3_eta.Write()
c19.SaveAs("trees/emtf3_eta.png")
c19.Close()

c20 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_phi.SetMinimum(1)
h_emtf_phi.Draw()
h_emtf_phi.SetTitle('All EMTF tracks #phi')
h_emtf_phi.GetXaxis().SetTitle('#phi')
h_emtf_phi.Write()
c20.SaveAs("trees/emtf_phi.png")
c20.Close()

c21 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf1_phi.SetMinimum(1)
h_emtf1_phi.Draw()
h_emtf1_phi.SetTitle('First emtf track #phi')
h_emtf1_phi.GetXaxis().SetTitle('#phi')
h_emtf1_phi.Write()
c21.SaveAs("trees/emtf1_phi.png")
c21.Close()

c22 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_phi.SetMinimum(1)
h_emtf2_phi.Draw()
h_emtf2_phi.SetTitle('Second emtf track #phi')
h_emtf2_phi.GetXaxis().SetTitle('#phi')
h_emtf2_phi.Write()
c22.SaveAs("trees/emtf2_phi.png")
c22.Close()

c23 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf3_phi.SetMinimum(1)
h_emtf3_phi.Draw()
h_emtf3_phi.SetTitle('Third emtf track #phi')
h_emtf3_phi.GetXaxis().SetTitle('#phi')
h_emtf3_phi.Write()
c23.SaveAs("trees/emtf3_phi.png")
c23.Close()

c24 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_charge.SetMinimum(1)
h_emtf_charge.Draw()
h_emtf_charge.SetTitle('All emtf muon charge')
h_emtf_charge.GetXaxis().SetTitle('charge')
h_emtf_charge.Write()
c24.SaveAs("trees/emtf_charge.png")
c24.Close()

c25 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf1_charge.SetMinimum(1)
h_emtf1_charge.Draw()
h_emtf1_charge.SetTitle('First emtf muon charge')
h_emtf1_charge.GetXaxis().SetTitle('charge')
h_emtf1_charge.Write()
c25.SaveAs("trees/emtf1_charge.png")
c25.Close()

c26 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_charge.SetMinimum(1)
h_emtf2_charge.Draw()
h_emtf2_charge.SetTitle('Second emtf muon charge')
h_emtf2_charge.GetXaxis().SetTitle('charge')
h_emtf2_charge.Write()
c26.SaveAs("trees/emtf2_charge.png")
c26.Close()

c27 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf3_charge.SetMinimum(1)
h_emtf3_charge.Draw()
h_emtf3_charge.SetTitle('Third emtf muon charge')
h_emtf3_charge.GetXaxis().SetTitle('charge')
h_emtf3_charge.Write()
c27.SaveAs("trees/emtf3_charge.png")
c27.Close()


#----------------------------
#Overlays--------------------

c34 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_nEmtf.SetMinimum(1)
h_nEmtf.Draw()
h_nEmtf.SetTitle('Number of EMTF tracks')
h_nEmtf.GetXaxis().SetTitle('EMTF Tracks')
h_nEmtf.Write()
c34.SaveAs("trees/nEmtf.png")
c34.Close()

#c35 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_nReco.SetMinimum(1)
#h_nReco.Draw()
#h_nReco.SetTitle('Number of Offline Reco Muons')
#h_nReco.GetXaxis().SetTitle('Reco Muons')
#h_nReco.Write()
#c35.SaveAs("trees/nReco.png")
#c35.Close()

c36 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_quality.SetMinimum(1)
h_emtf_quality.Draw()
h_emtf_quality.SetTitle('EMTF Track Quality')
h_emtf_quality.GetXaxis().SetTitle('Quality')
h_emtf_quality.Write()
c36.SaveAs("trees/emtf_quality.png")
c36.Close()

c37 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf1_quality.SetMinimum(1)
h_emtf1_quality.Draw()
h_emtf1_quality.SetTitle('First EMTF Track Quality')
h_emtf1_quality.GetXaxis().SetTitle('Quality')
h_emtf1_quality.Write()
c37.SaveAs("trees/emtf1_quality.png")
c37.Close()

c38 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_quality.SetMinimum(1)
h_emtf2_quality.Draw()
h_emtf2_quality.SetTitle('Second EMTF Track Quality')
h_emtf2_quality.GetXaxis().SetTitle('Quality')
h_emtf2_quality.Write()
c38.SaveAs("trees/emtf2_quality.png")
c38.Close()

c39 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf3_quality.SetMinimum(1)
h_emtf3_quality.Draw()
h_emtf3_quality.SetTitle('Third EMTF Track Quality')
h_emtf3_quality.GetXaxis().SetTitle('Quality')
h_emtf3_quality.Write()
c39.SaveAs("trees/emtf3_quality.png")
c39.Close()

c40 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
h_emtf1_pt.SetFillColor(kRed)
h_emtf1_pt.Draw()
h_emtf2_pt.SetFillColor(kBlue)
h_emtf2_pt.Draw("same")
h_emtf3_pt.SetFillColor(kGreen)
h_emtf3_pt.Draw("same")
gPad.SetLogy()
h_emtf1_pt.SetMinimum(1)
h_emtf1_pt.SetTitle('pT of first emtf track (red), second (blue), and third (green)')
c40.SaveAs("trees/emtf_pT_overlay.png")
c40.Close()

c41 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
h_emtf1_phi.SetFillColor(kRed)
h_emtf1_phi.Draw()
h_emtf2_phi.SetFillColor(kBlue)
h_emtf2_phi.Draw("same")
h_emtf3_phi.SetFillColor(kGreen)
h_emtf3_phi.Draw("same")
gPad.SetLogy()
h_emtf1_phi.SetMinimum(1)
h_emtf1_phi.SetTitle('#phi of first emtf track (red), second (blue), and third (green)')
c41.SaveAs("trees/emtf_phi_overlay.png")
c41.Close()

c42 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
h_emtf1_eta.SetFillColor(kRed)
h_emtf1_eta.Draw()
h_emtf2_eta.SetFillColor(kBlue)
h_emtf2_eta.Draw("same")
h_emtf3_eta.SetFillColor(kGreen)
h_emtf3_eta.Draw("same")
gPad.SetLogy()
h_emtf1_eta.SetMinimum(1)
h_emtf1_eta.SetTitle('#eta of first emtf track (red), second (blue), and third (green)')
c42.SaveAs("trees/emtf_eta_overlay.png")
c42.Close()

#c43 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_reco1_pt.SetFillColor(kRed)
#h_reco1_pt.Draw()
#h_reco2_pt.SetFillColor(kBlue)
#h_reco2_pt.Draw("same")
#gPad.SetLogy()
#h_reco1_pt.SetMinimum(1)
#h_reco1_pt.SetTitle('pT of first reco muon (red) and second muon (blue)')
#c43.SaveAs("trees/reco_pT_overlay.png")
#c43.Close()

#c44 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_reco1_eta.SetFillColorAlpha(kRed, 0.35)
#h_reco1_eta.Draw()
#h_reco2_eta.SetFillColorAlpha(kBlue, 1.0)
#h_reco2_eta.Draw("same")
#gPad.SetLogy()
#h_reco1_eta.SetMinimum(1)
#h_reco1_eta.SetTitle('#eta of first reco muon (red) and second muon (blue)')
#c44.SaveAs("trees/reco_eta_overlay.png")
#c44.Close()

#c45 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_reco1_phi.SetFillColor(kRed)
#h_reco1_phi.Draw()
#h_reco2_phi.SetFillColor(kBlue)
#h_reco2_phi.Draw("same")
#gPad.SetLogy()
#h_reco1_phi.SetMinimum(1)
#h_reco1_phi.SetTitle('#phi of first reco muon (red) and second muon (blue)')
#c45.SaveAs("trees/reco_phi_overlay.png")
#c45.Close()