//=================Making a normalized Histograms=======================
//======================including root libraries================
#include "TCanvas.h"
#include "TProfile.h"
#include "TLegend.h"
#include "TROOT.h"
#include "TGClient.h"
#include "TVirtualPad.h"
#include "TLine.h" 
#include "TPostScript.h"
#include "TH1.h"
#include "TH2.h"
#include "TAxis.h"
#include "TMath.h" 
#include "TROOT.h" 
#include "TStyle.h" 
#include "TFile.h"
#include "TAxis.h"
#include "TProfile.h"
#include "TProfile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TF1.h"
#include "TF2.h"
#include <string>
using namespace std;
using std::string;
void Stuck(){
//================including style options=====================
  gROOT->Reset();
  gROOT->SetStyle("Default");
  gStyle->SetOptFit(0111);
  gStyle->SetOptDate(0);
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetPadBorderMode(0);
  // gStyle->SetCanvasColor(0);
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadBottomMargin(0.15);
  gStyle->SetPalette(0);
  TPaveLabel pl;
  TLatex lt;
  lt.SetTextFont(70);
  lt.SetTextAlign(12);
  lt.SetTextSize(0.07);
  lt.SetTextColor(1);
//====Including normalization parameters====================
	float intLumiValue = 46.011;  //pb-1
//==================Canvas Definition=============================
  TCanvas *c1 = new TCanvas("c1","Stuck",800.0,800.0);
	char textpro1[100],textNDF1[100],textRatio1[100];
	c1->SetFillColor(0);
  	c1->cd(1);
  gPad->SetTopMargin(0.12);
  gPad->SetLeftMargin(0.15);
  gPad->SetFillColor(0);
  gPad->SetTickx();
  gPad->SetTicky();
  gPad->SetGridx();
  gPad->SetGridy();
  gPad->SetLogy();
       	 int binMass   = 1200;
	 float minMass = 0.0;
	 float maxMass = 300.0;
//=======Definition of Histograms=================================
	TH1F* hMassTTbaremu1          = new TH1F("hMassTTbaremu1","",1200,0,300);
	TH1F* hMassTTbaremu2          = new TH1F("hMassTTbaremu2","",1200,0,300);
	THStack *hs 		      = new THStack("hs","Stacked 1 D histogram");
//======Getting the first Histogram =============================
   TFile *f1 = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/SherpaResults/SherpaRootFiles/SherpaRootPDF-CTEQ66/HTOGammaPDF-Analyze-1000-Sherpa-ISR.root","READ");
  //TFile *f1 = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/PythiaResults/PythiaRootPDF-CTEQ66/HTOGammaPDF-ffbar2WW-ISR-1000.root","READ");	
  hMassTTbaremu1->Add(HiggsRecomassPDF);
  	int nb1           = hMassTTbaremu1->Integral();
  		cout<<"nb1   = "<<nb1<<endl;
  float SigmaMC1      = 5025.2; //fb 
  float AccepEff1     = (float)nb1/(2964086.0); //old 19941756.0
  float IntLumia1   = (float)nb1/(SigmaMC1*AccepEff1);
  //	cout<<"IntLumia1   = "<<IntLumia1<<endl;
		 float weight1       = intLumiValue/IntLumia1; 
  hMassTTbaremu1->SetLineStyle(0);
  hMassTTbaremu1->SetLineColor(1);
  hMassTTbaremu1->SetLineWidth(2);
  // hMassTTbaremu1->SetFillColor(12);//8
  hMassTTbaremu1->SetMarkerStyle(20);
  hMassTTbaremu1->SetMarkerSize(0.875);
  hMassTTbaremu1->GetYaxis()->SetRangeUser(20.,20000.0);
  hMassTTbaremu1->GetYaxis()->SetTitle("Events/GeV");
  hMassTTbaremu1->GetXaxis()->SetTitle("M_{#\gamma#\gamma} [GeV]");
  hMassTTbaremu1->Draw();
//=========Getting the second histogram=============================
  // TFile *f2 = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/PythiaResults/PythiaRootPDF2-MSTRW2004nlo/HTOGammaPDF2-ffbar2WWs-1000-ISR.root","READ");
  TFile *f2 = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/SherpaResults/SherpaRootFiles/SherpaRootPDF2-MSTRW2004nlo/HTOGammaPDF2-Analyze-1000-Sherpa-ISR.root","READ");
  hMassTTbaremu2->Add((HiggsRecomassPDF));
  	int nb2           = hMassTTbaremu2->Integral();
  		cout<<"nb2   = "<<nb2<<endl;
  float SigmaMC2      = 80.95; //fb 
  float AccepEff2     = (float)nb2/(681900); 
  float IntLumia2   = (float)nb2/(SigmaMC2*AccepEff2);
  //	cout<<"IntLumia2   = "<<IntLumia2<<endl;
  float weight2       = intLumiValue/IntLumia2; 
  hMassTTbaremu2->SetLineStyle(0);
  hMassTTbaremu2->SetLineColor(2);
  hMassTTbaremu2->SetLineWidth(2);
  //hMassTTbaremu2->SetFillColor(29);//2
  hMassTTbaremu2->SetMarkerStyle(20);
  hMassTTbaremu2->SetMarkerSize(0.875);
  hMassTTbaremu2->GetYaxis()->SetRangeUser(20.,20000.0);
  // hMassTTbaremu1->GetYaxis()->SetMaximum(2000);
   hMassTTbaremu2->Draw("Same");
   //=======================Print Header Information================================
TPaveText* tText1 = new TPaveText(0.70, 0.90, 0.90, 0.95, "brNDC");
  tText1->SetBorderSize(0);
  tText1->SetFillColor(0);
  tText1->SetFillStyle(0);
  TText *t1 = tText1->AddText("p-p Collision (13 TeV)");
  tText1->Draw();

  TPaveText* tText2 = new TPaveText(0.4, 0.95, 0.6, 0.85, "brNDC");
  tText2->SetBorderSize(0);
  tText2->SetFillColor(0);
  tText2->SetFillStyle(0);
  TText *t1 = tText2->AddText("MC");
  // tText2->Draw();
//============================Identify a label for each Histogram===========================
TLegend *leg = new TLegend(0.50, 0.85, 0.8, 0.77);
//leg->AddEntry(hMassTTbaremu2,"Sherpa 2.1.0 @NLO ","l");
//leg->AddEntry(hMassTTbaremu1,"PYTHIA 8","l");
//leg->AddEntry(hMassTTbaremu1,"PYTHIA 8-CTEQ66 ","l");
//leg->AddEntry(hMassTTbaremu2,"PYTHIA 8 -MSTRW2004nlo","l");
leg->AddEntry(hMassTTbaremu1,"Sherpa 2.1.0 @NLO -CTEQ66 ","l");
leg->AddEntry(hMassTTbaremu2,"Sherpa 2.1.0 @NLO-MSTRW2004nlo","l");
 leg->SetBorderSize(0.0);
 leg->SetMargin(0.4);
 leg->SetFillColor(0);
 leg->SetFillStyle(10);
 leg->SetLineColor(0);
 leg->SetTextSize(0.03); 
 leg->Draw(); 
//==============Saving the informations==============================
	c1->Update();
        c1->SaveAs("HTOgamma-final-pythia-invmassplo.png");
}

