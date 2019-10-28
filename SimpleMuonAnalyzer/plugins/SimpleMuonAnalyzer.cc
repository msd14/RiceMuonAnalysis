// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCandFwd.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCand.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "RiceMuonAnalysis/SimpleMuonAnalyzer/plugins/MyNtuple.h"

using reco::MuonCollection;
using l1t::RegionalMuonCandBxCollection;

class SimpleMuonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleMuonAnalyzer(const edm::ParameterSet&);
  ~SimpleMuonAnalyzer() {}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<MuonCollection> recoMuonToken_;
  edm::EDGetTokenT<RegionalMuonCandBxCollection> emtfToken_;

  TTree *tree_;
  MyNtuple ntuple_;

  bool verbose_;
};

SimpleMuonAnalyzer::SimpleMuonAnalyzer(const edm::ParameterSet& iConfig)
 :
  recoMuonToken_(consumes<MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
  emtfToken_(consumes<RegionalMuonCandBxCollection>(iConfig.getParameter<edm::InputTag>("emtf"))),
  verbose_(iConfig.getParameter<bool>("verbose"))
{
  tree_ = ntuple_.book(tree_, "Events");
}

// ------------ method called for each event  ------------
void
SimpleMuonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   const auto& recoMuons = iEvent.get(recoMuonToken_);
   const auto& emtfTracks = iEvent.get(emtfToken_);

   ntuple_.run = iEvent.id().run();
   ntuple_.lumi = iEvent.id().luminosityBlock();
   ntuple_.event = iEvent.id().event();

   ntuple_.nEmtf = recoMuons.size();

   // basic reco muon analysis
   for(int i = 0; i < nMaxRecoMuons; i++) {

     const auto& recoMuon = recoMuons.at(i);

     // fill basic muon quantities
     ntuple_.reco_pt[i] = recoMuon.pt();
     ntuple_.reco_eta[i] = recoMuon.eta();
     ntuple_.reco_phi[i] = recoMuon.phi();
     ntuple_.reco_charge[i] = recoMuon.charge();
     // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
     ntuple_.reco_isMediumMuon[i] = int(muon::isMediumMuon(recoMuon));
   }

   // basic l1 muon analysis
   int i = 0;
   for (int bx = emtfTracks.getFirstBX(); bx <= emtfTracks.getLastBX(); bx++ ){

     if ( bx != 0) continue;

     for (auto cand = emtfTracks.begin(bx); cand != emtfTracks.end(bx); ++cand ){

       const auto& emtfTrack = *cand;

       // https://github.com/cms-sw/cmssw/blob/master/DataFormats/L1TMuon/interface/RegionalMuonCand.h
       ntuple_.emtf_pt[i] = emtfTrack.hwPt()*0.5;
       ntuple_.emtf_eta[i] = emtfTrack.hwEta()*0.010875;
       ntuple_.emtf_phi[i] = emtfTrack.hwPhi()*2*M_PI/576;
       ntuple_.emtf_charge[i] = 1-2*emtfTrack.hwSign();

       // Matthew: add quality to the branch

       i++;
     }
   }
   // match reco muons to emtf tracks
   // Matthew: please add your code here...

   // fill tree
   tree_->Fill();
}
//define this as a plug-in
DEFINE_FWK_MODULE(SimpleMuonAnalyzer);
