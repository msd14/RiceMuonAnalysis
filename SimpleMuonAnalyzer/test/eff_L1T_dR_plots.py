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
#while i<256:
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
phi_bins = [256, -np.pi, np.pi]

h_reco_pt = TH1D('h_reco_pt', '', 70, 0, 350)
h_reco_eta = TH1D('h_reco_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco_phi = TH1D('h_reco_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf_pt = TH1D('h_emtf_pt', '', 70, 0, 350)
h_emtf_eta = TH1D('h_emtf_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf_phi = TH1D('h_emtf_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])


h_dEta_denom = TH1D('h_dEta_denom', '', eta_bins[0], -0.1, 0.1)
h_dPhi_denom = TH1D('h_dPhi_denom', '', phi_bins[0], -0.1, 0.1)
h_dR_denom   = TH1D('h_dR_denom', '', 30, 0, 0.1)

h_dEta_numer = TH1D('h_dEta_numer', '', eta_bins[0], -0.1, 0.1)
h_dPhi_numer = TH1D('h_dPhi_numer', '', phi_bins[0], -0.1, 0.1)
h_dR_numer   = TH1D('h_dR_numer', '', 30, 0, 0.1)

h_reco1_emtf1_dR = TH1D('h_reco1_emtf1', '', 256, 0, 1.2)
h_reco1_emtf2_dR = TH1D('h_reco1_emtf2', '', 256, 0, 1.2)
h_reco1_emtf3_dR = TH1D('h_reco1_emtf3', '', 256, 0, 1.2)
h_reco2_emtf1_dR = TH1D('h_reco2_emtf1', '', 256, 0, 1.2)
h_reco2_emtf2_dR = TH1D('h_reco2_emtf2', '', 256, 0, 1.2)
h_reco2_emtf3_dR = TH1D('h_reco2_emtf3', '', 256, 0, 1.2)
h_reco_emtf_dR  = TH1D('h_reco_emtf', '', 256, 0, 1.2)
h_reco1_emtf_dR = TH1D('h_reco1_emtf', '', 256, 0, 1.2)
h_reco2_emtf_dR = TH1D('h_reco2_emtf', '', 256, 0, 1.2)

h_reco1_besttrk_dR = TH1D('h_reco1_besttrk_dR', '', 256, 0, 1.2)
h_reco2_besttrk_dR = TH1D('h_reco2_besttrk_dR', '', 256, 0, 1.2)
h_reco_besttrk_dR = TH1D('h_reco_besttrk_dR', '', 256, 0, 1.2)
h_reco_either_besttrk_dR = TH1D('h_reco_either_besttrk_dR', '', 256, 0, 1.2)

h_invMass = TH1D('h_invMass', '', 256, 0, 150)

none_count       = 0
med_count        = 0
pT_count         = 0
EMTFmatch_count  = 0

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

  #if h.CalcDR(evt_tree.reco_eta[0], evt_tree.reco_eta[1], dPhiNorm) > 0.1: continue

  if (evt_tree.reco_eta[0] < -90 or evt_tree.reco_eta[0] < -90): continue
  if (evt_tree.reco_eta[1] < -90 or evt_tree.reco_phi[1] < -90): continue

  #Ignore events with offline reco muons near the sector boundries, due to duplicate tracks. (15, 75, 135, 195, 255, 315 degrees)
  check=0
  i=0
  while i<len(sector_boundries_fixed):
    if abs(evt_tree.reco_phi[0]-sector_boundries_fixed[i]) < 0.0872665: check+=1
    if abs(evt_tree.reco_phi[1]-sector_boundries_fixed[i]) < 0.0872665: check+=1
    i+=1
  if check!=0: continue

  none_count+=1 

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

  best1=0
  best2=0

  j=0
  while j<len(evt_tree.emtf_pt):
    if (reco_phi[0] - evt_tree.emtf_phi[j]) > 3.14:  dPhiNorm2 = (reco_phi[0] - evt_tree.emtf_phi[j]) - (2*3.14)
    if (reco_phi[0] - evt_tree.emtf_phi[j]) < -3.14: dPhiNorm2 = (reco_phi[0] - evt_tree.emtf_phi[j]) + (2*3.14)
    if (reco_phi[0] - evt_tree.emtf_phi[j]) <= 3.14 and (evt_tree.reco_phi[0] - evt_tree.emtf_phi[j]) >= -3.14: dPhiNorm2 = (reco_phi[0] - evt_tree.emtf_phi[j])

    if (reco_phi[1] - evt_tree.emtf_phi[j]) > 3.14:  dPhiNorm3 = (reco_phi[1] - evt_tree.emtf_phi[j]) - (2*3.14)
    if (reco_phi[1] - evt_tree.emtf_phi[j]) < -3.14: dPhiNorm3 = (reco_phi[1] - evt_tree.emtf_phi[j]) + (2*3.14)
    if (reco_phi[1] - evt_tree.emtf_phi[j]) <= 3.14 and (reco_phi[1] - evt_tree.emtf_phi[j]) >= -3.14: dPhiNorm3 = (reco_phi[1] - evt_tree.emtf_phi[j])

    if j==0: 
      h_reco1_emtf1_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf1_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))

      best1=h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2)
      best2=h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3)


    if j==1 and abs(evt_tree.emtf_eta[1] - evt_tree.emtf_eta[0])>0.2 and abs(evt_tree.emtf_phi[1] - evt_tree.emtf_phi[0])>0.2:
      h_reco1_emtf2_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf2_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))

      if h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2) < best1: best1 = h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2)
      if h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3) < best2: best2 = h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3)

    if j==2 and abs(evt_tree.emtf_eta[2] - evt_tree.emtf_eta[0])>0.2 and abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[0])>0.2 and (abs(evt_tree.emtf_eta[2] - evt_tree.emtf_eta[1])>0.2) and (abs(evt_tree.emtf_phi[2] - evt_tree.emtf_phi[1])>0.2):
      h_reco1_emtf3_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf3_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))
      h_reco1_emtf_dR.Fill(h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2))
      h_reco2_emtf_dR.Fill(h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3))

      if h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2) < best1: best1 = h.CalcDR(reco_eta[0], evt_tree.emtf_eta[j], dPhiNorm2)
      if h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3) < best2: best2 = h.CalcDR(reco_eta[1], evt_tree.emtf_eta[j], dPhiNorm3)

    j+=1

  h_reco1_besttrk_dR.Fill(best1)
  h_reco2_besttrk_dR.Fill(best2)
  h_reco_besttrk_dR.Fill(best1)
  h_reco_besttrk_dR.Fill(best2)
  
  if best1 < best2: h_reco_either_besttrk_dR.Fill(best1)
  if best2 < best1: h_reco_either_besttrk_dR.Fill(best2)

  
  v1 = TLorentzVector()
  v2 = TLorentzVector()
  v1.SetPtEtaPhiM(reco_pT[0], reco_eta[0], reco_phi[0], 0.105)
  v2.SetPtEtaPhiM(reco_pT[1], reco_eta[1], reco_phi[1], 0.105)

  invMass = (v1+v2).M()
  h_invMass.Fill(invMass)

  ##Apply ID and pT > 26 GeV selection on tag muon.
  #if evt_tree.reco_isMediumMuon[0] != 1 or evt_tree.reco_isMediumMuon[1] != 1: continue
  #med_count+=1

  #if evt_tree.reco_pt[0] < 26 or evt_tree.reco_pt[1] < 26: continue
  #pT_count+=1

  #tagPt = evt_tree.reco_pt[0]
  #tagEta = evt_tree.reco_eta[0]
  #tagPhi = evt_tree.reco_phi[0]
  #tagCharge = evt_tree.reco_charge[0]

  #probePt = evt_tree.reco_pt[1]
  #probeEta = evt_tree.reco_eta[1]
  #probePhi = evt_tree.reco_phi[1]
  #probeCharge = evt_tree.reco_charge[1]

  ##Define dEta, dPhi between tag and probe
  #dEta = probeEta - tagEta
  #dPhi = probePhi - tagPhi

  ##Normalize dPhi from -pi to pi
  #if dPhi > 3.14:  dPhiNorm = dPhi - (2*3.14)
  #if dPhi < -3.14: dPhiNorm = dPhi + (2*3.14)
  #if dPhi <= 3.14 and dPhi >= -3.14: dPhiNorm = dPhi

  ##Define dR between tag and probe
  #dR = h.CalcDR(probeEta, tagEta, dPhiNorm)

  ##Fill denominator distributions
  #h_dEta_denom.Fill(dEta)
  #h_dPhi_denom.Fill(dPhiNorm)
  #h_dR_denom.Fill(dR)

  #i=0
  #while i<len(evt_tree.reco_phi):
    #h_reco_pt.Fill(evt_tree.reco_pt[i])
    #h_reco_eta.Fill(evt_tree.reco_eta[i])
    #h_reco_phi.Fill(evt_tree.reco_phi[i])
    #i+=1

  #i=0
  #while i<len(evt_tree.emtf_phi): 
    #h_emtf_pt.Fill(evt_tree.emtf_pt[i])
    #h_emtf_eta.Fill(evt_tree.emtf_eta[i])
    #h_emtf_phi.Fill(evt_tree.emtf_phi[i])
    #i+=1

	
  ##Require at least one muon be EMTF matched
  #if evt_tree.reco_hasEMTFMatch[0] != 1 and evt_tree.reco_hasEMTFMatch[1] != 1: continue
  #EMTFmatch_count+=1

  ##Fill numerator distributions
  #h_dEta_numer.Fill(dEta)
  #h_dPhi_numer.Fill(dPhiNorm)
  #h_dR_numer.Fill(dR)




#Printouts
#print '-------------'
#print 'nMuons after selections:'
#print 'pre-selections only:', none_count
#print 'both reco muons are medium ID:', med_count
#print 'both reco muons pT > 26 GeV:', pT_count
#print 'at least one muon is EMTF matched:', EMTFmatch_count
#print '-------------'

    
############################################################
### Write output file with histograms and efficiencies ###
############################################################

c26 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco_emtf_dR.SetMinimum(1)
h_reco_emtf_dR.Draw()
h_reco_emtf_dR.SetTitle('All offline reco muons and all Emtf tracks #Delta R')
h_reco_emtf_dR.GetXaxis().SetTitle('#Delta R')
h_reco_emtf_dR.Write()
c26.SaveAs("tests2/reco_emtf_dR.png")
c26.Close()

c27 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco1_emtf1_dR.SetMinimum(1)
h_reco1_emtf1_dR.Draw()
h_reco1_emtf1_dR.SetTitle('first offline reco muon and first Emtf track #Delta R')
h_reco1_emtf1_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_emtf1_dR.Write()
c27.SaveAs("tests2/reco1_emtf1_dR.png")
c27.Close()

c28 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco1_emtf2_dR.SetMinimum(1)
h_reco1_emtf2_dR.Draw()
h_reco1_emtf2_dR.SetTitle('first offline reco muon and second Emtf track #Delta R')
h_reco1_emtf2_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_emtf2_dR.Write()
c28.SaveAs("tests2/reco1_emtf2_dR.png")
c28.Close()

c29 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco1_emtf3_dR.SetMinimum(1)
h_reco1_emtf3_dR.Draw()
h_reco1_emtf3_dR.SetTitle('first offline reco muon and third Emtf track #Delta R')
h_reco1_emtf3_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_emtf3_dR.Write()
c29.SaveAs("tests2/reco1_emtf3_dR.png")
c29.Close()

c35 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco2_emtf1_dR.SetMinimum(1)
h_reco2_emtf1_dR.Draw()
h_reco2_emtf1_dR.SetTitle('second offline reco muon and first Emtf track #Delta R')
h_reco2_emtf1_dR.GetXaxis().SetTitle('#Delta R')
h_reco2_emtf1_dR.Write()
c35.SaveAs("tests2/reco2_emtf1_dR.png")
c35.Close()

c36 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco2_emtf2_dR.SetMinimum(1)
h_reco2_emtf2_dR.Draw()
h_reco2_emtf2_dR.SetTitle('second offline reco muon and second Emtf track #Delta R')
h_reco2_emtf2_dR.GetXaxis().SetTitle('#Delta R')
h_reco2_emtf2_dR.Write()
c36.SaveAs("tests2/reco2_emtf2_dR.png")
c36.Close()

c37 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco2_emtf3_dR.SetMinimum(1)
h_reco2_emtf3_dR.Draw()
h_reco2_emtf3_dR.SetTitle('second offline reco muon and third Emtf track #Delta R')
h_reco2_emtf3_dR.GetXaxis().SetTitle('#Delta R')
h_reco2_emtf3_dR.Write()
c37.SaveAs("tests2/reco2_emtf3_dR.png")
c37.Close()


c48 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco1_emtf_dR.SetMinimum(1)
h_reco1_emtf_dR.Draw()
h_reco1_emtf_dR.SetTitle('#Delta R of First reco muon with all Emtf tracks')
h_reco1_emtf_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_emtf_dR.Write()
c48.SaveAs("tests2/reco1_emtf_dR.png")
c48.Close()

c49 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco2_emtf_dR.SetMinimum(1)
h_reco2_emtf_dR.Draw()
h_reco2_emtf_dR.SetTitle('#Delta R of second reco muon with all Emtf tracks')
h_reco2_emtf_dR.GetXaxis().SetTitle('#Delta R')
h_reco2_emtf_dR.Write()
c49.SaveAs("tests2/reco2_emtf_dR.png")
c49.Close()

c50 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
h_reco1_emtf_dR.SetFillColor(kRed)
h_reco1_emtf_dR.Draw()
h_reco2_emtf_dR.SetFillColor(kBlue)
h_reco2_emtf_dR.Draw("same")
gPad.SetLogy()
h_reco1_emtf_dR.SetMinimum(1)
h_reco1_emtf_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_emtf_dR.SetTitle('#Delta R of first reco muon with all tracks (red) and second reco muon with all tracks (blue)')
c50.SaveAs("tests2/reco_emtf_dR_overlay.png")
c50.Close()

c51 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco1_besttrk_dR.SetMinimum(1)
h_reco1_besttrk_dR.Draw()
h_reco1_besttrk_dR.SetTitle('#Delta R of first reco muon with closest Emtf track')
h_reco1_besttrk_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_besttrk_dR.Write()
c51.SaveAs("tests2/reco1_emtf_best_dR.png")
c51.Close()

c52 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco2_besttrk_dR.SetMinimum(1)
h_reco2_besttrk_dR.Draw()
h_reco2_besttrk_dR.SetTitle('#Delta R of second reco muon with closest Emtf track')
h_reco2_besttrk_dR.GetXaxis().SetTitle('#Delta R')
h_reco2_besttrk_dR.Write()
c52.SaveAs("tests2/reco2_emtf_best_dR.png")
c52.Close()

c53 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco_besttrk_dR.SetMinimum(1)
h_reco_besttrk_dR.Draw()
h_reco_besttrk_dR.SetTitle('#Delta R of both reco muons with their respective closest Emtf tracks')
h_reco_besttrk_dR.GetXaxis().SetTitle('#Delta R')
h_reco_besttrk_dR.Write()
c53.SaveAs("tests2/reco_emtf_best_dR.png")
c53.Close()


c54 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_reco_either_besttrk_dR.SetMinimum(1)
h_reco_either_besttrk_dR.Draw()
h_reco_either_besttrk_dR.SetTitle('#Delta R of the closest muon-Emtf track in the event')
h_reco_either_besttrk_dR.GetXaxis().SetTitle('#Delta R')
h_reco_either_besttrk_dR.Write()
c54.SaveAs("tests2/reco_emtf_either_best_dR.png")
c54.Close()

c55 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
h_reco1_besttrk_dR.SetFillColor(kRed)
h_reco1_besttrk_dR.Draw()
h_reco2_besttrk_dR.SetFillColor(kBlue)
h_reco2_besttrk_dR.Draw("same")
gPad.SetLogy()
h_reco1_besttrk_dR.SetMinimum(1)
h_reco1_besttrk_dR.GetXaxis().SetTitle('#Delta R')
h_reco1_besttrk_dR.SetTitle('#Delta R of first reco muon with its closest Emtf track (red) and second reco muon with its closest Emtf track (blue)')
c55.SaveAs("tests2/h_reco_besttrk_dR_overlay.png")
c55.Close()

c56 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_invMass.SetMinimum(1)
h_invMass.Draw()
h_invMass.SetTitle('Invariant Mass of both Offline Reco Muons')
h_invMass.GetXaxis().SetTitle('Inv Mass (GeV)')
h_invMass.Write()
c56.SaveAs("tests2/invMass.png")
c56.Close()

#-----------------------------------------


#c15 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_pt.SetMinimum(1)
#h_reco_pt.Draw()
#h_reco_pt.SetTitle('reco muon pT')
#h_reco_pt.Write()
#c15.SaveAs("tests_new/reco_pt.png")
#c15.Close()

#c16 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_eta.SetMinimum(1)
#h_reco_eta.Draw()
#h_reco_eta.SetTitle('reco muon #eta')
#h_reco_eta.Write()
#c16.SaveAs("tests_new/reco_eta.png")
#c16.Close()

#c17 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_phi.SetMinimum(1)
#h_reco_phi.Draw()
#h_reco_phi.SetTitle('reco muon #phi')
#h_reco_phi.Write()
#c17.SaveAs("tests_new/reco_phi.png")
#c17.Close()

#c18 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf_pt.SetMinimum(1)
#h_emtf_pt.Draw()
#h_emtf_pt.SetTitle('emtf muon pT')
#h_emtf_pt.Write()
#c18.SaveAs("tests_new/emtf_pt.png")
#c18.Close()

#c19 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf_eta.SetMinimum(1)
#h_emtf_eta.Draw()
#h_emtf_eta.SetTitle('emtf muon #eta')
#h_emtf_eta.Write()
#c19.SaveAs("tests_new/emtf_eta.png")
#c19.Close()

#c20 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf_phi.SetMinimum(1)
#h_emtf_phi.Draw()
#h_emtf_phi.SetTitle('emtf muon #phi')
#h_emtf_phi.Write()
#c20.SaveAs("tests_new/emtf_phi.png")
#c20.Close()

#c21 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#stack = THStack("stack", "")
#h_emtf_pt.SetFillColor(kBlue)
#stack.Add(h_emtf_pt)
#h_reco_pt.SetFillColor(kRed)
#stack.Add(h_reco_pt)
#gPad.SetLogy()
#stack.SetMinimum(1)
#stack.Draw()
#stack.SetTitle('reco (red) and emtf (blue) muon pT')
#c21.SaveAs("tests_new/reco_emtf_pt.png")
#c21.Close()

#c22 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#stack = THStack("stack", "")
#h_reco_eta.SetFillColor(kRed)
#stack.Add(h_reco_eta)
#h_emtf_eta.SetFillColor(kBlue)
#stack.Add(h_emtf_eta)
#gPad.SetLogy()
#stack.SetMinimum(1)
#stack.Draw()
#stack.SetTitle('reco (red) and emtf (blue) muon #eta')
#c22.SaveAs("tests_new/reco_emtf_eta.png")
#c22.Close()

#c23 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#stack = THStack("stack", "")
#h_reco_phi.SetFillColor(kRed)
#stack.Add(h_reco_phi)
#h_emtf_phi.SetFillColor(kBlue)
#stack.Add(h_emtf_phi)
#gPad.SetLogy()
#stack.SetMinimum(1)
#stack.Draw()
#stack.SetTitle('reco (red) and emtf (blue) muon #phi')
#c23.SaveAs("tests_new/reco_emtf_phi.png")
#c23.Close()

#c24 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dEta_denom.SetMinimum(1)
#h_dEta_denom.Draw()
#h_dEta_denom.SetTitle('tag-probe #Delta #eta')
#h_dEta_denom.Write()
#c24.SaveAs("tests_new/dEta_denom.png")
#c24.Close()

#c25 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_denom.SetMinimum(1)
#h_dPhi_denom.Draw()
#h_dPhi_denom.SetTitle('tag-probe #Delta #phi')
#h_dPhi_denom.Write()
#c25.SaveAs("tests_new/dPhi_denom.png")
#c25.Close()

#c26 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dR_denom.SetMinimum(1)
#h_dR_denom.Draw()
#h_dR_denom.SetTitle('tag-probe #Delta R')
#h_dR_denom.Write()
#c26.SaveAs("tests_new/dR_denom.png")
#c26.Close()


#--------------------------------------

#c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#c1.SetGrid()
#eff = TEfficiency(h_dEta_numer, h_dEta_denom)
#eff.Draw()
#eff.SetTitle('Trigger Efficiency vs #Delta #eta')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#gPad.Update()
#eff.Write()
#c1.SaveAs("tests_new/dEta_eff.png")
#c1.Close()

#c2 = TCanvas( 'c2', 'test scatter', 200, 10, 700, 500)
#c2.SetGrid()
#eff = TEfficiency(h_dPhi_numer, h_dPhi_denom)
#eff.Draw()
#eff.SetTitle('Trigger Efficiency vs #Delta #phi')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#gPad.Update()
#eff.Write()
#c2.SaveAs("tests_new/dPhi_eff.png")
#c2.Close()

#c3 = TCanvas( 'c3', 'test scatter', 200, 10, 700, 500)
#c3.SetGrid()
#eff = TEfficiency(h_dR_numer, h_dR_denom)
#eff.Draw()
#eff.SetTitle('Trigger Efficiency vs #Delta R')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#gPad.Update()
#eff.Write()
#c3.SaveAs("tests_new/dR_eff.png")
#c3.Close()


#--------------------------------------------
#Kinematic distributions for emtf-matched and unmatched events

#c4 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#c4.SetGrid()
#stack = THStack("stack", "")
#h_tagpT_noMatch.SetFillColor(kRed)
#stack.Add(h_tagpT_noMatch)
#h_tagpT_match.SetFillColor(kBlue)
#stack.Add(h_tagpT_match)
#scale = 1./h_tagpT_noMatch.Integral()
#scale2 = 1./h_tagpT_match.Integral()
#h_tagpT_noMatch.Scale(scale)
#h_tagpT_match.Scale(scale2)
#stack.Draw()
#c4.SaveAs("tests_new/pT_tag_compare.png")
#c4.Close()

#c4 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#c4.SetGrid()
#stack = THStack("stack", "")
#h_tagpT_noMatch.SetFillColor(kRed)
#stack.Add(h_tagpT_noMatch)
#h_tagpT_match.SetFillColor(kBlue)
#stack.Add(h_tagpT_match)
#stack.Draw()
#c4.SaveAs("tests_new/pT_tag_compare.png")
#c4.Close()

#c5 = TCanvas( 'c5', 'test scatter', 200, 10, 700, 500)
#c5.SetGrid()
#stack = THStack("stack", "")
#h_probepT_noMatch.SetFillColor(kRed)
#stack.Add(h_probepT_noMatch)
#h_probepT_match.SetFillColor(kBlue)
#stack.Add(h_probepT_match)
#stack.Draw()
#c5.SaveAs("tests_new/pT_probe_compare.png")
#c5.Close()

#c6 = TCanvas( 'c6', 'test scatter', 200, 10, 700, 500)
#c6.SetGrid()
#stack = THStack("stack", "")
#h_tagEta_noMatch.SetFillColor(kRed)
#stack.Add(h_tagEta_noMatch)
#h_tagEta_match.SetFillColor(kBlue)
#stack.Add(h_tagEta_match)
#stack.Draw()
#c6.SaveAs("tests_new/Eta_tag_compare.png")
#c6.Close()

#c7 = TCanvas( 'c7', 'test scatter', 200, 10, 700, 500)
#c7.SetGrid()
#stack = THStack("stack", "")
#h_probeEta_noMatch.SetFillColor(kRed)
#stack.Add(h_probeEta_noMatch)
#h_probeEta_match.SetFillColor(kBlue)
#stack.Add(h_probeEta_match)
#stack.Draw()
#c7.SaveAs("tests_new/Eta_probe_compare.png")
#c7.Close()

#c8 = TCanvas( 'c8', 'test scatter', 200, 10, 700, 500)
#c8.SetGrid()
#stack = THStack("stack", "")
#h_tagPhi_noMatch.SetFillColor(kRed)
#stack.Add(h_tagPhi_noMatch)
#h_tagPhi_match.SetFillColor(kBlue)
#stack.Add(h_tagPhi_match)
#stack.Draw()
#c8.SaveAs("tests_new/Phi_tag_compare.png")
#c8.Close()

#c9 = TCanvas( 'c9', 'test scatter', 200, 10, 700, 500)
#c9.SetGrid()
#stack = THStack("stack", "")
#h_probePhi_noMatch.SetFillColor(kRed)
#stack.Add(h_probePhi_noMatch)
#h_probePhi_match.SetFillColor(kBlue)
#stack.Add(h_probePhi_match)
#stack.Draw()
#c9.SaveAs("tests_new/Phi_probe_compare.png")
#c9.Close()

#c10 = TCanvas( 'c10', 'test scatter', 200, 10, 700, 500)
#c10.SetGrid()
#stack = THStack("stack", "")
#h_dEta_noMatch.SetFillColor(kRed)
#stack.Add(h_dEta_noMatch)
#h_dEta_match.SetFillColor(kBlue)
#stack.Add(h_dEta_match)
#stack.Draw()
#c10.SaveAs("tests_new/dEta_compare.png")
#c10.Close()

#c11 = TCanvas( 'c11', 'test scatter', 200, 10, 700, 500)
#c11.SetGrid()
#stack = THStack("stack", "")
#h_dPhi_noMatch.SetFillColor(kRed)
#stack.Add(h_dPhi_noMatch)
#h_dPhi_match.SetFillColor(kBlue)
#stack.Add(h_dPhi_match)
#stack.Draw()
#c11.SaveAs("tests_new/dPhi_compare.png")
#c11.Close()

#c12 = TCanvas( 'c12', 'test scatter', 200, 10, 700, 500)
#c12.SetGrid()
#stack = THStack("stack", "")
#h_dR_noMatch.SetFillColor(kRed)
#stack.Add(h_dR_noMatch)
#h_dR_match.SetFillColor(kBlue)
#stack.Add(h_dR_match)
#stack.Draw()
#c12.SaveAs("tests_new/dR_compare.png")
#c12.Close()

