// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"

//******************************************************************************
//                           Class declaration
//******************************************************************************

class FilterSample2RecoMu : public edm::EDFilter
{
public:
  explicit FilterSample2RecoMu(const edm::ParameterSet&);
  ~FilterSample2RecoMu();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() ;
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void endRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  //****************************************************************************
  //          RECO LEVEL VARIABLES, BRANCHES, COUNTERS AND SELECTORS
  //****************************************************************************

  // Labels to access
  edm::EDGetTokenT<reco::MuonCollection > m_muons;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
FilterSample2RecoMu::FilterSample2RecoMu(const edm::ParameterSet& iConfig)
{
  m_muons           = consumes<reco::MuonCollection >(edm::InputTag("muons"));
}


FilterSample2RecoMu::~FilterSample2RecoMu()
{
}

//
// member functions
//

// ------------ method called for each event  ------------
bool
FilterSample2RecoMu::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  edm::Handle<reco::MuonCollection > muons;
  iEvent.getByToken(m_muons, muons);
  const reco::MuonCollection& muonC = *muons.product();

  // two muons
  if (muonC.size() == 2) {

    // kinematic cuts
    if (muonC[0].pt() > 2 and
        muonC[1].pt() > 2 and
        1.2 <= std::abs(muonC[0].eta()) and
        std::abs(muonC[0].eta()) <= 2.4 and
        1.2 <= std::abs(muonC[1].eta()) and
        std::abs(muonC[1].eta()) <= 2.4) {

      // require both muons to be in the same endcap
      if (muonC[0].eta() * muonC[1].eta() > 0) {

        // require the two muons to be sufficiently close (dR<0.5)
        if (reco::deltaR(muonC[0].eta(), muonC[0].phi(),
                         muonC[1].eta(), muonC[1].phi()) < 0.5) {
          return true;
        }
      }
    }
  }
  return false;
}


// ------------ method called once each job just before starting event loop  ------------
void
FilterSample2RecoMu::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
FilterSample2RecoMu::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
void
FilterSample2RecoMu::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void
FilterSample2RecoMu::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
FilterSample2RecoMu::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
FilterSample2RecoMu::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FilterSample2RecoMu::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//Indentation change
//define this as a plug-in
DEFINE_FWK_MODULE(FilterSample2RecoMu);
