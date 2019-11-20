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
#include "DataFormats/Math/interface/normalizedPhi.h"
#include "L1Trigger/L1TMuon/interface/MicroGMTConfiguration.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"

#include "RiceMuonAnalysis/SimpleMuonAnalyzer/plugins/MyNtuple.h"

//using reco::recHitContainer;
using reco::MuonCollection;
using l1t::RegionalMuonCandBxCollection;

class SimpleMuonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleMuonAnalyzer(const edm::ParameterSet&);
  ~SimpleMuonAnalyzer() {}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<CSCSegmentCollection> cscSegmentToken_;
  edm::EDGetTokenT<MuonCollection> recoMuonToken_;
  edm::EDGetTokenT<RegionalMuonCandBxCollection> emtfToken_;
  
  
  TTree *tree_;
  MyNtuple ntuple_;

  bool verbose_;
};

SimpleMuonAnalyzer::SimpleMuonAnalyzer(const edm::ParameterSet& iConfig)
  :
  cscSegmentToken_(consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("cscSegments"))),
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
  // initialize all variables
  ntuple_.init();

  using namespace edm;
 
  const auto& recoMuons = iEvent.get(recoMuonToken_);
  const auto& emtfTracks = iEvent.get(emtfToken_);

  ntuple_.run = iEvent.id().run();
  ntuple_.lumi = iEvent.id().luminosityBlock();
  ntuple_.event = iEvent.id().event();

  ntuple_.nRecoMuon = recoMuons.size();
  
  reco::Track recoTrack;

  // basic reco muon analysis
  for(int i = 0; i < nMaxRecoMuons; i++) {

    const auto& recoMuon = recoMuons.at(i);

    
    if (recoMuon.isGlobalMuon()) {
      const auto& recoTrack = recoMuon.globalTrack();
    }

    else if (recoMuon.isStandAloneMuon()) {
      const auto& recoTrack = recoMuon.outerTrack();
    }
    
    else {
      continue;
    }
    
    const auto& trackrechits = recoTrack.recHits();
    
//     for (const auto& r : trackrechits){
//       std::cout << r->type() << endl;
//       //r->geoId();
//     }
    
    
    // fill basic muon quantities
    ntuple_.reco_pt[i] = recoMuon.pt();
    ntuple_.reco_eta[i] = recoMuon.eta();
    ntuple_.reco_phi[i] = recoMuon.phi();
    ntuple_.reco_charge[i] = recoMuon.charge();
   
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
    ntuple_.reco_isMediumMuon[i] = int(muon::isMediumMuon(recoMuon));
    
    ntuple_.reco_hasEMTFMatch[i] = 0;
  }

  // basic l1 muon analysis
  
  int count = 0;

  int i = 0;
  for (int bx = emtfTracks.getFirstBX(); bx <= emtfTracks.getLastBX(); bx++ ){

    if ( bx != 0) continue;

    for (auto cand = emtfTracks.begin(bx); cand != emtfTracks.end(bx); ++cand ){

      const auto& emtfTrack = *cand;

      // https://github.com/cms-sw/cmssw/blob/master/DataFormats/L1TMuon/interface/RegionalMuonCand.h
      ntuple_.emtf_pt[i] = emtfTrack.hwPt()*0.5;
      ntuple_.emtf_eta[i] = emtfTrack.hwEta()*0.010875;
      int globalphi = l1t::MicroGMTConfiguration::calcGlobalPhi(emtfTrack.hwPhi(),
                                                                emtfTrack.trackFinderType(),
                                                                emtfTrack.processor());
      ntuple_.emtf_phi[i] = normalizedPhi(globalphi*2*M_PI/576);
      ntuple_.emtf_charge[i] = 1-2*emtfTrack.hwSign();
      ntuple_.emtf_quality[i] = emtfTrack.hwQual();
      
      count+=1;

      i++;
    }
  }
  
  ntuple_.nEmtf = i;
  // match reco muons to emtf tracks
 
      
  // fill tree
  tree_->Fill();
}
//define this as a plug-in
DEFINE_FWK_MODULE(SimpleMuonAnalyzer);
