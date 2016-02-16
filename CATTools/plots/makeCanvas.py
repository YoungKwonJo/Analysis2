#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy


###################################################
###################################################
###################################################
###################################################
def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0)
  leg.SetLineColor(1)
  leg.SetTextFont(62)
  leg.SetTextSize(0.03)

  leg.SetBorderSize(1)
  leg.SetLineStyle(1)
  leg.SetLineWidth(1)
  leg.SetLineColor(0)

  return leg

def addLegendLumi():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"CMS #sqrt{s} = 13TeV, L = 2.26 fb^{-1}")
  title.SetNDC()
  title.SetTextAlign(12)
  title.SetX(0.20)
  title.SetY(0.83)
  title.SetTextFont(42)
  title.SetTextSize(0.05)
  title.SetTextSizePixels(24)
  title.Draw()

  return title

def addLegendCMS():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"Preliminary")
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.25)
  tex2.SetY(0.93)
  tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  tex2.Draw()

  return tex2

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("em")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("mm")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("ee")>-1 : ll2="e^{#mp}e^{#pm} channel"

  chtitle = TLatex(-20.,50.,ll2)
  chtitle.SetNDC()
  chtitle.SetTextAlign(12)
  chtitle.SetX(0.20)
  chtitle.SetY(0.75)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)
  chtitle.SetTextSizePixels(24)

  return chtitle

def myCanvas(name):
  c1 = TCanvas( name, '',1)#, 500, 500 )
  return c1
def myPad1(name):
  pad1 = TPad(name, "",0,0.3,1,1)
  pad1.SetPad(0.01, 0.23, 0.99, 0.99)
  pad1.SetTopMargin(0.1)
  pad1.SetRightMargin(0.04)

  return pad1

def myPad2(name):
  pad2 = TPad(name, "",0,0,1,0.3)
  pad2.SetPad(0.01, 0.02, 0.99, 0.3)
  #gStyle.SetGridWidth(0.5)
  gStyle.SetGridWidth(1)
  gStyle.SetGridColor(14)
  pad2.SetGridx()
  pad2.SetGridy()
  pad2.SetTopMargin(0.05)
  pad2.SetBottomMargin(0.4)
  pad2.SetRightMargin(0.04)

  return pad2


##############################
##############################
##############################
##############################
##############################
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
  canvasname=mon["name"]+step
  c1 = myCanvas(canvasname) 
  #c1 = TCanvas()
  c1.Divide(1,2)
  pad1 = myPad1(canvasname+"pad1")
  pad2 = myPad2(canvasname+"pad2")
  pad1.Draw()
  pad1.cd()
  legx1 = 0.8
  wid=0.12
  legx2 = 0.67
  leg  = make_legend(legx1,0.64, legx1+wid,0.88)
  leg2 = make_legend(legx2,0.68, legx2+wid,0.88)
  leg3 = make_legend(legx1,0.54, legx1+wid,0.63)
  if isLogy : pad1.SetLogy()

  ########################
  ########################
  ########################
  DATA   =  AddHist(decay,histograms2["DATA"])
  MCtot1 =  AddHist(decay,histograms2["MCtot1"])
  MCtot2 =  AddHist(decay,histograms2["MCtot2"])
  MCtot3 =  AddHist(decay,histograms2["MCtot3"])
  hs = StackHist(decay,histograms2,plotSet)

  if isLogy : 
    DATA.SetMinimum( 0.04 )
    DATA.SetMaximum( 100.0*max(DATA.GetMaximum(),MCtot1.GetMaximum()) )
  else :
    DATA.SetMaximum( 2.4*max(DATA.GetMaximum(),MCtot1.GetMaximum()) )

  DATA.Draw()
  hs.Draw("same,hist")
  MCtot1.Draw("same")
  MCtot2.Draw("same")
  MCtot3.Draw("same")
  DATA.Draw("same")

  ########################
  ########################
  pt = addLegendLumi()#lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode(decay)
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  pad1.Modified()
  c1.cd()
  pad2.Draw()
  pad2.cd()
  ########################

  ########################
  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  return c1,pad1,pad2,histograms2,hs,MCtot1,MCtot2,MCtot3,DATA,pt,pt2,pt3

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
  mon = monitors[11]
  aaa = {}
  aaa[0]=aCavas(mon,"S4","LL",True,"csvweight")
  aaa[1]=aCavas(mon,"S5","LL",True,"csvweight")
  aaa[2]=aCavas(mon,"S6","LL",True,"csvweight")

  return aaa


if __name__ == "__main__":
  test=main()


