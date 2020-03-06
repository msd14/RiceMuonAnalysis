#ifndef RiceMuonAnalysis_SimpleMuonAnalyzer_MyNtuple
#define RiceMuonAnalysis_SimpleMuonAnalyzer_MyNtuple

#include "TTree.h"
#include <vector>
#include <string>

const int nMaxRecoMuons = 8;
const int nMaxEmtfMuons = 8;

namespace{

struct MyNtuple
{
  void init(); // initialize to default values
  TTree* book(TTree *t, const std::string & name = "trk_eff");

  int lumi;
  int run;
  int event;

  // number of EMTF tracks
  int nEmtf;
  int nRecoMuon;

  float emtf_pt[nMaxEmtfMuons];
  float emtf_eta[nMaxEmtfMuons];
  float emtf_phi[nMaxEmtfMuons];
  int emtf_charge[nMaxEmtfMuons];
  int emtf_quality[nMaxEmtfMuons];

  float unpEmtf_Pt[nMaxEmtfMuons];
  float unpEmtf_Eta[nMaxEmtfMuons];
  float unpEmtf_Theta[nMaxEmtfMuons];
  float unpEmtf_Phi_glob[nMaxEmtfMuons];
  int unpEmtf_Phi_fp[nMaxEmtfMuons];
  int unpEmtf_Theta_fp[nMaxEmtfMuons];
  int unpEmtf_Mode[nMaxEmtfMuons];
  int unpEmtf_Mode_neighbor[nMaxEmtfMuons];
  int unpEmtf_BX[nMaxEmtfMuons];

  float reco_pt[nMaxRecoMuons];
  float reco_eta[nMaxRecoMuons];
  float reco_phi[nMaxRecoMuons];
  float reco_eta_prop[nMaxRecoMuons];
  float reco_phi_prop[nMaxRecoMuons];
  float reco_eta_st2[nMaxRecoMuons];
  float reco_phi_st2[nMaxRecoMuons];
  int reco_charge[nMaxRecoMuons];
  int reco_isMediumMuon[nMaxRecoMuons];
  int reco_hasEMTFMatch[nMaxRecoMuons];
};

void MyNtuple::init()
{
  lumi = -99;
  run = -99;
  event = -99;

  nEmtf = 0;
  nRecoMuon = 0;

  for (unsigned i=0; i<nMaxEmtfMuons; ++i){
    emtf_pt[i]= -99;
    emtf_eta[i] = -99.;
    emtf_phi[i]= -99;
    emtf_charge[i] = - 99;
    emtf_quality[i] = - 99;

    unpEmtf_Pt[i] = -99;
    unpEmtf_Eta[i] = -99;
    unpEmtf_Theta[i] = -99;
    unpEmtf_Phi_glob[i] = -99;
    unpEmtf_Phi_fp[i] = -99;
    unpEmtf_Theta_fp[i] = -99;
    unpEmtf_Mode[i] = -99;
    unpEmtf_Mode_neighbor[i] = -99;
    unpEmtf_BX[i] = -99;

  }
  for (unsigned i=0; i<nMaxRecoMuons; ++i){
    reco_pt[i]= -99;
    reco_eta[i] = -99.;
    reco_phi[i]= -99;
    reco_eta_prop[i] = -99.;
    reco_phi_prop[i]= -99;
    reco_eta_st2[i] = -99;
    reco_phi_st2[i] = -99;
    reco_charge[i] = - 99;
    reco_isMediumMuon[i] = 0;
    reco_hasEMTFMatch[i] = 0;
  }
}


TTree* MyNtuple::book(TTree *t, const std::string & name)
{
  edm::Service< TFileService > fs;
  t = fs->make<TTree>(name.c_str(), name.c_str());

  t->Branch("lumi", &lumi);
  t->Branch("run", &run);
  t->Branch("event", &event);

  t->Branch("nEmtf", &nEmtf);
  t->Branch("nRecoMuon", &nRecoMuon);

  t->Branch("emtf_pt",emtf_pt,"emtf_pt[nEmtf]/F");
  t->Branch("emtf_eta",emtf_eta,"emtf_eta[nEmtf]/F");
  t->Branch("emtf_phi",emtf_phi,"emtf_phi[nEmtf]/F");
  t->Branch("emtf_charge",emtf_charge,"emtf_charge[nEmtf]/I");
  t->Branch("emtf_quality",emtf_quality,"emtf_quality[nEmtf]/I");

  t->Branch("unpEmtf_Pt", unpEmtf_Pt, "unpEmtf_Pt[nEmtf]/F");
  t->Branch("unpEmtf_Eta", unpEmtf_Eta, "unpEmtf_Eta[nEmtf]/F");
  t->Branch("unpEmtf_Theta", unpEmtf_Theta, "unpEmtf_Theta[nEmtf]/F");
  t->Branch("unpEmtf_Phi_glob", unpEmtf_Phi_glob, "unpEmtf_Phi_glob[nEmtf]/F");
  t->Branch("unpEmtf_Theta_fp", unpEmtf_Theta_fp, "unpEmtf_Theta_fp[nEmtf]/I");
  t->Branch("unpEmtf_Phi_fp", unpEmtf_Phi_fp, "unpEmtf_Phi_fp[nEmtf]/I");
  t->Branch("unpEmtf_Mode", unpEmtf_Mode, "unpEmtf_Mode[nEmtf]/I");
  t->Branch("unpEmtf_Mode_neighbor", unpEmtf_Mode_neighbor, "unpEmtf_Mode_neighbor[nEmtf]/I");
  t->Branch("unpEmtf_BX", unpEmtf_BX, "unpEmtf_BX[nEmtf]/I");


  t->Branch("reco_pt",reco_pt,"reco_pt[nRecoMuon]/F");
  t->Branch("reco_eta",reco_eta,"reco_eta[nRecoMuon]/F");
  t->Branch("reco_phi",reco_phi,"reco_phi[nRecoMuon]/F");
  t->Branch("reco_eta_prop",reco_eta_prop,"reco_eta_prop[nRecoMuon]/F");
  t->Branch("reco_phi_prop",reco_phi_prop,"reco_phi_prop[nRecoMuon]/F");
  t->Branch("reco_eta_st2",reco_eta_st2, "reco_eta_st2[nRecoMuon]/F");
  t->Branch("reco_phi_st2",reco_phi_st2, "reco_phi_st2[nRecoMuon]/F");
  t->Branch("reco_charge",reco_charge,"reco_charge[nRecoMuon]/I");
  t->Branch("reco_isMediumMuon",reco_isMediumMuon,"reco_isMediumMuon[nRecoMuon]/I");
  t->Branch("reco_hasEMTFMatch",reco_hasEMTFMatch,"reco_hasEMTFMatch[nRecoMuon]/I");

  return t;
}

}

#endif
