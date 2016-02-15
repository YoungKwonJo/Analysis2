#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

def StackHist(channel, histograms2, plotSet):
  hs = THStack("hs","")
  ls=["hMM","hEE","hME"]
  if channel=="MM":   ls = ["hMM"]
  if channel=="EE":   ls = ["hEE"]
  if channel=="ME":   ls = ["hME"]
  if channel=="MMEE": ls = ["hMM","hEE"]

  for aa in plotSet["ttbars"]:
    h={}
    for bb in ls: 
      if len(h.keys())==0:
        h[aa]=copy.deepcopy(histograms2[aa]["h1"][bb])
      else :
        h[aa].Add(copy.deepcopy(histograms2[aa]["h1"][bb]))
    h[aa].SetFillColor( TColor.GetColor(histograms2[aa]["color"]) )
    hs.Add(copy.deepcopy(h[aa]))
  for aa in plotSet["bkg"]:
    h={}
    for bb in ls: 
      if len(h.keys())==0:
        h[aa]=copy.deepcopy(histograms2[aa]["h1"][bb])
      else :
        h[aa].Add(copy.deepcopy(histograms2[aa]["h1"][bb]))
    h[aa].SetFillColor( TColor.GetColor(histograms2[aa]["color"]) )
    hs.Add(copy.deepcopy(h[aa]))

  return hs

def AddHist(channel,histograms):
  ls=["hMM","hEE","hME"]
  if channel=="MM":   ls = ["hMM"]
  if channel=="EE":   ls = ["hEE"]
  if channel=="ME":   ls = ["hME"]
  if channel=="MMEE": ls = ["hMM","hEE"]
  h={}
  for bb in ls: 
    if len(h.keys())==0:
      h["aa"]=copy.deepcopy(histograms["h1"][bb])
    else :
      h["aa"].Add(copy.deepcopy(histograms["h1"][bb]))
  if "color"       in histograms.keys(): h["aa"].SetLineColor( TColor.GetColor(histograms["color"])  )
  if "LineStyle"   in histograms.keys(): h["aa"].SetLineStyle(  histograms["LineStyle"]   )
  if "MarkerStyle" in histograms.keys(): h["aa"].SetMarkerStyle(histograms["MarkerStyle"] )
  if "MarkerSize"  in histograms.keys(): h["aa"].SetMarkerSize( histograms["MarkerSize"]  )
  if "FillColor"   in histograms.keys(): h["aa"].SetFillColor(  TColor.GetColor(histograms["FillColor"]) )

  return h["aa"]


######################################
######################################
######################################
def aCavas(mon,step,decay,isLogy,Weight):
  from makeMCHistSet import makeMCHistSet,load1stHistograms
  histograms=load1stHistograms(mon,step,Weight)
  histograms2,plotSet=makeMCHistSet(histograms)

  #decay = "LL"
  #isLogy = False
  
  c1 = TCanvas()
  #c1.Divide(2,2)
  c1.cd()
  if isLogy : c1.SetLogy()

  DATA   =  AddHist(decay,histograms2["DATA"])
  MCtot1 =  AddHist(decay,histograms2["MCtot1"])
  MCtot2 =  AddHist(decay,histograms2["MCtot2"])
  MCtot3 =  AddHist(decay,histograms2["MCtot3"])
  hs = StackHist(decay,histograms2,plotSet)

  if isLogy : 
    DATA.SetMinimum( 0.04 )
    DATA.SetMaximum( 100.0*DATA.GetMaximum() )
  else :
    DATA.SetMaximum( 2.4*DATA.GetMaximum() )

  DATA.Draw()
  hs.Draw("same,hist")
  MCtot1.Draw("same")
  MCtot2.Draw("same")
  MCtot3.Draw("same")
  DATA.Draw("same")
  #hs.Draw("hist")
  #c1.cd(2)
  #histograms2["MCtot1"]["h1"]["hEE"].Draw()
  #c1.cd(3)
  #histograms2["MCtot1"]["h1"]["hME"].Draw()
  return c1,histograms2,hs,MCtot1,MCtot2,MCtot3,DATA

def main():
  gROOT.SetStyle("Plain")
  gStyle.SetOptFit(1000)
  gStyle.SetOptStat("emruo")
  gStyle.SetOptStat(kFALSE)
  gStyle.SetPadTickY(1)
  gStyle.SetPadTickX(1)
  
  gROOT.ProcessLine(".L tdrStyle.C")
  setTDRStyle()

  from monitors_cfi import monitors,monitors2d
  #mon = monitors[34]
  mon = monitors[5]
  aaa=aCavas(mon,"S4","LL",True,"csvweight")
  bbb=aCavas(mon,"S5","LL",True,"csvweight")
  ccc=aCavas(mon,"S6","LL",True,"csvweight")

  return aaa,bbb,ccc


if __name__ == "__main__":
  test=main()


