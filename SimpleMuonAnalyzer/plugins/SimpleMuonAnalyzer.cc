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
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "RiceMuonAnalysis/SimpleMuonAnalyzer/plugins/MyNtuple.h"

using reco::MuonCollection;
using l1t::EMTFTrackCollection;

class SimpleMuonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleMuonAnalyzer(const edm::ParameterSet&);
  ~SimpleMuonAnalyzer() {}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<MuonCollection> recoMuonToken_;
  edm::EDGetTokenT<EMTFTrackCollection> emtfToken_;

  TTree *tree_;
  MyNtuple ntuple_;
};

SimpleMuonAnalyzer::SimpleMuonAnalyzer(const edm::ParameterSet& iConfig)
 :
  recoMuonToken_(consumes<MuonCollection>(iConfig.getParameter<edm::InputTag>("recoMuon"))),
  emtfToken_(consumes<EMTFTrackCollection>(iConfig.getParameter<edm::InputTag>("emtfTrack")))
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

   // basic reco muon analysis
   for(int i = 0; i < nMaxRecoMuons; i++) {

     const auto& recoMuon = recoMuons.at(i);

     // fill basic muon quantities
     ntuple_.reco_pt[i] = recoMuon.pt();
     ntuple_.reco_eta[i] = recoMuon.eta();
     ntuple_.reco_phi[i] = recoMuon.phi();
     ntuple_.reco_charge[i] = recoMuon.charge();
     ntuple_.reco_charge[i] = int(muon::isMediumMuon(recoMuon));
   }

   // basic l1 muon analysis
   for(int i = 0; i < nMaxEmtfMuons; i++) {

     const auto& emtfTrack = emtfTracks.at(i);

     ntuple_.emtf_pt[i] = emtfTrack.Pt();
     ntuple_.emtf_eta[i] = emtfTrack.Eta();
     ntuple_.emtf_phi[i] = emtfTrack.Phi_glob();
     ntuple_.emtf_charge[i] = emtfTrack.Charge();
   }

   // match reco muons to emtf tracks
   // Matthew: please add your code here...

   // fill tree
   tree_->Fill();
}
//define this as a plug-in
DEFINE_FWK_MODULE(SimpleMuonAnalyzer);
