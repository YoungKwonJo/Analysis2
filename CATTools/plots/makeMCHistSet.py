#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy


from loadHistograms import loadHistogramMC,loadHistogramDATA,mergesHistograms

def makeMCHistSet(histograms):
  ttV   = ["TTWlNu","TTWqq","TTZll","TTZqq"]
  ST    = ["STbt","STt","STbtW","STtW"]
  VV    = ["WW","WZ","ZZ"]
  WJets = ["WJets"]
  ZJets = ["DYJets","DYJets10"]
  ttH   = ["ttH2non","ttH2bb"]
  ######
  MG5ttbar = ["MG5ttbb","MG5ttb","MG5ttcc","MG5ttlf","MG5ttot"]
  AMCttbar = ["AMCttbb","AMCttb","AMCttcc","AMCttlf","AMCttot"]
  POWttbar = ["POWttbb","POWttb","POWttcc","POWttlf","POWttot"]
  
  upPOWttbar = ["upPOWttbb","upPOWttb","upPOWttcc","upPOWttlf","upPOWttot"]
  dwPOWttbar = ["dwPOWttbb","dwPOWttb","dwPOWttcc","dwPOWttlf","dwPOWttot"]
  ###################
  Bkg1   = ST+VV+WJets+ZJets
  MCtot1 = POWttbar+Bkg1
  MCtot2 = MG5ttbar+Bkg1
  MCtot3 = AMCttbar+Bkg1
  
  histograms2 = {}
  histograms2["ttbb"] = { "h1":histograms["POWttbb"],   "color":"#660000",  "label":"t#bar{t}+b#bar{b}      " }
  histograms2["ttb"]  = { "h1":histograms["POWttb"],    "color":"#ffcc00",  "label":"t#bar{t}+b        "      }
  histograms2["ttcc"] = { "h1":histograms["POWttcc"],   "color":"#cc6600",  "label":"t#bar{t}+c#bar{c}      " }
  histograms2["ttlf"] = { "h1":histograms["POWttlf"],   "color":"#ff0000",  "label":"t#bar{t}+lf       "      }
  histograms2["ttot"] = { "h1":histograms["POWttot"],   "color":"#ff6565",  "label":"t#bar{t} others"         }
  #histograms2["ttall"] = {"h1":histograms["POWttal"],   "color":"#ff6565",  "label":"t#bar{t} all"            }

  histograms2["Singlet"] = {"h1":mergesHistograms(ST,    histograms),    "color":"#ff00ff",  "label":"Single t"            } 
  histograms2["VV"]      = {"h1":mergesHistograms(VV,    histograms),    "color":"#ffffff",  "label":"VV            "      }
  histograms2["WJets"]   = {"h1":mergesHistograms(WJets, histograms),    "color":"#33cc33",  "label":"WJets      "         }
  histograms2["ZJets"]   = {"h1":mergesHistograms(ZJets, histograms),    "color":"#3366ff",  "label":"DYJets    "          }
  histograms2["ttV"]     = {"h1":mergesHistograms(ttV,   histograms),    "color":"#7676ff",  "label":"t#bar{t}V          " }
  histograms2["ttH"]     = {"h1":mergesHistograms(ttH,   histograms),    "color":"#7676ff",  "label":"t#bar{t}H         "  }
  
  histograms2["DATA"]    = {"h1":histograms["DATA"],                     "color":"#000000",  "label":"DATA "    ,"MarkerStyle":20,  "MarkerSize": 0.7        }

  histograms2["MCtot1"]  = {"h1":mergesHistograms(MCtot1,  histograms),  "color":"#afc6c6",  "label":""         ,"LineStyle": 1001,  "FillColor":"#afc6c6" } 
  histograms2["MCtot2"]  = {"h1":mergesHistograms(MCtot2,  histograms),  "color":"#59d354",  "label":"Madgraph" ,"LineStyle": 3   ,  "FillColor":"#ffffff" } 
  histograms2["MCtot3"]  = {"h1":mergesHistograms(MCtot3,  histograms),  "color":"#ff00ff",  "label":"MC@NLO"   ,"LineStyle": 2   ,  "FillColor":"#ffffff" } 
  ttbarlist = ["ttbb","ttb","ttcc","ttlf","ttot"]
  bkglist=["ttV","Singlet","VV","WJets","ZJets","ttV"]
  fullmc =["MCtot1"]
  others =["MCtot2","MCtot3"]
  plotSet = {"ttbars":ttbarlist, "bkg":bkglist, "fullmc":fullmc, "others":others}
  return histograms2,plotSet

def load1stHistograms(mon,step,Weight):
  from drellYanEstimation import DYsf 
  from mcsample_cfi import mcsamples
  histograms = {}
  for mc in mcsamples:
    histograms[mc["name"]]=loadHistogramMC(mc, mon,step,Weight,DYsf)
  histograms["DATA"]=loadHistogramDATA(mon,step,Weight)

  return histograms

######################################
######################################
######################################
def main():
  from monitors_cfi import monitors,monitors2d
  mon = monitors[7]
  histograms=load1stHistograms(mon,"S2")
  #c1 = TCanvas()
  #histograms["TTZqq"]["hMM"].Draw()
  #histograms["DATA"]["hEE"].Draw()
  histograms2,plotSet=makeMCHistSet(histograms)
  
  
  gROOT.SetStyle("Plain")
  gStyle.SetOptFit(1000)
  gStyle.SetOptStat("emruo")
  gStyle.SetOptStat(kFALSE)
  gStyle.SetPadTickY(1)
  gStyle.SetPadTickX(1)
  
  gROOT.ProcessLine(".L tdrStyle.C")
  setTDRStyle()
  c1 = TCanvas()
  #c1.Divide(2,2)
  c1.cd()
  histograms2["MCtot1"]["h1"]["hMM"].SetLineColor( TColor.GetColor(histograms2["MCtot1"]["color"]) )
  histograms2["MCtot1"]["h1"]["hMM"].Draw()
  #c1.cd(2)
  #histograms2["MCtot1"]["h1"]["hEE"].Draw()
  #c1.cd(3)
  #histograms2["MCtot1"]["h1"]["hME"].Draw()
  return c1,histograms2

if __name__ == "__main__":
  test=main()


