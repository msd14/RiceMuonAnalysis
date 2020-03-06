// system include files
#include <memory>
#include <cmath>

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

#include "MagneticField/Engine/interface/MagneticField.h"
#include "TrackingTools/GeomPropagators/interface/Propagator.h"

#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "DataFormats/GeometrySurface/interface/Plane.h"
#include "DataFormats/GeometrySurface/interface/Cylinder.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/CSCGeometry/interface/CSCLayerGeometry.h"

//#define DataFormats_L1TMuon_EMTFTrack_h

static const float AVERAGE_GEM_Z(568.6); // [cm]

static const float AVERAGE_GE11_ODD_Z(568.6); // [cm]
static const float AVERAGE_GE11_EVEN_Z(568.6); // [cm]

static const float AVERAGE_GE21_LONG_Z(568.6); // [cm]
static const float AVERAGE_GE21_SHORT_Z(568.6); // [cm]

static const float AVERAGE_ME11_EVEN_Z(585); // [cm]
static const float AVERAGE_ME11_ODD_Z(615); // [cm]

static const float AVERAGE_ME21_EVEN_Z(820); // [cm]
static const float AVERAGE_ME21_ODD_Z(835); // [cm]

static const float AVERAGE_ME0_Z(568.6); // [cm]

static const float AVERAGE_DT1_R(440); // [cm] for Barrel
static const float AVERAGE_DT2_R(523);

//using reco::recHitContainer;

//using l1t::CSCSegmentCollection;
using reco::MuonCollection;
using l1t::RegionalMuonCandBxCollection;

class SimpleMuonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
public:
  explicit SimpleMuonAnalyzer(const edm::ParameterSet&);
  ~SimpleMuonAnalyzer() {}

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  /// general interface to propagation
  GlobalPoint propagateToZ(const GlobalPoint &inner_point, const GlobalVector &inner_vector, float z, int charge) const;

  /// general interface to propagation
  GlobalPoint propagateToR(const GlobalPoint &inner_point, const GlobalVector &inner_vector, float r, int charge) const;

  edm::EDGetTokenT<CSCSegmentCollection> cscSegmentToken_;
  edm::EDGetTokenT<MuonCollection> recoMuonToken_;
  edm::EDGetTokenT<RegionalMuonCandBxCollection> emtfToken_;
  edm::EDGetTokenT<std::vector<l1t::EMTFTrack>> emtfUnpTrack_token;

  edm::ESHandle<MagneticField> magfield_;
  edm::ESHandle<Propagator> propagator_;
  edm::ESHandle<Propagator> propagatorOpposite_;
  edm::ESHandle<CSCGeometry> csc_geom_;
  const CSCGeometry* cscGeometry_;

  TTree *tree_;
  MyNtuple ntuple_;

  bool verbose_;
};

SimpleMuonAnalyzer::SimpleMuonAnalyzer(const edm::ParameterSet& iConfig)
  :
  cscSegmentToken_(consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("cscSegments"))),
  recoMuonToken_(consumes<MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
  emtfToken_(consumes<RegionalMuonCandBxCollection>(iConfig.getParameter<edm::InputTag>("emtf"))),
  emtfUnpTrack_token(consumes<std::vector<l1t::EMTFTrack>>(iConfig.getParameter<edm::InputTag>("unpEmtf"))),
  verbose_(iConfig.getParameter<bool>("verbose"))
{
  tree_ = ntuple_.book(tree_, "Events");
}


// ------------ method called for each event  ------------
void
SimpleMuonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // Get the magnetic field
  iSetup.get<IdealMagneticFieldRecord>().get(magfield_);

  // Get the propagators
  iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAlong", propagator_);
  iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorOpposite", propagatorOpposite_);

  
  iSetup.get<MuonGeometryRecord>().get(csc_geom_);
  cscGeometry_ = &*csc_geom_;

  // initialize all variables
  ntuple_.init();

  using namespace edm;

  //const auto& cscSegments = iEvent.get(cscSegmentToken_);
  const auto& recoMuons = iEvent.get(recoMuonToken_);
  const auto& emtfTracks = iEvent.get(emtfToken_);
  const auto& emtfUnpTracks = iEvent.get(emtfUnpTrack_token);
 
  std::cout << recoMuons.size() << std::endl;

  // basic reco muon analysis

  if ((recoMuons.size() < 10) and (recoMuons.size() > 1)) {

    ntuple_.run = iEvent.id().run();
    ntuple_.lumi = iEvent.id().luminosityBlock();
    ntuple_.event = iEvent.id().event();

    ntuple_.nRecoMuon = recoMuons.size();

    //for(int i = 0; i < nMaxRecoMuons; i++) {
    for (std::size_t i=0; i<recoMuons.size(); i++) {
      const auto& recoMuon = recoMuons.at(i);

      // propagate the muon to the second muon endcap station
      const auto& muon_point = GlobalPoint(recoMuon.vertex().x(), recoMuon.vertex().y(), recoMuon.vertex().z());;
      const auto& muon_vector = GlobalVector(recoMuon.momentum().x(), recoMuon.momentum().y(), recoMuon.momentum().z());

      // pick a Z position
      const auto& zStation2( recoMuon.eta() > 0 ? AVERAGE_ME21_EVEN_Z : -AVERAGE_ME21_EVEN_Z );

      const GlobalPoint& prop_point(propagateToZ(muon_point, muon_vector,
                                               zStation2, recoMuon.charge()));
      if ( abs(recoMuon.eta()) < 2.4 and abs(recoMuon.eta()) > 1.2 ) {
	//std::cout << "Muon point (x,y,z):" << muon_point << std::endl;
	//std::cout << "zSt2:" << zStation2 << std::endl;
	//std::cout << "Prop point: " << prop_point << std::endl;
	//std::cout << "Total momentum: " << sqrt( pow(recoMuon.momentum().x(),2) + pow(recoMuon.momentum().y(),2) + pow(recoMuon.momentum().z(),2) ) << std::endl;
	//std::cout << "muon pt " << recoMuon.pt() << std::endl;
	//std::cout << "muon eta " << recoMuon.eta() << " " << "muon phi " <<recoMuon.phi() << std::endl;
	//std::cout << "muon prop eta " << prop_point.eta() << " " << "muon prop phi " <<prop_point.phi() << std::endl;
	//std::cout << "-----------------" << std::endl;
      }

      const auto& mumatches = recoMuon.matches();
      for (const auto& r : mumatches){
	if (r.detector()==2 and r.station()==2) {
	  //std::cout << "matches " << r.detector() << " " << r.station() << " " << r.x << " " << r.y << " " << CSCDetId(r.id) << std::endl;
	  const LocalPoint lp(r.x, r.y, 0.);
	  const GlobalPoint& gp = cscGeometry_->idToDet(CSCDetId(r.id))->surface().toGlobal(lp);
	  ntuple_.reco_eta_st2[i] = gp.eta();
	  ntuple_.reco_phi_st2[i] = gp.phi();
	  //std::cout << "St2 gp eta: " << gp.eta() << ", St2 gp phi: " << gp.phi() << std::endl;
	  break;
	}
      }

      //std::cout << "------------" << std::endl;
      // fill basic muon quantities
      ntuple_.reco_pt[i] = recoMuon.pt();
      ntuple_.reco_eta[i] = recoMuon.eta();
      ntuple_.reco_phi[i] = recoMuon.phi();
      ntuple_.reco_eta_prop[i] = prop_point.eta();
      ntuple_.reco_phi_prop[i] = prop_point.phi();
      ntuple_.reco_charge[i] = recoMuon.charge();
   
      // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
      ntuple_.reco_isMediumMuon[i] = int(muon::isMediumMuon(recoMuon));
    
      ntuple_.reco_hasEMTFMatch[i] = 0;
    }

    // basic l1 muon analysis
    for (std::size_t i=0; i<emtfUnpTracks.size(); i++) { 
      ntuple_.unpEmtf_Pt[i] = emtfUnpTracks.at(i).Pt();
      ntuple_.unpEmtf_Eta[i] = emtfUnpTracks.at(i).Eta();
      ntuple_.unpEmtf_Theta[i] = emtfUnpTracks.at(i).Theta();
      ntuple_.unpEmtf_Phi_glob[i] = emtfUnpTracks.at(i).Phi_glob();
      ntuple_.unpEmtf_Theta_fp[i] = emtfUnpTracks.at(i).Theta_fp();
      ntuple_.unpEmtf_Phi_fp[i] = emtfUnpTracks.at(i).Phi_fp();
      ntuple_.unpEmtf_Mode[i] = emtfUnpTracks.at(i).Mode();
      ntuple_.unpEmtf_Mode_neighbor[i] = emtfUnpTracks.at(i).Mode_neighbor();
      ntuple_.unpEmtf_BX[i] = emtfUnpTracks.at(i).BX();
    } 

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

	i++;
      }
    }
  
    ntuple_.nEmtf = i;
    // match reco muons to emtf tracks
 

    // fill tree
    tree_->Fill();
  }
}

GlobalPoint
SimpleMuonAnalyzer::propagateToZ(const GlobalPoint &inner_point,
                                const GlobalVector &inner_vec, float z, int charge) const
{
  Plane::PositionType pos(0.f, 0.f, z);
  Plane::RotationType rot;
  Plane::PlanePointer my_plane(Plane::build(pos, rot));

  FreeTrajectoryState state_start(inner_point, inner_vec, charge, &*magfield_);
  //if ( abs(recoMuon.eta()) < 2.4 and abs(recoMuon.eta()) > 1.2 ) {

  //std::cout <<"state_start  position "<< state_start.position()<<" momentum "<< state_start.momentum()<<" charge "<<state_start.charge() << std::endl;
 
  //if (state_start.hasError()) std::cout <<"state_start has error  "<< std::endl;

  TrajectoryStateOnSurface tsos(propagator_->propagate(state_start, *my_plane));
  //  if (!tsos.isValid()) std::cout <<" tsos not valid "<< std::endl;
  if (!tsos.isValid()) tsos = propagatorOpposite_->propagate(state_start, *my_plane);

  if (tsos.isValid()) return tsos.globalPosition();
  return GlobalPoint();
}

GlobalPoint
SimpleMuonAnalyzer::propagateToR(const GlobalPoint &inner_point,
                                 const GlobalVector &inner_vec, float R, int charge) const
{
  Cylinder::CylinderPointer my_cyl(Cylinder::build(Surface::PositionType(0,0,0), Surface::RotationType(), R));

  FreeTrajectoryState state_start(inner_point, inner_vec, charge, &*magfield_);

  TrajectoryStateOnSurface tsos(propagator_->propagate(state_start, *my_cyl));
  if (!tsos.isValid()) tsos = propagatorOpposite_->propagate(state_start, *my_cyl);

  if (tsos.isValid()) return tsos.globalPosition();
  return GlobalPoint();
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimpleMuonAnalyzer);
