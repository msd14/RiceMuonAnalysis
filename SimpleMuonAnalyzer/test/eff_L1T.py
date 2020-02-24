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
printouts = False
plot_kinematics = True
plot_efficiency = True

## ================ Event branches ======================
evt_tree  = TChain('SimpleMuonAnalyzer/Events')


## ================ Read input files ======================
dataset = int(input("Run over: (Data:1, Monte Carlo:2):"))

if dataset == 1:
  dir1 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/SingleMuon/SingleMuon_Run2017C-17Nov2017-v1_useParent/200103_210545/0000/Ntuples2/'  
  nFiles = int(input("How many input data files? (Min:1, Max: 416):"))

  if nFiles>416 or nFiles<1: 
    print "Choose a number of input files between 1 than 416."
    sys.exit()

  i=1
  while i<(nFiles+1):
    file_name = dir1+"L1Ntuple_"+str(i)+".root"
    print 'Loading file:', "L1Ntuple_"+str(i)+".root"
    evt_tree.Add(file_name)
    i+=1
  

if dataset == 2:
  dir1 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/step1/step2/L1Ntuples/'
  nFiles = int(input("How many input MC files? (Min:1, Max: 60):"))

  if nFiles>60 or nFiles<1: 
    print "Choose a number of input MC files between 1 than 60."
    sys.exit()

  i=1
  while i<(nFiles+1): 
      print 'Loading file:', "L1Ntuple_MC_"+str(i)+".root"
      file_name = dir1+"L1Ntuple_MC_"+str(i)+".root"
      evt_tree.Add(file_name)
      i+=1

if dataset!=1 and dataset!=2:
  print 'Please choose either data:1 or monte carlo:2'
  sys.exit()

print 'Some files will give an error message if they failed processing.'


############################################
#### Initialise histograms and plot options.
############################################
eta_bins = [256, -2.8, 2.8]
phi_bins = [256, -np.pi, np.pi]

h_nEmtf = TH1D('h_nEmtf', '', 8, 0, 8)
h_nReco = TH1D('h_nReco', '', 8, 0, 8)

#Initialize kinematic histograms.
h_dEta = TH1D('h_dEta', '', eta_bins[0], -0.2, 0.2)
h_dPhi = TH1D('h_dPhi', '', phi_bins[0], -0.2, 0.2)

h_emtf_pt = TH1D('h_emtf_pt', '', 70, 0, 300)
h_emtf1_pt = TH1D('h_emtf1_pt', '', 70, 0, 300)
h_emtf2_pt = TH1D('h_emtf2_pt', '', 70, 0, 300) 
h_emtf_eta = TH1D('h_emtf_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf1_eta = TH1D('h_emtf1_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf2_eta = TH1D('h_emtf2_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_emtf_phi = TH1D('h_emtf_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf1_phi = TH1D('h_emtf1_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_emtf2_phi = TH1D('h_emtf2_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])

h_reco_pt = TH1D('h_reco_pt', '', 128, 0, 250)
h_reco1_pt = TH1F('h_reco1_pt','', 128, 0, 250)
h_reco2_pt = TH1F('h_reco2_pt', '', 256, 0, 250)
h_reco_eta = TH1D('h_reco_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco1_eta = TH1D('h_reco1_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco2_eta = TH1D('h_reco2_eta', '', eta_bins[0], eta_bins[1], eta_bins[2])
h_reco_phi = TH1D('h_reco_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_reco1_phi = TH1D('h_reco1_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])
h_reco2_phi = TH1D('h_reco2_phi', '', phi_bins[0], phi_bins[1], phi_bins[2])

#Initialize efficiency histograms (numerator, denominator).
h_dEta_denom = TH1D('h_dEta_denom', '', 64, -0.3, 0.3)
h_dPhi_denom = TH1D('h_dPhi_denom', '', 64, -0.3, 0.3)
h_dR_denom   = TH1D('h_dR_denom', '', 64, 0, 0.3)
h_dEta_numer = TH1D('h_dEta_numer', '', 64, -0.3, 0.3)
h_dPhi_numer = TH1D('h_dPhi_numer', '', 64, -0.3, 0.3)
h_dR_numer   = TH1D('h_dR_numer', '', 64, 0, 0.3)

#Counters to keep track of the number of events after each selection.
prefilter_count  = 0
medium_count     = 0
EMTFmatch_count  = 0

#Variables used to compute binned average efficiencies at the end.
denom_dR_3020 = 0. ; numer_dR_3020 = 0.
denom_dR_2010 = 0. ; numer_dR_2010 = 0.
denom_dR_1008 = 0. ; numer_dR_1008 = 0.
denom_dR_0806 = 0. ; numer_dR_0806 = 0.
denom_dR_0604 = 0. ; numer_dR_0604 = 0.
denom_dR_0402 = 0. ; numer_dR_0402 = 0.
denom_dR_0200 = 0. ; numer_dR_0200 = 0.
## ================================================
## ================================================


#######################################
#### Event loop.
#######################################
for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  #In the MC, some events have less than two reco muons. Ignore these events.
  if len(evt_tree.reco_eta) < 2: continue

  #Default values in ntuples are -99. Remove events not defined correctly.
  for i in range(len(evt_tree.reco_eta)):
    if (evt_tree.reco_pt[i] < -90 or evt_tree.reco_eta[i] < -90 or evt_tree.reco_phi[i] < -90): continue

  h_nReco.Fill(len(evt_tree.reco_pt))
  h_nEmtf.Fill(len(evt_tree.emtf_pt))
  ## ================================================
  ## ================================================

  #######################################
  #### Save RECO muon properties.
  #######################################
  reco_pT, reco_eta, reco_phi, reco_eta_prop, reco_phi_prop = [],[],[],[],[]

  #For the MC, there can be up to eight offline reco muons per event. 
  #Find a muon pair with dR < 0.5 that pass through an endcap.
  index = [-1, -1]
  for i in range(len(evt_tree.reco_eta)):
    for j in range(len(evt_tree.reco_eta)):
      if i!=j and abs(evt_tree.reco_eta[i]) > 1.2 and abs(evt_tree.reco_eta[i]) < 2.4 and abs(evt_tree.reco_eta[j]) > 1.2 and abs(evt_tree.reco_eta[j]) < 2.4:
	if h.CalcDR2(evt_tree.reco_eta[i], evt_tree.reco_phi[i], evt_tree.reco_eta[j], evt_tree.reco_phi[j]) < 0.5:
	  index = [i, j]
	  break

  #If no good pair, skip the event.
  if index[0]<0: continue

  #Order reco muons by leading pT.
  i=index[0]; j=index[1]
  if evt_tree.reco_pt[i] > evt_tree.reco_pt[j]: 
    for i in range(2):
      j=index[i]
      reco_pT.append(evt_tree.reco_pt[j])
      reco_eta.append(evt_tree.reco_eta[j])
      reco_phi.append(evt_tree.reco_phi[j])
      reco_eta_prop.append(evt_tree.reco_eta_prop[j])
      reco_phi_prop.append(evt_tree.reco_phi_prop[j])

  else:
    for i in range(1, -1, -1):
      j=index[i]
      reco_pT.append(evt_tree.reco_pt[j])
      reco_eta.append(evt_tree.reco_eta[j])
      reco_phi.append(evt_tree.reco_phi[j])
      reco_eta_prop.append(evt_tree.reco_eta_prop[j])
      reco_phi_prop.append(evt_tree.reco_phi_prop[j])


  #A pT filter wasn't applied to the MC, so apply one.
  if len(reco_pT)!=2: continue
  if reco_pT[0] < 15 or reco_pT[1] < 15: continue 
  ## ================================================
  ## ================================================

  #################################################
  #### Save L1 muon properties. Remove duplicates.
  #################################################
  emtf_pT, emtf_eta, emtf_phi = [], [], []   #L1 (regional muon candidate) properties.

  #MC currently doesn't have unpacked Emtf tracks to remove duplicates.
  #If two regional muon candidates have exactly the same (eta, phi) then only keep one.
  if len(evt_tree.emtf_phi)>0:
    if evt_tree.emtf_quality[0]>12:
      emtf_pT.append(evt_tree.emtf_pt[0])
      emtf_eta.append(evt_tree.emtf_eta[0])
      emtf_phi.append(evt_tree.emtf_phi[0])

    for i in range(len(evt_tree.emtf_phi)):
      flag=0

      #Compare the (eta,phi) of current track to the ones already saved.
      for j in range(len(emtf_phi)):
	if emtf_eta[j]!= evt_tree.emtf_eta[i] or emtf_phi[j]!= evt_tree.emtf_phi[i]:
	  flag+=1


      #If the track isn't a duplicate, save its properties.
      if flag==len(emtf_phi) and evt_tree.emtf_quality[i]>12:
	  emtf_pT.append(evt_tree.emtf_pt[i])
	  emtf_eta.append(evt_tree.emtf_eta[i])
	  emtf_phi.append(evt_tree.emtf_phi[i])

  ## ================================================
  ## ================================================
  unpEmtf_Pt, unpEmtf_Eta, unpEmtf_Phi, unpEmtf_Phi_fp, unpEmtf_Phi_glob = [],[],[],[],[] #L1 (Unpacked Emtf track) properties.

  #For the SM data use unpacked tracks as L1 muons.
  if dataset==1:
    if len(evt_tree.unpEmtf_Pt)>0:
      if evt_tree.unpEmtf_Mode[0]>12: #Apply a quality cut.
	unpEmtf_Pt.append(evt_tree.unpEmtf_Pt[0])
	unpEmtf_Eta.append(evt_tree.unpEmtf_Eta[0])
	unpEmtf_Phi.append(evt_tree.unpEmtf_Phi[0])
	unpEmtf_Phi_fp.append(evt_tree.unpEmtf_Phi_fp[0])
	unpEmtf_Phi_glob.append(evt_tree.unpEmtf_Phi_glob[0]*np.pi/180.)

      for i in range(len(evt_tree.unpEmtf_Eta)):
	flag=0

	#If two tracks differ in integer phi by exactly 3600 (duplicate), only keep one.
	for j in range(len(unpEmtf_Eta)):
	  if i!=j and abs(unpEmtf_Phi_fp[j] - evt_tree.unpEmtf_Phi_fp[i]) != 3600 and abs(unpEmtf_Phi_glob[j] - evt_tree.unpEmtf_Phi_glob[i]) != 0:
	    flag+=1

	#If the track isn't a duplicate, save its properties.
	if flag==len(unpEmtf_Eta) and evt_tree.unpEmtf_Mode[i]>12:
	    unpEmtf_Pt.append(evt_tree.unpEmtf_Pt[i])
	    unpEmtf_Eta.append(evt_tree.unpEmtf_Eta[i])
	    unpEmtf_Phi.append(evt_tree.unpEmtf_Phi[i])
	    unpEmtf_Phi_fp.append(evt_tree.unpEmtf_Phi_fp[i])
	    unpEmtf_Phi_glob.append(evt_tree.unpEmtf_Phi_glob[i]*np.pi/180.)
  ## ================================================
  ## ================================================
  
  #######################################
  #### Match reco muons to L1 muons
  #######################################
  temp1, temp2 = [], [] 

  #Match a reco muon to a L1 muon.
  #For SM dataset, use unpacked emtf track as L1 Muon.
  if dataset==1 and len(unpEmtf_Eta)>1:
    for i in range(len(unpEmtf_Eta)):
      temp1.append(h.CalcDR2(reco_eta_prop[0], reco_phi_prop[0], unpEmtf_Eta[i], unpEmtf_Phi_glob[i]))
      temp2.append(h.CalcDR2(reco_eta_prop[1], reco_phi_prop[1], unpEmtf_Eta[i], unpEmtf_Phi_glob[i]))

    if temp1[0]==temp1[1]: continue #Very rarely (1 in 30K events), the temp elements will be equal and the code will crash. Skip these events.

    #Make sure that you don't match both reco muons to the same L1 muon (check the index of smallest dR)
    #Store the reco-L1 separation distances into variables 'best1, best2'. Use for a later selection.
    dR1 = set(temp1) ; dR2 = set(temp2)
    if np.argmin(temp1) == np.argmin(temp2) and sorted(dR1)[0] < sorted(dR2)[0]: best1 = sorted(dR1)[0] ; best2 = sorted(dR2)[1] 
    if np.argmin(temp1) == np.argmin(temp2) and sorted(dR1)[0] > sorted(dR2)[0]: best1 = sorted(dR1)[1] ; best2 = sorted(dR2)[0]
    if np.argmin(temp1) != np.argmin(temp2): best1 = sorted(dR1)[0] ; best2 = sorted(dR2)[0] 


  #The MC doesn't have unpacked tracks, so use regional muon cands instead for L1 muons.
  if dataset==2 and len(emtf_eta)>1:
    for i in range(len(emtf_eta)):
      temp1.append(h.CalcDR2(reco_eta_prop[0], reco_phi_prop[0], emtf_eta[i], emtf_phi[i]))
      temp2.append(h.CalcDR2(reco_eta_prop[1], reco_phi_prop[1], emtf_eta[i], emtf_phi[i]))

    dR1 = set(temp1) ; dR2 = set(temp2)
    if np.argmin(temp1) == np.argmin(temp2) and sorted(dR1)[0] < sorted(dR2)[0]: best1 = sorted(dR1)[0] ; best2 = sorted(dR2)[1] 
    if np.argmin(temp1) == np.argmin(temp2) and sorted(dR1)[0] > sorted(dR2)[0]: best1 = sorted(dR1)[1] ; best2 = sorted(dR2)[0]
    if np.argmin(temp1) != np.argmin(temp2): best1 = sorted(dR1)[0] ; best2 = sorted(dR2)[0]

  ## ================================================
  ## ================================================

  #####################################################
  ##### Some useful printouts.
  #####################################################

  if printouts == True:
    print 'reco muon properties (pT, eta, phi (propagated)):'
    print 'reco muon 1:', reco_pT[0], reco_eta_prop[0], reco_phi_prop[0]
    print 'reco muon 2:', reco_pT[1], reco_eta_prop[1], reco_phi_prop[1]
    print 'L1 muon properties (pT, eta, phi):'

    if dataset==1:
      for i in range(len(unpEmtf_Eta)):
	print 'L1 muon', i+1, ':',  unpEmtf_Pt[i], unpEmtf_Eta[i], unpEmtf_Phi_glob[i]
    else:
      for i in range(len(emtf_eta)):
	print 'L1 muon', i+1, ':',  emtf_pT[i], emtf_eta[i], emtf_phi[i]
    print '---------------'
    ## ================================================
    ## ================================================

  #####################################################
  ##### Apply selections, calculate trigger efficiency.
  #####################################################

  prefilter_count+=1   #No selections applied (only filter)
  if evt_tree.reco_isMediumMuon[0] != 1 or evt_tree.reco_isMediumMuon[1] != 1: continue
  medium_count+=1    #Events that pass medium selection.

  dEta = reco_eta_prop[0] - reco_eta_prop[1]
  dPhi = reco_phi_prop[0] - reco_phi_prop[1]
  dR = h.CalcDR2(reco_eta_prop[0], reco_phi_prop[0], reco_eta_prop[1], reco_phi_prop[1])

  #Denominator histogram.
  h_dEta_denom.Fill(dEta)
  h_dPhi_denom.Fill(dPhi)
  h_dR_denom.Fill(dR)

  if dR <= 0.30 and dR > 0.20: denom_dR_3020+=1
  if dR <= 0.20 and dR > 0.10: denom_dR_2010+=1
  if dR <= 0.10 and dR > 0.08: denom_dR_1008+=1
  if dR <= 0.08 and dR > 0.06: denom_dR_0806+=1
  if dR <= 0.06 and dR > 0.04: denom_dR_0604+=1
  if dR <= 0.04 and dR > 0.02: denom_dR_0402+=1
  if dR <= 0.02: denom_dR_0200+=1

  if dataset==1: 
    if len(unpEmtf_Eta)<2: continue
    if best1>0.2 or best2>0.2: continue
  if dataset==2: 
    if len(emtf_phi)<2: continue
    if best1>0.2 or best2>0.2: continue

  EMTFmatch_count+=1

  #Numerator histogram.
  h_dEta_numer.Fill(dEta)
  h_dPhi_numer.Fill(dPhi)
  h_dR_numer.Fill(dR)

  if dR <= 0.30 and dR > 0.20: numer_dR_3020+=1
  if dR <= 0.20 and dR > 0.10: numer_dR_2010+=1
  if dR <= 0.10 and dR > 0.08: numer_dR_1008+=1
  if dR <= 0.08 and dR > 0.06: numer_dR_0806+=1
  if dR <= 0.06 and dR > 0.04: numer_dR_0604+=1
  if dR <= 0.04 and dR > 0.02: numer_dR_0402+=1
  if dR <= 0.02: numer_dR_0200+=1
  ## ================================================
  ## ================================================

####################################################
#### Printout NEvents, efficiencies binned by dR.
####################################################
print '-------------'
print 'nMuons after selections:'
print 'pre-selections only:', prefilter_count
print 'both reco muons are medium ID:', medium_count
print 'both muons are EMTF matched:', EMTFmatch_count
print '-------------'
print 'Averaged efficiency binned:'
print '0.30 > dR > 0.20: ', numer_dR_3020/denom_dR_3020
print '0.20 > dR > 0.10: ', numer_dR_2010/denom_dR_2010
print '0.10 > dR > 0.08: ', numer_dR_1008/denom_dR_1008
print '0.08 > dR > 0.06: ', numer_dR_0806/denom_dR_0806
print '0.06 > dR > 0.04: ', numer_dR_0604/denom_dR_0604
print '0.04 > dR > 0.02: ', numer_dR_0402/denom_dR_0402
print '0.02 > dR: ', numer_dR_0200/denom_dR_0200
print '-------------'

####################################################
#### Fill kinematic histograms.
####################################################

#Reco muons.
h_reco1_pt.Fill(reco_pT[0])
h_reco2_pt.Fill(reco_pT[1])
h_reco1_eta.Fill(reco_eta[0])
h_reco2_eta.Fill(reco_eta[1])
h_reco1_phi.Fill(reco_phi[0])
h_reco2_phi.Fill(reco_phi[1])
h_dEta.Fill(reco_eta_prop[0] - reco_eta_prop[1])
h_dPhi.Fill(reco_phi_prop[0] - reco_phi_prop[1])

for j in range(len(reco_pT)):
  h_reco_pt.Fill(reco_pT[j])
  h_reco_eta.Fill(reco_eta[j])
  h_reco_phi.Fill(reco_phi[j])

#Regional muon candidate kinematics.
for j in range(len(emtf_pT)):
  if j==0: 
    h_emtf_pt.Fill(emtf_pT[j])
    h_emtf_eta.Fill(emtf_eta[j])
    h_emtf_phi.Fill(emtf_phi[j])

    h_emtf1_pt.Fill(emtf_pT[j])
    h_emtf1_eta.Fill(emtf_eta[j])
    h_emtf1_phi.Fill(emtf_phi[j])

  if j==1:
    h_emtf_pt.Fill(emtf_pT[j])
    h_emtf_eta.Fill(emtf_eta[j])
    h_emtf_phi.Fill(emtf_phi[j])

    h_emtf2_pt.Fill(emtf_pT[j])
    h_emtf2_eta.Fill(emtf_eta[j])
    h_emtf2_phi.Fill(emtf_phi[j])
  ## ================================================
  ## ================================================

############################################################
### Write output file with histograms and efficiencies ###
############################################################
if plot_efficiency == True:
  c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
  c57.SetGrid()
  eff = TEfficiency(h_dEta_numer, h_dEta_denom)
  eff.Draw()
  if dataset==1: eff.SetTitle('Trigger Efficiency vs #Delta #eta')
  else: eff.SetTitle('Trigger Efficiency vs #Delta #eta (MC)')
  gPad.Update()
  graph = eff.GetPaintedGraph()
  graph.SetMinimum(0)
  graph.SetMaximum(1)
  if dataset==1: c57.SaveAs("tests2/eff_dEta.png")
  else: c57.SaveAs("tests2/eff_dEta_MC.png")
  c57.Close()

  c58 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
  c58.SetGrid()
  eff2 = TEfficiency(h_dPhi_numer, h_dPhi_denom)
  eff2.Draw()
  if dataset==1: eff2.SetTitle('Trigger Efficiency vs #Delta #phi')
  else: eff2.SetTitle('Trigger Efficiency vs #Delta #phi (MC)')
  gPad.Update()
  graph = eff2.GetPaintedGraph()
  graph.SetMinimum(0)
  graph.SetMaximum(1)
  if dataset==1: c58.SaveAs("tests2/eff_dPhi.png")
  else: c58.SaveAs("tests2/eff_dPhi_MC.png")
  c58.Close()

  c59 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
  c59.SetGrid()
  eff3 = TEfficiency(h_dR_numer, h_dR_denom)
  eff3.Draw()
  if dataset==1: eff3.SetTitle('Trigger Efficiency vs #Delta R')
  else: eff3.SetTitle('Trigger Efficiency vs #Delta R (MC)')
  gPad.Update()
  graph = eff3.GetPaintedGraph()
  graph.SetMinimum(0)
  graph.SetMaximum(1)
  if dataset==1: c59.SaveAs("tests2/eff_dR.png")
  else: c59.SaveAs("tests2/eff_dR_MC.png")
  c59.Close()

################
################
################

if plot_kinematics == True:
  c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco_pt.SetMinimum(1)
  h_reco_pt.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco_pt.SetTitle('All offline reco muon pT')
  if dataset==2: h_reco_pt.SetTitle('All offline reco muon pT (MC)')
  h_reco_pt.GetXaxis().SetTitle('pT (GeV)')
  h_reco_pt.Write()
  if dataset==1: c1.SaveAs("trees/reco_pT.png")
  if dataset==2: c1.SaveAs("trees/reco_pT_MC.png")
  c1.Close()

  c2 = TCanvas( 'c2', '', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco1_pt.SetMinimum(1)
  h_reco1_pt.Draw()
  gStyle.SetOptStat(0)
  h_reco1_pt.GetXaxis().SetTitle('pT (GeV)')
  if dataset==1: h_reco1_pt.SetTitle('First offline reco muon pT')
  if dataset==2: h_reco1_pt.SetTitle('First offline reco muon pT (MC)')
  h_reco1_pt.Write()
  if dataset==1: c2.SaveAs("trees/reco1_pT.png")
  if dataset==2: c2.SaveAs("trees/reco1_pT_MC.png")
  c2.Close()

  c3 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco2_pt.SetMinimum(1)
  h_reco2_pt.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco2_pt.SetTitle('Second offline reco muon pT')
  if dataset==2: h_reco2_pt.SetTitle('Second offline reco muon pT (MC)')
  h_reco2_pt.GetXaxis().SetTitle('pT (GeV)')
  h_reco2_pt.Write()
  if dataset==1: c3.SaveAs("trees/reco2_pT.png")
  if dataset==2: c3.SaveAs("trees/reco2_pT_MC.png")
  c3.Close()

  c4 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco_eta.SetMinimum(1)
  h_reco_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco_eta.SetTitle('All offline reco muon #eta')
  if dataset==2: h_reco_eta.SetTitle('All offline reco muon #eta (MC)')
  h_reco_eta.GetXaxis().SetTitle('#eta')
  h_reco_eta.Write()
  if dataset==1: c4.SaveAs("trees/reco_eta.png")
  if dataset==2: c4.SaveAs("trees/reco_eta_MC.png")
  c4.Close()

  c5 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco1_eta.SetMinimum(1)
  h_reco1_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco1_eta.SetTitle('First offline reco muon #eta')
  if dataset==2: h_reco1_eta.SetTitle('First offline reco muon #eta (MC)')
  h_reco1_eta.GetXaxis().SetTitle('#eta')
  h_reco1_eta.Write()
  if dataset==1: c5.SaveAs("trees/reco1_eta.png")
  if dataset==2: c5.SaveAs("trees/reco1_eta_MC.png")
  c5.Close()

  c5 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco2_eta.SetMinimum(1)
  h_reco2_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco2_eta.SetTitle('Second offline reco muon #eta')
  if dataset==2: h_reco2_eta.SetTitle('Second offline reco muon #eta (MC)')
  h_reco2_eta.GetXaxis().SetTitle('#eta')
  h_reco2_eta.Write()
  if dataset==1: c5.SaveAs("trees/reco2_eta.png")
  if dataset==2: c5.SaveAs("trees/reco2_eta_MC.png")
  c5.Close()

  c6 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco_phi.SetMinimum(1)
  h_reco_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco_phi.SetTitle('All offline reco muon #phi')
  if dataset==2: h_reco_phi.SetTitle('All offline reco muon #phi (MC)')
  h_reco_phi.GetXaxis().SetTitle('#phi')
  h_reco_phi.Write()
  if dataset==1: c6.SaveAs("trees/reco_phi.png")
  if dataset==2: c6.SaveAs("trees/reco_phi_MC.png")
  c6.Close()

  c7 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco1_phi.SetMinimum(1)
  h_reco1_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco1_phi.SetTitle('First offline reco muon #phi')
  if dataset==2: h_reco1_phi.SetTitle('First offline reco muon #phi (MC)')
  h_reco1_phi.GetXaxis().SetTitle('#phi')
  h_reco1_phi.Write()
  if dataset==1: c7.SaveAs("trees/reco1_phi.png")
  if dataset==2: c7.SaveAs("trees/reco1_phi_MC.png")
  c7.Close()

  c8 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_reco2_phi.SetMinimum(1)
  h_reco2_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_reco2_phi.SetTitle('Second offline reco muon #phi')
  if dataset==2: h_reco2_phi.SetTitle('Second offline reco muon #phi (MC)')
  h_reco2_phi.GetXaxis().SetTitle('#phi')
  h_reco2_phi.Write()
  if dataset==1: c8.SaveAs("trees/reco2_phi.png")
  if dataset==2: c8.SaveAs("trees/reco2_phi_MC.png")
  c8.Close()

  c12 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf_pt.SetMinimum(1)
  h_emtf_pt.Draw()
  gStyle.SetOptStat(0)
  h_emtf_pt.SetTitle('All EMTF Tracks pT')
  if dataset==1: h_emtf_pt.GetXaxis().SetTitle('pT (GeV)')
  if dataset==2: h_emtf_pt.GetXaxis().SetTitle('pT (GeV) (MC)')
  h_emtf_pt.Write()
  if dataset==1: c12.SaveAs("trees/emtf_pT.png")
  if dataset==2: c12.SaveAs("trees/emtf_pT_MC.png")
  c12.Close()

  c13 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf1_pt.SetMinimum(1)
  h_emtf1_pt.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf1_pt.SetTitle('First Emtf track pT')
  if dataset==2: h_emtf1_pt.SetTitle('First Emtf track pT (MC)')
  h_emtf1_pt.GetXaxis().SetTitle('pT (GeV)')
  h_emtf1_pt.Write()
  if dataset==1: c13.SaveAs("trees/emtf1_pT.png")
  if dataset==2: c13.SaveAs("trees/emtf1_pT_MC.png")
  c13.Close()

  c14 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf2_pt.SetMinimum(1)
  h_emtf2_pt.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf2_pt.SetTitle('Second Emtf track pT')
  if dataset==2: h_emtf2_pt.SetTitle('Second Emtf track pT (MC)')
  h_emtf2_pt.GetXaxis().SetTitle('pT (GeV)')
  h_emtf2_pt.Write()
  if dataset==1: c14.SaveAs("trees/emtf2_pT.png")
  if dataset==2: c14.SaveAs("trees/emtf2_pT_MC.png")
  c14.Close()

  c16 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf_eta.SetMinimum(1)
  h_emtf_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf_eta.SetTitle('All EMTF tracks #eta')
  if dataset==2: h_emtf_eta.SetTitle('All EMTF tracks #eta (MC)')
  h_emtf_eta.GetXaxis().SetTitle('#eta')
  h_emtf_eta.Write()
  if dataset==1: c16.SaveAs("trees/emtf_eta.png")
  if dataset==2: c16.SaveAs("trees/emtf_eta_MC.png")
  c16.Close()

  c17 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf1_eta.SetMinimum(1)
  h_emtf1_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf1_eta.SetTitle('First Emtf track #eta')
  if dataset==2: h_emtf1_eta.SetTitle('First Emtf track #eta (MC)')
  h_emtf1_eta.GetXaxis().SetTitle('#eta')
  h_emtf1_eta.Write()
  if dataset==1: c17.SaveAs("trees/emtf1_eta.png")
  if dataset==2: c17.SaveAs("trees/emtf1_eta_MC.png")
  c17.Close()

  c18 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf2_eta.SetMinimum(1)
  h_emtf2_eta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf2_eta.SetTitle('Second Emtf track #eta')
  if dataset==2: h_emtf2_eta.SetTitle('Second Emtf track #eta (MC)')
  h_emtf2_eta.GetXaxis().SetTitle('#eta')
  h_emtf2_eta.Write()
  if dataset==1: c18.SaveAs("trees/emtf2_eta.png")
  if dataset==2: c18.SaveAs("trees/emtf2_eta_MC.png")
  c18.Close()

  c20 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf_phi.SetMinimum(1)
  h_emtf_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf_phi.SetTitle('All EMTF tracks #phi')
  if dataset==2: h_emtf_phi.SetTitle('All EMTF tracks #phi (MC)')
  h_emtf_phi.GetXaxis().SetTitle('#phi')
  h_emtf_phi.Write()
  if dataset==1: c20.SaveAs("trees/emtf_phi.png")
  if dataset==2: c20.SaveAs("trees/emtf_phi_MC.png")
  c20.Close()

  c21 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf1_phi.SetMinimum(1)
  h_emtf1_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf1_phi.SetTitle('First emtf track #phi')
  if dataset==2: h_emtf1_phi.SetTitle('First emtf track #phi (MC)')
  h_emtf1_phi.GetXaxis().SetTitle('#phi')
  h_emtf1_phi.Write()
  if dataset==1: c21.SaveAs("trees/emtf1_phi.png")
  if dataset==2: c21.SaveAs("trees/emtf1_phi_MC.png")
  c21.Close()

  c22 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_emtf2_phi.SetMinimum(1)
  h_emtf2_phi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_emtf2_phi.SetTitle('Second emtf track #phi')
  if dataset==2: h_emtf2_phi.SetTitle('Second emtf track #phi (MC)')
  h_emtf2_phi.GetXaxis().SetTitle('#phi')
  h_emtf2_phi.Write()
  if dataset==1: c22.SaveAs("trees/emtf2_phi.png")
  if dataset==2: c22.SaveAs("trees/emtf2_phi_MC.png")
  c22.Close()

  c33 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_nReco.SetMinimum(1)
  h_nReco.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_nReco.SetTitle('Number of Offline Reconstructed Muons per event')
  if dataset==2: h_nReco.SetTitle('Number of Offline Reconstructed Muons per event (MC)')
  h_nReco.GetXaxis().SetTitle('Offline Muons')
  h_nReco.Write()
  if dataset==1: c33.SaveAs("trees/nReco.png")
  if dataset==2: c33.SaveAs("trees/nReco_MC.png")
  c33.Close()

  c34 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_nEmtf.SetMinimum(1)
  h_nEmtf.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_nEmtf.SetTitle('Number of EMTF tracks per event')
  if dataset==2: h_nEmtf.SetTitle('Number of EMTF tracks per event (MC)')
  h_nEmtf.GetXaxis().SetTitle('EMTF Tracks')
  h_nEmtf.Write()
  if dataset==1: c34.SaveAs("trees/nEmtf.png")
  if dataset==2: c34.SaveAs("trees/nEmtf_MC.png")
  c34.Close()

  c35 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_dEta.SetMinimum(1)
  h_dEta.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_dEta.SetTitle('Difference between reco muon #eta')
  if dataset==2: h_dEta.SetTitle('Difference between reco muon #eta (MC)')
  h_dEta.GetXaxis().SetTitle('#Delta #eta')
  h_dEta.Write()
  if dataset==1: c35.SaveAs("trees/dEta.png")
  if dataset==2: c35.SaveAs("trees/dEta_MC.png")
  c35.Close()

  c36 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
  gPad.SetLogy()
  h_dPhi.SetMinimum(1)
  h_dPhi.Draw()
  gStyle.SetOptStat(0)
  if dataset==1: h_dPhi.SetTitle('Difference between reco muon #phi')
  if dataset==2: h_dPhi.SetTitle('Difference between reco muon #phi (MC)')
  h_dPhi.GetXaxis().SetTitle('#Delta #phi')
  h_dPhi.Write()
  if dataset==1: c36.SaveAs("trees/dPhi.png")
  if dataset==2: c36.SaveAs("trees/dPhi_MC.png")
  c36.Close()