#include <stdio>
#include <fstream>
#include <iostream>
#include "TList.h"
#include "TCollection.h"
#include "TObjString.h"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH2.h"
#include "TRandom.h"
#include "Riostream.h"
#include "TString.h"
//#include "TMath.h"
using namespace std; 
Double_t f1(Double_t *x,Double_t *par){     //Gauss (peak 3)
Double_t arg=0;
if (par[2]!=0) arg=(x[0]-par[1])/par[2];
Double_t fitval=par[0]*TMath::Exp(-0.5*arg*arg);
return fitval;
			               }

Double_t f2(Double_t *x,Double_t *par){     //Exponential*pol1 (3)
Double_t fitval=(par[0]+par[1]*x[0])*TMath::Exp(-par[2]*x[0]);
return fitval;
                                      }

Double_t f3(Double_t *x,Double_t *par){     //Lorentz (peak 3)
Double_t arg=0;
arg=(x[0]-par[1]);
Double_t fitval=(par[0]/TMath::Pi())*par[2]/(4.0 * arg*arg + par[2]*par[2]);
return fitval;
                                      }

Double_t f4(Double_t *x,Double_t *par){     //Extreme (peak 3)
Double_t arg=0;
if (par[2]!=0) arg=(x[0]-par[1])/par[2];
Double_t fitval=par[0]*TMath::Exp(-TMath::Exp(-arg) - arg + 1);
return fitval;
                                      }

Double_t ftotal(Double_t *x,Double_t *par){  // Peak function + Exponential*pol1
Double_t fitval=f4(x,&par[0])+f2(x,&par[3]);
return fitval;
                                          }
//============================================================
void fittinvm() {
	 int binMass   = 1200;
	 float minMass = 0.0;
	 float maxMass = 300.0;
Double_t para[6];
//Double_t initpara[6] = {20.,125.,4.5e-1,1.55491e+03,-3.27382e-02,1.42408e-02};//By M.H
 Double_t initpara[6] = {60.,125.,4.5e-1,1.55453e+03,-4.2752e-02,1.42408e-02};
TVirtualFitter::SetDefaultFitter("Minuit2");
TFile *file1 = new TFile("/Users/ahmedqamesh/Desktop/Master/HToGamma/PythiaResults/PythiaRootPDF2-MSTRW2004nlo/HTOGammaPDF2-Analyze-1000-Sherpa-ISR.root");
//TH1F *invmass=(TH1F*)file1->Get("HiggsRecomass");
TH1F *invmass=(TH1F*)file1->Get("HiggsRecomassPDF");
TF1 *func1=new TF1("fitf1",f4,100,150,3);
TF1 *func2=new TF1("fitf2",f2,100,150,3);
TF1 *func3=new TF1("fitf3",ftotal,100,150,6);
TH1F *histofunc= new TH1F("function", "func", binMass, minMass, maxMass);
TH1F *histores = invmass->Clone();
func3->SetParameters (initpara);
invmass->Fit("fitf3","M","",100,150);
func3->GetParameters(para);
func1->SetParameters (para);
func2->SetParameters (&para[3]);
for (int i=0;i<binMass;i++)
 {
   Double_t x1=invmass->GetBinCenter(i);
   Double_t y1=func2->Eval(x1);
   histofunc->SetBinContent(i, y1);
 }
histores->Add(histofunc, -1);

func1->SetNpx(50000);
func2->SetNpx(5000);
func3->SetNpx(50000);
Int_t np = 1000;
double *x=new double[np];
double *w=new double[np];
func1->CalcGaussLegendreSamplingPoints(np,x,w,1e-15);    //Peak Integral = 38848.7
                                                         //Gauss Peak Integral = 898.748
func2->CalcGaussLegendreSamplingPoints(np,x,w,1e-15);

TH1F *func3hist =func3->GetHistogram();
TH1F *residhist = invmass->Clone();
Double_t peakint = TMath::Abs(func2->IntegralFast(np,x,w, 100.0,150.0) - invmass->Integral(300,450)); //Peak Integral = 38719.5, 57370
Double_t Gpeakint= func1->IntegralFast(np,x,w,100.0,150.0);

cout << "Peak Integral = " << peakint<< endl;
cout << "Peak Integral = " <<histores->Integral(124.0,126.0)<< endl;
invmass->GetYaxis()->SetRangeUser(0.0, 2000);
invmass->GetYaxis()->SetTitle("Events/GeV");
invmass->GetXaxis()->SetTitle("M_{#\gamma#\gamma} [GeV]");
invmass->Draw();

func3->Draw("SAME");

histofunc->Draw();
histores->Draw();

TCanvas *can1=new TCanvas("can1", "GammaH", 600, 400);
//can1->SetFillColor(33);
//can1->SetFrameFillColor(41);
can1->SetGrid();
invmass->Draw();


func1->SetLineWidth(2.5);
func1->SetLineColor(kMagenta);
func2->SetLineColor(kRed);

//func1->Draw("SAME");
//func2->Draw("SAME");
func3->SetLineColor(kOrange);
func3->Draw("SAME");


                   }
