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
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Candidate/interface/Candidate.h"



//******************************************************************************
//                           Class declaration
//******************************************************************************

class FilterSample2GenMu : public edm::EDFilter
{
public:
  explicit FilterSample2GenMu(const edm::ParameterSet&);
  ~FilterSample2GenMu();

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
  edm::EDGetTokenT<reco::GenParticleCollection > m_genParticles;
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
FilterSample2GenMu::FilterSample2GenMu(const edm::ParameterSet& iConfig)
{
  m_genParticles      = consumes<reco::GenParticleCollection >(edm::InputTag("genParticles"));
}


FilterSample2GenMu::~FilterSample2GenMu()
{
}

//
// member functions
//

// ------------ method called for each event  ------------
bool
FilterSample2GenMu::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  edm::Handle<reco::GenParticleCollection > genParticles;
  iEvent.getByToken(m_genParticles, genParticles); 
  const reco::GenParticleCollection& candidateC = *genParticles.product();

  double muon_eta[8];
  double muon_phi[8];
  
  int nMuons = 0;
  int j=0;
  //Pick out muons (Id=+/- 13) that are final state muons (status=1) in the endcap system (1.2<|eta|<2.4).
  //Store their eta and phis into a local array to calculate dR in the next step.
  for (std::size_t i=0 ; i<candidateC.size() ; i++) {
    if (std::abs(candidateC[i].pdgId()) != 13) continue;
    if (candidateC[i].status() != 1) continue;
    if (std::abs(candidateC[i].eta()) < 1.2) continue;
    if (std::abs(candidateC[i].eta()) >= 2.4) continue;

    muon_eta[j] = candidateC[i].eta();
    muon_phi[j] = candidateC[i].phi();

    nMuons++;
    j++;
  }

  
  // Skip event if less than two muons
  if (nMuons < 2) {
    std::cout << "Less than 2 muons in event." << std::endl;
    return false;
  }

  std::cout << nMuons << std::endl;
  // Skip event if more than two muons in barrel
  int nMuonsBarrel = 0;
  for (int iMu = 0; iMu < nMuons; iMu++){
    if ((std::abs(muon_eta[iMu]) < 0.9) and (std::abs(muon_eta[iMu]) != 0.000)) {
      nMuonsBarrel++;
    }
  }

  
  if (nMuonsBarrel > 2) {
    std::cout << "More than 2 muons in barrel." << std::endl;
    return false;
  }

  
  // Skip event if more than two muons in either endcap.
  int nMuonsEndcapP = 0;
  int nMuonsEndcapM = 0;
  for (int iMu = 0; iMu < nMuons; iMu++){
    if ((0.9 <= muon_eta[iMu]) and (muon_eta[iMu] <= 2.4)) {
      nMuonsEndcapP++;
    }
    if ((-0.9 >= muon_eta[iMu]) and (muon_eta[iMu] >= -2.4)) {
      nMuonsEndcapM++;
    }
  }

  if (nMuonsEndcapP > 2 or nMuonsEndcapM > 2) {
    std::cout << "More than 2 muons in an endcap." << std::endl;
    return false;
  }

  
  int muPair_endcap1 = 0;
  int muPair_endcap2 = 0;
  // We will accept events that have at least one muon pair passing through the same endcap with dR<0.5.
  // If there are two muon pairs in the event, require they pass through different endcap.
  for (int iMu = 0; iMu < nMuons; iMu++) {
    for (int jMu = iMu+1; jMu < nMuons; jMu++) {

      if (iMu == jMu) continue;

      // build a pair
      double dR = reco::deltaR(muon_eta[iMu], muon_phi[iMu], muon_eta[jMu], muon_phi[jMu]);
      if ((dR < 0.5) and (muon_eta[iMu] != 0.000)) {

        if (muon_eta[iMu] > 0.9) {
          muPair_endcap1++;
        } 
        if (muon_eta[iMu] < -0.9) { 
          muPair_endcap2++;
        }
      }
    }
  }

  if ((muPair_endcap1 == 0) and (muPair_endcap2 == 0)) {
    std::cout << "No muon pairs in either endcap." << std::endl;
    return false;
  }
  
  // Allow up to 2 good muon pairs, if they are in different endcaps
  if ((muPair_endcap1 > 1) or (muPair_endcap2 > 1)) {
    std::cout << "More than one pair in an endcap." << std::endl;
    return false;
  }
  
  std::cout << "Good event!" << std::endl;
  std::cout << "Pairs in endcap+:" << muPair_endcap1 << "Pairs in endcap-:" << muPair_endcap2 << std::endl;
  return true;
}

// ------------ method called once each job just before starting event loop  ------------
void
FilterSample2GenMu::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
FilterSample2GenMu::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
void
FilterSample2GenMu::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void
FilterSample2GenMu::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
FilterSample2GenMu::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
FilterSample2GenMu::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FilterSample2GenMu::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//Indentation change
//define this as a plug-in
DEFINE_FWK_MODULE(FilterSample2GenMu);