# -*- coding: utf-8 -*-
import ROOT as rt
import CMS_lumi, tdrstyle
import array

kinematics = False
efficiency = True

name_kin = ['h_reco_pt', 'h_reco_eta', 'h_reco_phi', 'h_emtf_pt', 'h_emtf_eta', 'h_emtf_phi']
title_kin = ['All offline reco muon pT', 'All offline reco muon #eta', 'All offline reco muon #phi', 'All L1 muon pT', 'All L1 muon #eta', 'All L1 muon #phi']

#name_eff = ['efficiency_dEta', 'efficiency_dPhi', 'efficiency_dR']
#title_eff = '2017C (4.79 fb^{-1})'
name_eff = ['efficiency_dEta', 'efficiency_dPhi', 'efficiency_dR']
title_eff = 'Monte Carlo MSSMD'

out_file  = rt.TFile('histo_style.root','recreate')

out_file.cd()

if efficiency == True:
  for i in range(len(name_eff)):
    #set the tdr style
    tdrstyle.setTDRStyle()

    #change the CMS_lumi variables (see CMS_lumi.py)
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText = "Simulation"   #Preliminary, In-Progress

    iPos = 11
    if( iPos==0 ): CMS_lumi.relPosX = 0.12

    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref

    iPeriod = 0

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = rt.TCanvas("c2","c2",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( 0.15 ) #L/W
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)

    file = rt.TFile("Histograms.root","READ")
    hist   = file.Get(name_eff[i])
    hist.Draw("")
    rt.gPad.Update()
    graph = hist.GetPaintedGraph()
    graph.SetMinimum(0)
    graph.SetMaximum(1)

    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos,title_eff)

    canvas.cd()
    canvas.Update()

    #set the colors and size for the legend
    markerSize  = 1.0

    latex = rt.TLatex()
    n_ = 2

    if i==0: x1_l = 0.82
    else: x1_l = 0.92
    y1_l = 0.40

    dx_l = 0.30
    dy_l = 0.18
    x0_l = x1_l-dx_l
    y0_l = y1_l-dy_l

    legend =  rt.TPad("legend_0","legend_0",x0_l,y0_l,x1_l, y1_l )
    legend.Draw()
    legend.cd()

    ar_l = dy_l/dx_l
    gap_ = 1./(n_+1)
    bwx_ = 0.12
    bwy_ = 0.12

    x_l = [1.*bwx_]
    y_l = [0.25]
    ex_l = [0]
    ey_l = [0.04/ar_l]

    #array must be converted 
    x_l = array.array("f",x_l)
    ex_l = array.array("f",ex_l)
    y_l = array.array("f",y_l)
    ey_l = array.array("f",ey_l)

    gr_l =  rt.TGraphErrors(1, x_l, y_l, ex_l, ey_l)

    rt.gStyle.SetEndErrorSize(0)
    gr_l.SetMarkerSize(0.9)
    gr_l.SetMarkerStyle(2)
    gr_l.Draw("P")

    latex.SetTextFont(42)
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)    
    latex.SetTextSize(0.25)    
    latex.SetTextAlign(12) 

    #box_ = rt.TBox()
    xx_ = x_l[0]
    yy_ = y_l[0]
    #latex.DrawLatex(xx_+1.*bwx_,yy_,"Data")
    latex.DrawLatex(xx_,yy_,r'$\gamma_{D} \rightarrow \mu^+ \mu^-$ (MC)')

    raw_input("Press Enter to end")

if kinematics == True:
  for i in range(len(name_kin)):
    #set the tdr style
    tdrstyle.setTDRStyle()

    #change the CMS_lumi variables (see CMS_lumi.py)
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText = "Preliminary"   #Simulation, In-Progress

    iPos = 11
    if( iPos==0 ): CMS_lumi.relPosX = 0.12

    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref

    iPeriod = 0

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = rt.TCanvas("c2","c2",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)

    file = rt.TFile("Histograms.root","READ")
    hist   = file.Get(name_kin[i])
    hist.Draw("")
    #hist.GetYaxis().SetRangeUser(0,1)

    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos,title_kin[i])

    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    #update the canvas
    canvas.Update()

    raw_input("Press Enter to end")
