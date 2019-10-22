#ifndef RiceMuonAnalysis_SimpleMuonAnalyzer_MyNtuple
#define RiceMuonAnalysis_SimpleMuonAnalyzer_MyNtuple

#include "TTree.h"
#include <vector>
#include <string>

const int nMaxRecoMuons = 2;
const int nMaxEmtfMuons = 2;

namespace{

struct MyNtuple
{
  void init(); // initialize to default values
  TTree* book(TTree *t, const std::string & name = "trk_eff");

  Int_t lumi;
  Int_t run;
  Int_t event;

  float emtf_pt[nMaxEmtfMuons];
  float emtf_eta[nMaxEmtfMuons];
  float emtf_phi[nMaxEmtfMuons];
  float emtf_charge[nMaxEmtfMuons];

  float reco_pt[nMaxRecoMuons];
  float reco_eta[nMaxRecoMuons];
  float reco_phi[nMaxRecoMuons];
  float reco_charge[nMaxRecoMuons];
  int reco_isMediumMuon[nMaxRecoMuons];
  int reco_hasEMTFMatch[nMaxRecoMuons];
};

void MyNtuple::init()
{
  lumi = -99;
  run = -99;
  event = -99;

  for (unsigned i=0; i<nMaxEmtfMuons; ++i){
    emtf_pt[i]= -99;
    emtf_eta[i] = -99.;
    emtf_phi[i]= -99;
    emtf_charge[i] = - 99;
  }
  for (unsigned i=0; i<nMaxRecoMuons; ++i){
    reco_pt[i]= -99;
    reco_eta[i] = -99.;
    reco_phi[i]= -99;
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

  t->Branch("emtf_pt",emtf_pt,"emtf_pt[nMaxEmtfMuons]/F");
  t->Branch("emtf_eta",emtf_eta,"emtf_eta[nMaxEmtfMuons]/F");
  t->Branch("emtf_phi",emtf_phi,"emtf_phi[nMaxEmtfMuons]/F");
  t->Branch("emtf_charge",emtf_charge,"emtf_charge[nMaxEmtfMuons]/I");

  t->Branch("reco_pt",reco_pt,"reco_pt[nMaxRecoMuons]/F");
  t->Branch("reco_eta",reco_eta,"reco_eta[nMaxRecoMuons]/F");
  t->Branch("reco_phi",reco_phi,"reco_phi[nMaxRecoMuons]/F");
  t->Branch("reco_charge",reco_charge,"reco_charge[nMaxRecoMuons]/I");
  t->Branch("reco_isMediumMuon",reco_isMediumMuon,"reco_isMediumMuon[nMaxRecoMuons]/F");
  t->Branch("reco_hasEMTFMatch",reco_hasEMTFMatch,"reco_hasEMTFMatch[nMaxRecoMuons]/F");

  return t;
}

}

#endif
