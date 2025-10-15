#include <stdio.h> 
#include "TProfile.h"
#include "TProfile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TF1.h"
#include "TF2.h"
#include "TMath.h"
#include <math.h>
#include <string>
#include "TGraph.h"
using std::string;
void THToGammaPDFPlots(){
        Double_t yerrscale =30 ;
	gROOT->Reset();
  	gROOT->SetStyle("Plain");
 	gStyle->SetStatFormat("5.3f");
  	gStyle->SetFitFormat("5.3f"); 
  	gStyle->SetOptFit(1111);
  	gStyle->SetOptDate(0);
  	gStyle->SetOptTitle(1);
  	gStyle->SetPadBorderMode(0);
  	gStyle->SetCanvasColor(0); //(10);
  	gStyle->SetPadLeftMargin(0.20);
  	gStyle->SetPadBottomMargin(0.15);
  	gStyle->SetPalette(0);
  	TPaveLabel pl;
  	TLatex lt;
  	lt.SetTextAlign(12);
  	lt.SetTextSize(0.03);
  	lt.SetTextColor(1);
	TCanvas* ccc1=new TCanvas("ccc1","Correlation",500,500); 
	const int n = 10;
	double ex[n],eypp[n],eypp_PDF[n];
 	TMultiGraph *mg = new TMultiGraph();
//===================================================================
	double x[n]={1000,700,500,400,300,200,100,50,20,10};//Number of generated Higgs (== Number of generated Events)
  	gPad->SetTopMargin(0.12);
  	gPad->SetLeftMargin(0.15);
  	gPad->SetFillColor(0);
  	gPad->SetTickx();
  	gPad->SetTicky();
  	gPad->SetGridy();
  	gPad->SetGridx(); 	
	ccc1->cd(1);	
//============(Histograms for Correlations for MSTRW2004nlo=======================================
	// double ypp[n]={36978.4,23621,14730,15261.1,13273.8,7643.08,4149.37,1280.12,460.031,405.406};//p-p PDF2
	//double ypp[n]={14693.6,10195.8,7463.37,5866.34,4255.71,2548.3,987.417,336.434,215.955,140.769}; //p-p PDF2 ISR
	// double ypp[n]={14711.6,10871.8,7471.65,5866.33,4255.69,2548.26,987.774,331.75,216.798,140.769}; //p-p PDF2 ISR New reading
	//double ypp[n]={12265.4,8965.66,6045.25,4226.58,3759.74,2470.86,1273.26,647.056,99.6934,96.6113};//P-P PDF2 FSR
	   double ypp[n]= {10599,6913.02,4926.73,4143.34,3126.07,2214.17,1018.37,565.886,329.326,202.616}; //P-P PDF2 ISR-FSR
	for(int i= 0; i< n; i++){
	 ex[i]= 0.0;   //sqrt(x[i]);
	 eypp[i]= yerrscale*sqrt(ypp[i]);
				}
	  TGraphErrors *graph_pp= new TGraphErrors(n,x,ypp,ex,eypp);
	  graph_pp->SetMarkerColor(kBlue);
	  graph_pp->SetMarkerStyle(21);
	 	 graph_pp->Fit("pol1");
		 graph_pp->GetFunction("pol1")->SetLineColor(kBlue);
		 graph_pp->GetFunction("pol1")->SetLineStyle(9);
    	  graph_pp->Draw("AP");
 	  mg->Add(graph_pp);
//============(Histograms for Correlations CTEQ66=======================================
	  //double ypp_PDF[n]={39650.1,27398.2,19919.8,16103.7,12408,7810.42,3915.56,1796.63,954.963,619.307};//p-p PDF
	  //double ypp_PDF[n]={20563.7,14157.8,10251.4,8369.05,6092.61,4085.17,2371.54,1067.55,220.008,180.3};// P-P PDF ISR
	  // double ypp_PDF[n]={20563.9,14157.9,10251.4,8369.03,6092.61,4085.15,2221.77,1010.04,401.993,177.63};// P-P PDF ISR New reading
	  // double ypp_PDF[n]={15840.2,11540.2,7974.12,6330.36,4491.64,3119.19,1476.45,771.168,500,194.42}; //p-p PDF FSR
	   double ypp_PDF[n]={16398.1,12177.7,7779.86,6596.98,5133.35,3607.39,1816.39,995.914,461.395,288.609}; //p-p PDF ISR-FSR
	for(int i= 0; i< n; i++){
	 eypp_PDF[i]= yerrscale*sqrt(ypp_PDF[i]);
				}
    TGraphErrors *graph_pp_PDF= new TGraphErrors(n,x,ypp_PDF,ex,eypp_PDF);
	graph_pp_PDF->SetMarkerColor(kRed);
	graph_pp_PDF->SetMarkerStyle(20);
	graph_pp_PDF->Fit("pol1");
	graph_pp_PDF->GetFunction("pol1")->SetLineColor(kRed);
	graph_pp_PDF->GetFunction("pol1")->SetLineStyle(1);

//============(Adding the Two lines together)===============================
	mg->Add(graph_pp_PDF);
	mg->Draw("AP");
         mg->GetXaxis()->SetTitle("Number of Generated Events");//in case of Integrated
	 //mg->GetXaxis()->SetTitle("Number of Generated Events");//in case of real
          //mg->GetXaxis()->SetTitle("Exact Number of Higgs");//in case of real 
          mg->GetYaxis()->SetTitle("Integrated Invariant Mass Higgs");//in case of Integrated
 	//mg->GetYaxis()->SetTitle("Exact Number of Higgs");//in case of real
	//graph_pp_PDF->Draw("AP");   
//===========================================================================
   ccc1->Update();
    TPaveStats *stats1 = (TPaveStats*)graph_pp->GetListOfFunctions()->FindObject("stats");
    TPaveStats *stats2 = (TPaveStats*)graph_pp_PDF->GetListOfFunctions()->FindObject("stats");
   stats1->SetTextColor(kBlue);
   stats2->SetTextColor(kRed);
   stats1->SetX1NDC(0.7); stats1->SetX2NDC(0.85); stats1->SetY1NDC(0.25);stats1->SetY2NDC(0.4);
   stats2->SetX1NDC(0.7); stats2->SetX2NDC(0.85); stats2->SetY1NDC(0.45);stats2->SetY2NDC(0.6);
   ccc1->Modified();
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  TPaveText* tText1 = new TPaveText(0.2, 0.90, 0.4, 0.95, "brNDC");
  tText1->SetBorderSize(0);
  tText1->SetFillColor(0);
  tText1->SetFillStyle(0);
  // TText *t1 = tText1->AddText("P#bar{P} Collision [ISR=on FSR=on] #sqrt{s}=13 Tev");
  TText *t1 = tText1->AddText("PP Collision [ISR=off FSR=off] #sqrt{s}=13 Tev");
  tText1->SetTextSize(0.030);
  tText1->Draw("Same");
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  TPaveText* tText1 = new TPaveText(0.0002, 0.60, 0.5, 0.5, "brNDC");
  tText1->SetBorderSize(0);
  tText1->SetFillColor(0);
  tText1->SetFillStyle(0);
  TText *t1 = tText1->AddText("Sherpa 2.1.0 @NLO ");
  tText1->SetTextSize(0.030);
  tText1->Draw("Same");  
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++
TLegend *leg = new TLegend(0.55, 0.50, 0.30, 0.60);
    leg->AddEntry(graph_pp_PDF,"CTEQ66","lep");
    leg->AddEntry(graph_pp,"MSTRW2004nlo","lep");
    leg->SetBorderSize(0.0);
    leg->SetMargin(0.4);
    leg->SetFillColor(0);
    leg->SetFillStyle(10);
    leg->SetLineColor(0);
    leg->SetTextSize(0.03); 
    leg->Draw(); 
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
//	ccc1->Print("HTOGamma-PDF","pdf");

}
