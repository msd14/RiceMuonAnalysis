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

dir1 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018A-17Sep2018-v2_AOD/191121_192542/0000/Ntuples/'
dir2 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018B-17Sep2018-v1_AOD/191128_175215/0000/Ntuples/'
dir3 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018C-17Sep2018-v1_AOD/191121_191920/0000/Ntuples/'
dir4 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/CRAB3_Analysis_SingleMuon_Run2018D-PromptReco-v2_AOD/191121_192704/0000/Ntuples/'
run_str = '_2018D'


## Load input files
i = 1
while  i<200:  #555
    file_name = dir1+"L1Ntuple_"+str(i)+".root"
    #These files did not Ntuplize properly.
    if i==12 or i==20 or i==31 or i==37 or i==41 or i==47 or i==52 or i==57 or i==74 or i==81 or i==84 or i==93 or i==140 or i==173 or i==181 or i==229 or i==257 or i==297 or i==311: 
      i+=1
      continue
    print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    evt_tree.Add(file_name)
    i+=1

#i = 1
#while i<263:   #263
    #file_name = dir2+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

#i = 1
#while i<263:   #263
    #file_name = dir3+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

#i = 1
#while i<1249:   #1249
    #file_name = dir4+"L1Ntuple_"+str(i)+".root"
    #print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    #evt_tree.Add(file_name)
    #i+=1

## ================ Histograms ======================

h_Nemtf = TH1D('h_Nemtf', '', 4, 0, 4)

h_reco_pt = TH1D('h_reco_pt', '', 256, 0, 1000)
h_reco1_pt = TH1F('','', 256, 0, 1000)
h_reco2_pt = TH1F('h_reco2_pt', '', 256, 0, 250)
h_reco_eta = TH1D('h_reco_eta', '', 256, -2.8, 2.8)
h_reco1_eta = TH1D('h_reco1_eta', '', 256, -2.8, 2.8)
h_reco2_eta = TH1D('h_reco2_eta', '', 256, -2.8, 2.8)
h_reco_phi = TH1D('h_reco_phi', '', 256, -np.pi, np.pi)
h_reco1_phi = TH1D('h_reco1_phi', '', 256, -np.pi, np.pi)
h_reco2_phi = TH1D('h_reco2_phi', '', 256, -np.pi, np.pi)

h_emtf_pt = TH1D('h_emtf_pt', '', 256, 0, 256)
h_emtf_eta = TH1D('h_emtf_eta', '', 256, -2.8, 2.8)
h_emtf_phi = TH1D('h_emtf_phi', '', 256, -180, 180)
h_emtf1_phi = TH1D('h_emtf1_phi', '', 256, -np.pi, np.pi)
h_emtf2_phi = TH1D('h_emtf2_phi', '', 256, -180, 180)
h_emtf3_phi = TH1D('h_emtf3_phi', '', 256, -np.pi, np.pi)

h_dPhi_1trk_numer = TH1D('h_dPhi_1trk_numer', '', 32, -0.3, 0.3)
h_dPhi_2trk_numer = TH1D('h_dPhi_2trk_numer', '', 32, -0.3, 0.3)
h_dPhi_1trk_denom = TH1D('h_dPhi_1trk_denom', '', 32, -0.3, 0.3)
h_dPhi_2trk_denom = TH1D('h_dPhi_2trk_denom', '', 32, -0.3, 0.3)

h_dEta_denom = TH1D('h_dEta_denom', '', 32, -0.1, 0.1)
h_dPhi_denom = TH1D('h_dPhi_denom', '', 32, -0.1, 0.1)
h_dR_denom   = TH1D('h_dR_denom', '', 32, 0, 0.1)

h_dEta_numer = TH1D('h_dEta_numer', '', 32, -0.1, 0.1)
h_dPhi_numer = TH1D('h_dPhi_numer', '', 32, -0.1, 0.1)
h_dR_numer   = TH1D('h_dR_numer', '', 32, 0, 0.1)

#h_dR_1_numer   = TH1D('h_dR_1_numer', '', 64, 0, 0.1)
#h_dR_09_numer   = TH1D('h_dR_09_numer', '', 64, 0, 0.1)
#h_dR_08_numer   = TH1D('h_dR_08_numer', '', 64, 0, 0.1)
#h_dR_07_numer   = TH1D('h_dR_07_numer', '', 64, 0, 0.1)

#h_reco_phi = TH1D('h_reco_phi', '', 256, -np.pi, np.pi)
#h_emtf_phi = TH1D('h_emtf_phi', '', 256, 0, 360)

h_reco1_besttrk_dR = TH1D('h_reco1_besttrk_dR', '', 128, 0, 0.2)
h_reco2_besttrk_dR = TH1D('h_reco2_besttrk_dR', '', 128, 0, 0.2)
h_reco_besttrk_dR = TH1D('h_reco_besttrk_dR', '', 128, 0, 0.2)

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

  #Default values in ntuples are -99, so get rid of any event not defined correctly.
  if (evt_tree.reco_eta[0] < -90 or evt_tree.reco_eta[0] < -90): continue
  if (evt_tree.reco_eta[1] < -90 or evt_tree.reco_phi[1] < -90): continue

  #We will need two distinct Emtf tracks to match to offline muons, so if the event has less than two tracks, skip the event.
  #if len(evt_tree.emtf_pt)<2: continue

  #Order the offline reco muons, leading and subleading.
  reco_pT = [] #First muon = leading, second muon = subleading
  reco_eta = []
  reco_eta_prop = []
  reco_phi = []
  reco_phi_prop = []

  reco_phi_prop_deg = []

  if evt_tree.reco_pt[0] > evt_tree.reco_pt[1]: 
    reco_pT.append(evt_tree.reco_pt[0])
    reco_pT.append(evt_tree.reco_pt[1])
    reco_eta.append(evt_tree.reco_eta[0])
    reco_eta.append(evt_tree.reco_eta[1])
    reco_eta_prop.append(evt_tree.reco_eta_prop[0])
    reco_eta_prop.append(evt_tree.reco_eta_prop[1])
    reco_phi_prop.append(evt_tree.reco_phi_prop[0])
    reco_phi_prop.append(evt_tree.reco_phi_prop[1])
    reco_phi.append(evt_tree.reco_phi[0])
    reco_phi.append(evt_tree.reco_phi[1])
  if evt_tree.reco_pt[0] < evt_tree.reco_pt[1]:
    reco_pT.append(evt_tree.reco_pt[1])
    reco_pT.append(evt_tree.reco_pt[0])
    reco_eta.append(evt_tree.reco_eta[1])
    reco_eta.append(evt_tree.reco_eta[0])
    reco_eta_prop.append(evt_tree.reco_eta_prop[1])
    reco_eta_prop.append(evt_tree.reco_eta_prop[0])
    reco_phi_prop.append(evt_tree.reco_phi_prop[1])
    reco_phi_prop.append(evt_tree.reco_phi_prop[0])
    reco_phi.append(evt_tree.reco_phi[1])
    reco_phi.append(evt_tree.reco_phi[0])

  if evt_tree.reco_pt[0] == evt_tree.reco_pt[1]: continue

  #Fill reco histograms.
  h_reco1_pt.Fill(reco_pT[0])
  h_reco2_pt.Fill(reco_pT[1])
  h_reco1_eta.Fill(reco_eta[0])
  h_reco2_eta.Fill(reco_eta[1])
  h_reco1_phi.Fill(reco_phi[0])
  h_reco2_phi.Fill(reco_phi[1])
  j=0
  while j<len(evt_tree.reco_pt):
    h_reco_pt.Fill(reco_pT[j])
    h_reco_eta.Fill(reco_eta[j])
    h_reco_phi.Fill(reco_phi[j])
    j+=1

  j=0
  while j<len(reco_phi_prop):
    if reco_phi_prop[j]>0: reco_phi_prop_deg.append(reco_phi_prop[j]*180/np.pi)
    if reco_phi_prop[j]<=0: reco_phi_prop_deg.append(reco_phi_prop[j]*180/np.pi)
   
    j+=1


  #Fill Emtf quantities and some histograms.
  #Unlike the offline muons, we do not order the tracks by pT.
  emtf_pT = []
  emtf_eta = []
  emtf_phi = []
  emtf_phi_deg = []

  if len(evt_tree.emtf_phi)>0:
    emtf_pT.append(evt_tree.emtf_pt[0])
    emtf_eta.append(evt_tree.emtf_eta[0])
    emtf_phi.append(evt_tree.emtf_phi[0])
    h_emtf1_phi.Fill(evt_tree.emtf_phi[0])

 

  #There may still be some duplicate tracks in the event, so double check that there aren't.
  if len(evt_tree.emtf_phi)>1:
    #if abs(emtf_phi[0]-evt_tree.emtf_phi[1])>0.005: 
    emtf_pT.append(evt_tree.emtf_pt[1])
    emtf_eta.append(evt_tree.emtf_eta[1])
    emtf_phi.append(evt_tree.emtf_phi[1])

    if evt_tree.emtf_phi[1]>0: h_emtf2_phi.Fill(evt_tree.emtf_phi[1]*180/np.pi)
    if evt_tree.emtf_phi[1]<=0: h_emtf2_phi.Fill(evt_tree.emtf_phi[1]*180/np.pi)

  if len(emtf_phi)==2 and len(evt_tree.emtf_phi)>2:
    #if abs(emtf_phi[0]-evt_tree.emtf_phi[2])>0.005 and abs(emtf_phi[1]-evt_tree.emtf_phi[2])>0.005:
    emtf_pT.append(evt_tree.emtf_pt[2])
    emtf_eta.append(evt_tree.emtf_eta[2])
    emtf_phi.append(evt_tree.emtf_phi[2])
    h_emtf3_phi.Fill(evt_tree.emtf_phi[2])


  #After removing duplicates, check again that there are at least two distinct Emtf tracks in the event.
  #if len(emtf_phi)<2: continue


  h_Nemtf.Fill(len(emtf_pT))

  #Fill Emtf histograms, now that all duplicate tracks should be removed.
  j=0
  while j<len(emtf_pT):
    if evt_tree.emtf_phi[j]>0: emtf_phi_deg.append(emtf_phi[j]*180./np.pi)
    if evt_tree.emtf_phi[j]<=0: emtf_phi_deg.append(emtf_phi[j]*180./np.pi)

    h_emtf_pt.Fill(emtf_pT[j])
    h_emtf_eta.Fill(emtf_eta[j])
    h_emtf_phi.Fill(emtf_phi_deg[j])
    
    j+=1

  
  #Match offline reco muons to their closest track.
  #First, calculate the dR for the first offline muon and the Emtf tracks and pick the closest one.
  #Then calculate dR for the second offline muon and the tracks and pick the best one.
  #Double check that you don't assign the same track to both muons.
  best1=0
  best2=0
  best1_backup=0
  best2_backup=0

  j=0
  b1_index=-1
  while j<len(emtf_phi):
    if (reco_phi_prop[0] - emtf_phi[j]) > 3.14:  dPhiNorm = (reco_phi_prop[0] - emtf_phi[j]) - (2*3.14)
    if (reco_phi_prop[0] - emtf_phi[j]) < -3.14: dPhiNorm = (reco_phi_prop[0] - emtf_phi[j]) + (2*3.14)
    if (reco_phi_prop[0] - emtf_phi[j]) <= 3.14 and (reco_phi_prop[0] - emtf_phi[j]) >= -3.14: dPhiNorm = (reco_phi_prop[0] - emtf_phi[j])

    if j==0: best1 = h.CalcDR(reco_eta[0], emtf_eta[j], dPhiNorm)
    if j==1: 
      if h.CalcDR(reco_eta_prop[0], emtf_eta[j], dPhiNorm) < best1:
	best1_backup = best1
	best1 = h.CalcDR(reco_eta_prop[0], emtf_eta[j], dPhiNorm)
	b1_index=1
      if h.CalcDR(reco_eta_prop[0], emtf_eta[j], dPhiNorm) > best1:
	b1_index=0
	best1_backup = h.CalcDR(reco_eta_prop[0], emtf_eta[j], dPhiNorm)
    j+=1


  #Use the propagated phi to match to Emtf tracks. (First, renorm from -pi to pi, then calc dR)

  j=0
  b2_index=-1
  while j<len(emtf_phi):
    if (reco_phi_prop[1] - emtf_phi[j]) > 3.14:  dPhiNorm = (reco_phi_prop[1] - emtf_phi[j]) - (2*3.14)
    if (reco_phi_prop[1] - emtf_phi[j]) < -3.14: dPhiNorm = (reco_phi_prop[1] - emtf_phi[j]) + (2*3.14)
    if (reco_phi_prop[1] - emtf_phi[j]) <= 3.14 and (reco_phi_prop[1] - emtf_phi[j]) >= -3.14: dPhiNorm = (reco_phi_prop[1] - emtf_phi[j])

    if j==0: best2 = h.CalcDR(reco_eta_prop[1], emtf_eta[j], dPhiNorm)
    if j==1: 
      if h.CalcDR(reco_eta_prop[1], emtf_eta[j], dPhiNorm) < best2:
	best2_backup = best2
	best2 = h.CalcDR(reco_eta_prop[1], emtf_eta[j], dPhiNorm)
	b2_index=1
      if h.CalcDR(reco_eta_prop[1], emtf_eta[j], dPhiNorm) > best2:
	b2_index=0
	best2_backup = h.CalcDR(reco_eta_prop[1], emtf_eta[j], dPhiNorm)

    j+=1


  #If the two reco muons match to the same track, use the better match and then set the worse match to its backup track.

  if len(emtf_pT)==1:
    if best1>best2:
      h_reco2_besttrk_dR.Fill(best2)
      h_reco_besttrk_dR.Fill(best2)
    if best2>best1:
      h_reco1_besttrk_dR.Fill(best1)
      h_reco_besttrk_dR.Fill(best1)

  if len(emtf_pT)==2:
    if b1_index==b2_index:
      if best1>best2: best1=best1_backup
      if best2>best1: best2=best2_backup

      h_reco1_besttrk_dR.Fill(best1)
      h_reco2_besttrk_dR.Fill(best2)
      h_reco_besttrk_dR.Fill(best1)
      h_reco_besttrk_dR.Fill(best2)

  none_count+=1

  #if len(emtf_pT)==1:
    #print '1 track event:'
    #print "reco muon 1 pT, eta, phi: ", reco_pT[0], reco_eta[0], reco_phi[0]
    #print "reco muon 2 pT, eta, phi: ", reco_pT[1], reco_eta[1], reco_phi[1]
    #print "emtf track pT, eta, phi: ",emtf_pT[0], emtf_eta[0], emtf_phi[0]
    #if best1>best2: print "this track matches to muon 2"
    #if best2>best1: print "this track matches to muon 1"
    #print '---------------------------------------------'

  

  if len(emtf_pT)==2:
    print '2 Emtf tracks in the event:'
    print "offline muon 1 pT, eta, phi (propagated): ", reco_pT[0], reco_eta_prop[0], reco_phi_prop_deg[0]
    print "offline muon 2 pT, eta, phi (propagated): ", reco_pT[1], reco_eta_prop[1], reco_phi_prop_deg[1]
    print "Emtf track 1 pT, eta, phi: ", emtf_pT[0], emtf_eta[0], emtf_phi_deg[0]
    #if best1>best2: print "this track matches to muon 2" 
    #if best2>best1: print "this track matches to muon 1"
    print "Emtf track 2 pT, eta, phi: ", emtf_pT[1], emtf_eta[1], emtf_phi_deg[1]
    #if best2>best1: print "this track matches to muon 1"
    #if best1>best2: print "this track matches to muon 2"
    print '---------------------------------------------'
    

  #Apply medium selection
  if evt_tree.reco_isMediumMuon[0] != 1 or evt_tree.reco_isMediumMuon[1] != 1: continue 
  med_count+=1

  if len(emtf_pT)==1: h_dPhi_1trk_denom.Fill(reco_phi[0] - reco_phi[1])
  if len(emtf_pT)==2: h_dPhi_2trk_denom.Fill(reco_phi[0] - reco_phi[1])

  #if reco_pT[0] < 20 or reco_pT[1] < 20: continue
  #pT_count+=1

  if (reco_phi[0] - reco_phi[1]) > 3.14:  dPhiNorm = (reco_phi[0] - reco_phi[1]) - (2*3.14)
  if (reco_phi[0] - reco_phi[1]) < -3.14: dPhiNorm = (reco_phi[0] - reco_phi[1]) + (2*3.14)
  if (reco_phi[0] - reco_phi[1]) <= 3.14 and (reco_phi[0] - reco_phi[1]) >= -3.14: dPhiNorm = (reco_phi[0] - reco_phi[1])
  
  h_dEta_denom.Fill(reco_eta[0] - reco_eta[1])
  h_dPhi_denom.Fill(reco_phi[0] - reco_phi[1])
  h_dR_denom.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))

  #if best1<0.1 and best2<0.1: h_dR_1_numer.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))
  #if best1<0.09 and best2<0.09: h_dR_09_numer.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))
  #if best1<0.08 and best2<0.08: h_dR_08_numer.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))
  #if best1<0.07 and best2<0.07: h_dR_07_numer.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))


  if best1>0.1 or best2>0.1 or len(emtf_pT)<2: continue
  EMTFmatch_count+=1


  if len(emtf_pT)==1: h_dPhi_1trk_numer.Fill(reco_phi[0] - reco_phi[1])
  if len(emtf_pT)==2: h_dPhi_2trk_numer.Fill(reco_phi[0] - reco_phi[1])

  h_dEta_numer.Fill(reco_eta[0] - reco_eta[1])
  h_dPhi_numer.Fill(reco_phi[0] - reco_phi[1])
  h_dR_numer.Fill(h.CalcDR(reco_eta[0], reco_eta[1], dPhiNorm))

  h_reco_phi.Fill(reco_phi[0])
  h_reco_phi.Fill(reco_phi[1])

  
  i=0
  while i<len(emtf_phi):
    h_emtf_phi.Fill(emtf_phi[i])
    i+=1

#Printouts
print '-------------'
print 'nMuons after selections:'
print 'pre-selections only:', none_count
print 'both reco muons are medium ID:', med_count
#print 'both reco muons pT > 26 GeV:', pT_count
print 'both muons are EMTF matched:', EMTFmatch_count
print '-------------'

print float(EMTFmatch_count) / float(med_count)

############################################################
### Write output file with histograms and efficiencies ###
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

#c6 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_eta.SetMinimum(1)
#h_reco2_eta.Draw()
#h_reco2_eta.SetTitle('Second offline reco muon #eta')
#h_reco2_eta.GetXaxis().SetTitle('#eta')
#h_reco2_eta.Write()
#c6.SaveAs("trees/reco2_eta.png")
#c6.Close()

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

c8 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf_phi.SetMinimum(1)
h_emtf_phi.Draw()
h_emtf_phi.SetTitle('All EMTF tracks #phi')
h_emtf_phi.GetXaxis().SetTitle('#phi')
h_emtf_phi.Write()
c8.SaveAs("trees/emtf_phi.png")
c8.Close()

#c9 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_Nemtf.SetMinimum(1)
#h_Nemtf.Draw()
#h_Nemtf.SetTitle('Number of Emtf tracks (duplicates removed)')
#h_Nemtf.GetXaxis().SetTitle('#phi')
#h_Nemtf.Write()
#c9.SaveAs("trees/N_Emtf.png")
#c9.Close()

#c21 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf1_phi.SetMinimum(1)
#h_emtf1_phi.Draw()
#h_emtf1_phi.SetTitle('First emtf track #phi')
#h_emtf1_phi.GetXaxis().SetTitle('#phi')
#h_emtf1_phi.Write()
#c21.SaveAs("trees/emtf1_phi.png")
#c21.Close()

c22 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
gPad.SetLogy()
h_emtf2_phi.SetMinimum(1)
h_emtf2_phi.Draw()
h_emtf2_phi.SetTitle('Second emtf track #phi')
h_emtf2_phi.GetXaxis().SetTitle('#phi')
h_emtf2_phi.Write()
c22.SaveAs("trees/emtf2_phi.png")
c22.Close()

#c23 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf3_phi.SetMinimum(1)
#h_emtf3_phi.Draw()
#h_emtf3_phi.SetTitle('Third emtf track #phi')
#h_emtf3_phi.GetXaxis().SetTitle('#phi')
#h_emtf3_phi.Write()
#c23.SaveAs("trees/emtf3_phi.png")
#c23.Close()

#c41 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_emtf1_phi.SetFillColor(kRed)
#h_emtf1_phi.Draw()
#h_emtf2_phi.SetFillColor(kBlue)
#h_emtf2_phi.Draw("same")
#h_emtf3_phi.SetFillColor(kGreen)
#h_emtf3_phi.Draw("same")
#gPad.SetLogy()
#h_emtf1_phi.SetMinimum(1)
#h_emtf1_phi.SetTitle('#phi of first emtf track (red), second (blue), and third (green)')
#c41.SaveAs("trees/emtf_phi_overlay.png")
#c41.Close()




#c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c57.SetGrid()
#eff = TEfficiency(h_dEta_numer, h_dEta_denom)
#eff.Draw()
#eff.SetTitle('Trigger Efficiency vs #Delta #eta')
#gPad.Update()
#graph = eff.GetPaintedGraph()
##graph.SetMinimum(0)
#gPad.Update()
#eff.Write()
#c57.Update()
#c57.Modified()
#c57.Update()
#c57.SaveAs("tests2/eff_dEta.png")
#c57.Close()

#c58 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c58.SetGrid()
#eff2 = TEfficiency(h_dPhi_numer, h_dPhi_denom)
#eff2.Draw()
#eff2.SetTitle('Trigger Efficiency vs #Delta #phi')
#gPad.Update()
#graph = eff2.GetPaintedGraph()
##graph.SetMinimum(0)
#gPad.Update()
#eff2.Write()
#c58.Update()
#c58.Modified()
#c58.Update()
#c58.SaveAs("tests2/eff_dPhi.png")
#c58.Close()

#c59 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c59.SetGrid()
#eff3 = TEfficiency(h_dR_numer, h_dR_denom)
#eff3.Draw()
#eff3.SetTitle('Trigger Efficiency vs #Delta R')
#gPad.Update()
#graph = eff3.GetPaintedGraph()
##graph.SetMinimum(0)
#gPad.Update()
#eff3.Write()
#c59.Update()
#c59.Modified()
#c59.Update()
#c59.SaveAs("tests2/eff_dR.png")
#c59.Close()

#c60 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_1trk_denom.SetMinimum(1)
#h_dPhi_1trk_denom.Draw()
#h_dPhi_1trk_denom.SetTitle('#Delta #phi between offline muons if 1 track in event (denom)')
#h_dPhi_1trk_denom.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_1trk_denom.Write()
#c60.SaveAs("tests2/dPhi_1track_denom.png")
#c60.Close()

#c61 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_2trk_denom.SetMinimum(1)
#h_dPhi_2trk_denom.Draw()
#h_dPhi_2trk_denom.SetTitle('#Delta #phi between offline muons if 2 tracks in event (denom)')
#h_dPhi_2trk_denom.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_2trk_denom.Write()
#c61.SaveAs("tests2/dPhi_2track_denom.png")
#c61.Close()

#c62 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_1trk_numer.SetMinimum(1)
#h_dPhi_1trk_numer.Draw()
#h_dPhi_1trk_numer.SetTitle('#Delta #phi between offline muons if 1 track in event (numer)')
#h_dPhi_1trk_numer.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_1trk_numer.Write()
#c62.SaveAs("tests2/dPhi_1track_numer.png")
#c62.Close()

#c63 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_2trk_numer.SetMinimum(1)
#h_dPhi_2trk_numer.Draw()
#h_dPhi_2trk_numer.SetTitle('#Delta #phi between offline muons if 2 tracks in event (numer)')
#h_dPhi_2trk_numer.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_2trk_numer.Write()
#c63.SaveAs("tests2/dPhi_2track_numer.png")
#c63.Close()
  

#c51 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco1_besttrk_dR.SetMinimum(1)
#h_reco1_besttrk_dR.Draw()
#h_reco1_besttrk_dR.SetTitle('#Delta R of first reco muon with closest Emtf track')
#h_reco1_besttrk_dR.GetXaxis().SetTitle('#Delta R')
#h_reco1_besttrk_dR.Write()
#c51.SaveAs("tests2/reco1_emtf_best_dR.png")
#c51.Close()

#c52 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco2_besttrk_dR.SetMinimum(1)
#h_reco2_besttrk_dR.Draw()
#h_reco2_besttrk_dR.SetTitle('#Delta R of second reco muon with closest Emtf track')
#h_reco2_besttrk_dR.GetXaxis().SetTitle('#Delta R')
#h_reco2_besttrk_dR.Write()
#c52.SaveAs("tests2/reco2_emtf_best_dR.png")
#c52.Close()

#c53 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_besttrk_dR.SetMinimum(1)
#h_reco_besttrk_dR.Draw()
#h_reco_besttrk_dR.SetTitle('#Delta R of both reco muons with their respective closest Emtf tracks')
#h_reco_besttrk_dR.GetXaxis().SetTitle('#Delta R')
#h_reco_besttrk_dR.Write()
#c53.SaveAs("tests2/reco_emtf_best_dR.png")
#c53.Close()

#c55 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_reco2_besttrk_dR.SetFillColor(kBlue)
#h_reco2_besttrk_dR.Draw()
#h_reco1_besttrk_dR.SetFillColor(kRed)
#h_reco1_besttrk_dR.Draw("same")
#gPad.SetLogy()
#h_reco2_besttrk_dR.SetMinimum(1)
#h_reco2_besttrk_dR.GetXaxis().SetTitle('#Delta R')
#h_reco2_besttrk_dR.SetTitle('#Delta R of first reco muon with its closest Emtf track (red) and second reco muon with its closest Emtf track (blue)')
#c55.SaveAs("tests2/h_reco_besttrk_dR_overlay.png")
#c55.Close()

#c60 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c60.SetGrid()
#eff3 = TEfficiency(h_dR_1_numer, h_dR_denom)
#eff3.Draw()
#eff3.SetTitle('Trigger Efficiency vs #Delta R')
#eff3.Write()
#c60.Update()
#c60.Modified()
#c60.Update()
#c60.SaveAs("tests2/eff_dR_1.png")
#c60.Close()

#c61 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c61.SetGrid()
#eff3 = TEfficiency(h_dR_09_numer, h_dR_denom)
#eff3.Draw()
#eff3.SetTitle('Trigger Efficiency vs #Delta R')
#eff3.Write()
#c61.Update()
#c61.Modified()
#c61.Update()
#c61.SaveAs("tests2/eff_dR_09.png")
#c61.Close()

#c62 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c62.SetGrid()
#eff3 = TEfficiency(h_dR_08_numer, h_dR_denom)
#eff3.Draw()
#eff3.SetTitle('Trigger Efficiency vs #Delta R')
#eff3.Write()
#c62.Update()
#c62.Modified()
#c62.Update()
#c62.SaveAs("tests2/eff_dR_08.png")
#c62.Close()

#c63 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c63.SetGrid()
#eff3 = TEfficiency(h_dR_07_numer, h_dR_denom)
#eff3.Draw()
#eff3.SetTitle('Trigger Efficiency vs #Delta R')
#eff3.Write()
#c63.Update()
#c63.Modified()
#c63.Update()
#c63.SaveAs("tests2/eff_dR_07.png")
#c63.Close()

#c4 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dEta.SetMinimum(1)
#h_dEta.Draw()
#h_dEta.SetTitle('All offline reco muon #Delta #eta')
#h_dEta.GetXaxis().SetTitle('#Delta #eta')
#h_dEta.Write()
#c4.SaveAs("trees/reco_dEta.png")
#c4.Close()
    
#c5 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z1.SetMinimum(1)
#h_dPhi_z1.Draw()
#h_dPhi_z1.SetTitle('All offline reco muon #Delta #phi (z = 1m)')
#h_dPhi_z1.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z1.Write()
#c5.SaveAs("trees/reco_dPhi_z1.png")
#c5.Close()

#c6 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z2.SetMinimum(1)
#h_dPhi_z2.Draw()
#h_dPhi_z2.SetTitle('All offline reco muon #Delta #phi (z = 2m)')
#h_dPhi_z2.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z2.Write()
#c6.SaveAs("trees/reco_dPhi_z2.png")
#c6.Close()

#c7 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z3.SetMinimum(1)
#h_dPhi_z3.Draw()
#h_dPhi_z3.SetTitle('All offline reco muon #Delta #phi (z = 3m)')
#h_dPhi_z3.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z3.Write()
#c7.SaveAs("trees/reco_dPhi_z3.png")
#c7.Close()

#c8 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z4.SetMinimum(1)
#h_dPhi_z4.Draw()
#h_dPhi_z4.SetTitle('All offline reco muon #Delta #phi (z = 4m)')
#h_dPhi_z4.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z4.Write()
#c8.SaveAs("trees/reco_dPhi_z4.png")
#c8.Close()

#c9 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z5.SetMinimum(1)
#h_dPhi_z5.Draw()
#h_dPhi_z5.SetTitle('All offline reco muon #Delta #phi (z = 5m)')
#h_dPhi_z5.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z5.Write()
#c9.SaveAs("trees/reco_dPhi_z5.png")
#c9.Close()

#c10 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z6.SetMinimum(1)
#h_dPhi_z6.Draw()
#h_dPhi_z6.SetTitle('All offline reco muon #Delta #phi (z = 6m)')
#h_dPhi_z6.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z6.Write()
#c10.SaveAs("trees/reco_dPhi_z6.png")
#c10.Close()

#c11 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_dPhi_z7.SetMinimum(1)
#h_dPhi_z7.Draw()
#h_dPhi_z7.SetTitle('All offline reco muon #Delta #phi (z = 7m)')
#h_dPhi_z7.GetXaxis().SetTitle('#Delta #phi')
#h_dPhi_z7.Write()
#c11.SaveAs("trees/reco_dPhi_z7.png")
#c11.Close()

#c6 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_reco_phi.SetMinimum(1)
#h_reco_phi.Draw()
#h_reco_phi.SetTitle('All offline reco muon #phi')
#h_reco_phi.GetXaxis().SetTitle('#phi')
#h_reco_phi.Write()
#c6.SaveAs("trees/reco_phi.png")
#c6.Close()

#c20 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf_phi.SetMinimum(1)
#h_emtf_phi.Draw()
#h_emtf_phi.SetTitle('All EMTF tracks #phi')
#h_emtf_phi.GetXaxis().SetTitle('#phi')
#h_emtf_phi.Write()
#c20.SaveAs("trees/emtf_phi.png")
#c20.Close()

#c21 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf1_phi.SetMinimum(1)
#h_emtf1_phi.Draw()
#h_emtf1_phi.SetTitle('First emtf track #phi')
#h_emtf1_phi.GetXaxis().SetTitle('#phi')
#h_emtf1_phi.Write()
#c21.SaveAs("trees/emtf1_phi.png")
#c21.Close()

#c22 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf2_phi.SetMinimum(1)
#h_emtf2_phi.Draw()
#h_emtf2_phi.SetTitle('Second emtf track #phi')
#h_emtf2_phi.GetXaxis().SetTitle('#phi')
#h_emtf2_phi.Write()
#c22.SaveAs("trees/emtf2_phi.png")
#c22.Close()

#c23 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
#gPad.SetLogy()
#h_emtf3_phi.SetMinimum(1)
#h_emtf3_phi.Draw()
#h_emtf3_phi.SetTitle('Third emtf track #phi')
#h_emtf3_phi.GetXaxis().SetTitle('#phi')
#h_emtf3_phi.Write()
#c23.SaveAs("trees/emtf3_phi.png")
#c23.Close()

#c41 = TCanvas( 'c4', 'test scatter', 200, 10, 700, 500)
#h_emtf1_phi.SetFillColor(kRed)
#h_emtf1_phi.Draw()
#h_emtf2_phi.SetFillColor(kBlue)
#h_emtf2_phi.Draw("same")
#h_emtf3_phi.SetFillColor(kGreen)
#h_emtf3_phi.Draw("same")
#gPad.SetLogy()
#h_emtf1_phi.SetMinimum(1)
#h_emtf1_phi.SetTitle('#phi of first emtf track (red), second (blue), and third (green)')
#c41.SaveAs("trees/emtf_phi_overlay.png")
#c41.Close()