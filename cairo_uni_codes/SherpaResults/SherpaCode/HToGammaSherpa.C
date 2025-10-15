#define HToGammaSherpa_cxx
#include "HToGammaSherpa.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TFile.h"
#include <math.h>
#include "TF2.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLorentzVector.h"
#include <time.h>
#include <iostream>
#include <vector>
using namespace std;
void HToGammaSherpa::Loop()
{
     	 int binMass   = 1200;
	 float minMass = 0.0;
	 float maxMass = 300.0;
  //==========================================My Histograms==================================
  TH1F *HiggsRecomassPDF		= new TH1F("HiggsRecomassPDF","",binMass,minMass,maxMass);
 //=======================================================================================
   if (fChain == 0) return;
   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;
//====================Generate event(s) [Event Loop]=====================
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      cout <<"========================================================================================================================================="<<endl;
      cout << "Event number "<<"  "<< jentry<<endl;      
      // if (Cut(ientry) < 0) continue;
      //==============================[Selection]==============================
      int IH=0,IG=0;
      for(unsigned i=0; i<iGen->size(); i++){
	if(fabs(idGen->at(i)) == 25)IH++;
	if(fabs(idGen->at(i)) == 22)IG++;
	if(fabs(idGen->at(i)) == 22
	   ){
	  iGflag1 =i;
	  GDau1++;
	  //cout << "Gamma (1)" <<"  "<<iGflag1<<endl;
	}//cut Gamma1
	for (unsigned j = 0; j<iGen->size(); j++){
	  TLorentzVector G2;
	  G2.SetPtEtaPhiE(Et2,Eta2,Phi2,En2);
	  if(fabs(idGen->at(j)) == 22 &&    
	     j != iGflag1){
	    iGflag2 =j;
	    GDau2++;
	    //cout << "Gamma (2)" <<"  "<<iGflag2<<endl;
	  }//cut Gamma2
	    if (GDau1 > 0 && GDau2 > 0){
	  Et1      = ptGen->at(iGflag1);
	  Phi1     = phiGen->at(iGflag1);
	  Eta1     = etaGen->at(iGflag1);
	  En1      = EnergyGen->at(iGflag1);
	  ID1      = idGen->at(iGflag1);
	  State1   = statusGen->at(iGflag1);
	  
	  Et2      = ptGen->at(iGflag2);
	  Phi2     = phiGen->at(iGflag2);
	  Eta2     = etaGen->at(iGflag2);
	  En2      = EnergyGen->at(iGflag2);
	  ID2      = idGen->at(iGflag2);
	  State2   = statusGen->at(iGflag2);
	  // cout << "G(1)" <<"  "<<iGflag1 <<"  "<<"&&"<<"  "<<"G(2)" <<"  "<<iGflag2<<endl;
	  TLorentzVector G1;
	  TLorentzVector G2;
		G1.SetPtEtaPhiE(Et1,Eta1,Phi1,En1);
		G2.SetPtEtaPhiE(Et2,Eta2,Phi2,En2);
		mRecoMass = (G1+G2).M();
		HiggsRecomassPDF->Fill(mRecoMass);
		 }//If both
	     GDau2 = 0.0;
	}//end of Gamma 2 loop
	GDau1 = 0.0;
      }//end of Gamma 1 loop
       cout << "Number of gamma is "<<"  "<<IG<<endl;
       cout << "Number of Higgs is "<<"  "<<IH<<endl;
       //cout << "The status of the Higgs is "<<"  "<<statusGen->at(25)<<endl;
    }//Event loop
      TFile *output = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/SherpaCode/file.root","recreate");
 output->cd();
 HiggsRecomassPDF->Draw();
 HiggsRecomassPDF->Write();
 output->Close();
    }
