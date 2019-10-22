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
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"
#include "RiceMuonAnalysis/SimpleMuonAnalyzer/plugins/MyNtuple.h"

using reco::TrackCollection;
using l1t::EMTFTrackCollection;

class SimpleMuonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleMuonAnalyzer(const edm::ParameterSet&);
  ~SimpleMuonAnalyzer() {}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<TrackCollection> recoMuonToken_;
  edm::EDGetTokenT<EMTFTrackCollection> emtfToken_;

  TTree *tree_;
  MyNtuple ntuple_;
};

SimpleMuonAnalyzer::SimpleMuonAnalyzer(const edm::ParameterSet& iConfig)
 :
  recoMuonToken_(consumes<TrackCollection>(iConfig.getParameter<edm::InputTag>("recoMuon"))),
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

   for(int i = 0; i < nMaxRecoMuons; i++) {

     const auto& recoMuon = recoMuons.at(i);

     // fill basis muon quantities
     ntuple_.reco_pt[i] =
     ntuple_.phi = t.momentum().phi();
     ntuple_.eta = t.momentum().eta();
     ntuple_.charge = t.charge();
   }

   for(const auto& emtf : iEvent.get(emtfToken_) ) {
      // do something with track parameters, e.g, plot the charge.
      // int charge = track.charge();
   }

   // fill tree
   tree_->Fill();
}
//define this as a plug-in
DEFINE_FWK_MODULE(SimpleMuonAnalyzer);
