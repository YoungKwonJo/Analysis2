#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

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

def addLegendCMS():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"Preliminary")
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.25)
  tex2.SetY(0.968)
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
  chtitle.SetY(0.91)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)
  chtitle.SetTextSizePixels(24)

  return chtitle

gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()


#ROOT.gROOT.Macro("rootlogon.C")
#h1_DYJets_MET_S4mm
#HN = "nBJet30M"
HN = "jet3CSV_jet4CSV"
from mcsample_cfi import mcsamples,datasamples 
lumi = 2110. 
Step = "S6"

#histograms = ["name":"name","hist": ]
histograms = {}
f= TFile.Open("hist_roofit.root")
#for name in mcnames:
for mc in mcsamples:
  name = mc['name']
  color = mc['color'] 
  h1 = f.Get("h2_"+name+"_"+HN+"_"+Step+"mm").Clone("h2_"+name+"_"+Step+"LL")
  h2 = f.Get("h2_"+name+"_"+HN+"_"+Step+"ee")
  h3 = f.Get("h2_"+name+"_"+HN+"_"+Step+"em")
  if h1.Integral()>0 :  h1.Scale(mc['cx']*lumi)
  if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
  if h3.Integral()>0 :  h3.Scale(mc['cx']*lumi)
  h1.Add(h2)
  h1.Add(h3)
  histograms[name]={"h1":copy.deepcopy(h1),"color":color,"exp":h1.Integral()}
  #print "FINAL "+name

#for datesmaples
for i in range(1):
  name_ = "DATA"
  color = mc['color'] 
  h1 = f.Get("h2_MuMu1_"+HN+"_"+Step+"mm").Clone("h2_"+name_+"_"+Step+"LL")
  h1.Reset()
  for j in range(1,4):
    h11 = f.Get("h2_MuMu"+str(j)+"_"+HN+"_"+Step+"mm")
    h2 = f.Get("h2_ElEl"+str(j)+"_"+HN+"_"+Step+"ee")
    h3 = f.Get("h2_MuEl"+str(j)+"_"+HN+"_"+Step+"em")
    h1.Add(h11)
    h1.Add(h2)
    h1.Add(h3)
  histograms[name_]={"h1":copy.deepcopy(h1),"color":kBlack,"exp":h1.Integral()}

print str(type(histograms))
print str(histograms["POWttbb"]["color"])
print str(histograms["POWttbb"]["exp"])
print ""
print str(histograms["DATA"]["color"])
print str(histograms["DATA"]["exp"])

signals1= ['POWttbb', 'POWttb']
signals2= ['POWttcc','POWttc', 'POWttlf']#, 'POWttot']
backgrounds1= ["POWttot"]
backgrounds2= ['TTWlNu', 'TTWqq', 'TTZll', 'TTZqq', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ', 'DYJets']
higgs= ['ttH2non', 'ttH2bb']

bkghist = histograms['POWttot']["h1"].Clone("bkghist")
bkghist.Reset()

ttcclfhist = histograms['POWttot']["h1"].Clone("ttcclfhist")
ttcclfhist.Reset()
for hh in signals2:
  h = histograms[hh]["h1"]
  ttcclfhist.Add(h)
histograms["POWttcclf"]={"h1":copy.deepcopy(ttcclfhist),"color":kOrange,"exp":ttcclfhist.Integral()}

for hh in backgrounds2:
  h = histograms[hh]["h1"]
  bkghist.Add(h)
  #print "FINAL "+hh
histograms["bkg"]={"h1":copy.deepcopy(bkghist),"color":kGray,"exp":bkghist.Integral()}


histograms["POWttcc"]["h1"].Add(histograms["POWttc"]["h1"])

n_ttbb = histograms["POWttbb"]["exp"]
n_ttb  = histograms["POWttb"]["exp"]
#n_tt2b = histograms["POWtt2b"]["exp"]
n_ttcc = histograms["POWttcc"]["exp"]+histograms["POWttc"]["exp"]
#n_ttc = histograms["POWttc"]["exp"]
n_ttlf = histograms["POWttlf"]["exp"]
n_ttcclf = histograms["POWttcclf"]["exp"]
n_ttot = histograms["POWttot"]["exp"]
n_bkg = histograms["bkg"]["exp"]
n_data = histograms["DATA"]["exp"]

n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf
n_ttbar = n_ttjj+n_ttot

print "n_ttbb:"+str(n_ttbb)
print "n_ttb:"+str(n_ttb)
#print "n_tt2b:"+str(n_tt2b)
#print "n_ttc:"+str(n_ttc)
print "n_ttcc:"+str(n_ttcc)
print "n_ttlf:"+str(n_ttlf)
print "n_ttot:"+str(n_ttot)
print "n_bkg:"+str(n_bkg)
print "n_data:"+str(n_data)


rttbb = n_ttbb/n_ttjj
rttb  = n_ttb/n_ttjj
#rtt2b = n_tt2b/n_ttjj
rttcc = (n_ttcc)/n_ttjj

x=RooRealVar("x","x",bkghist.GetXaxis().GetXmin(),bkghist.GetXaxis().GetXmax()) 
y=RooRealVar("y","y",bkghist.GetYaxis().GetXmin(),bkghist.GetYaxis().GetXmax()) 

RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
#Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);

fsig   =RooRealVar(    "fsig",                "fsig",           rttbb, 0.0, 0.2) 
fsig2  =RooFormulaVar("fsig2",               "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )
#fsig3  =RooFormulaVar("fsig3",               "fsig3","@0/@1*@2",RooArgList(fsig2,RttbbReco,RttbReco,Rtt2bReco) )
fsigcc =RooRealVar(  "fsigcc",              "fsigcc",           rttcc, 0.0, 0.5) 
k      =RooRealVar(       "k","normalization factor",           1, 0.5, 1.5) 

nttjj =RooRealVar(    "nttjj","number of ttjj events",                            n_ttjj , n_ttjj, n_ttjj)
knttjj=RooFormulaVar("knttjj","number of ttjj events after fitting","k*nttjj",    RooArgList(k,nttjj) )
nttot =RooRealVar(    "nttot","number of ttot events",                            n_ttot , n_ttot, n_ttot)
knttot=RooFormulaVar("knttot","number of ttot events after fitting","k*nttot",    RooArgList(k,nttot) )
nbkg  =RooRealVar(     "nbkg","number of background events",                      n_bkg , n_bkg, n_bkg)
knbkg=RooFormulaVar("knbkg","number of background events after fitting","k*nbkg", RooArgList(k,nbkg) )

nttcc  =RooRealVar(     "nttcc","number of ttcc events",                            n_ttcc , n_ttcc, n_ttcc)
#nttbar =RooRealVar(    "nttbar","number of ttbar events",                           n_ttbar , n_ttbar, n_ttbar)
#knttbar=RooFormulaVar("knttbar","number of ttbar events after fitting","k*nttbar",  RooArgList(k,nttbar) )


#histogram
data    = RooDataHist("data",    "data set with (x)",   RooArgList(x, y), histograms["DATA"]["h1"])
ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   RooArgList(x, y), histograms["POWttbb"]["h1"])
ttb     = RooDataHist("ttb",     "ttb  set with (x)",   RooArgList(x, y), histograms["POWttb"]["h1"])
#tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",  RooArgList(x, y), histograms["POWtt2b"]["h1"])
ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   RooArgList(x, y), histograms["POWttcc"]["h1"] )
ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   RooArgList(x, y), histograms["POWttlf"]["h1"])
ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", RooArgList(x, y), histograms["POWttcclf"]["h1"])
ttot    = RooDataHist("ttot",    "ttot set with (x)",   RooArgList(x, y), histograms["POWttot"]["h1"])
bkg     = RooDataHist("bkg",     "bkg  set with (x)",   RooArgList(x, y), histograms["bkg"]["h1"])

#print "ttbar type: "+str(type(ttbar))
#print "rooArglist(x):"+str(type(RooArgList(x)))

#pdf
ttbbpdf      = RooHistPdf("ttbbpdf",     "ttbbpdf",      RooArgSet(RooArgList(x,y)), ttbb)
ttbpdf       = RooHistPdf("ttbpdf",      "ttbpdf",       RooArgSet(RooArgList(x,y)), ttb)
#tt2bpdf      = RooHistPdf("tt2bpdf",     "tt2bpdf",     RooArgSet(RooArgList(x,y)), tt2b)
ttccpdf      = RooHistPdf("ttccpdf",     "ttccpdf",      RooArgSet(RooArgList(x,y)), ttcc)
ttlfpdf      = RooHistPdf("ttlfpdf",     "ttlfpdf",      RooArgSet(RooArgList(x,y)), ttlf)
ttcclfpdf    = RooHistPdf("ttcclfpdf",   "ttcclfpdf",    RooArgSet(RooArgList(x,y)), ttcclf)
ttotpdf      = RooHistPdf("ttotpdf",     "ttotpdf",      RooArgSet(RooArgList(x,y)), ttot)
bkgpdf       = RooHistPdf("bkgpdf",      "bkgpdf",       RooArgSet(RooArgList(x,y)), bkg)

#for separate ttcc
#model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, tt2bpdf, ttccpdf, ttlfpdf), RooArgList(fsig,fsig2,fsigcc))
#for merge ttcc+ttlf
model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, ttcclfpdf), RooArgList(fsig,fsig2))
#model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf),              RooArgList(knttjj,knttot,knbkg)) # k*bkg
model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf),              RooArgList(knttjj,knttot,nbkg)) # fixing bkg
model2.fitTo(data)
#model2.fitTo(ttlf)

recoR      = fsig.getVal()
recoRerror = fsig.getError()

kVal      = k.getVal()
kValerror = k.getError()
  
print "FINAL: ttbb Rreco = "+ str(recoR)+" +- "+str(recoRerror)
print "FINAL: k = "+str(kVal)+" +- "+str(kValerror) 

cR10 = TCanvas("R10", "R", 1)#500, 500)
nll = model2.createNLL(data)
#nll = model2.createNLL(ttlf)
#RooMinuit(nk1).migrad() 
RFrame = fsig.frame()
nll.plotOn(RFrame,RooFit.ShiftToZero()) 
RFrame.SetMaximum(4.);RFrame.SetMinimum(0)
RFrame.GetXaxis().SetTitle("nttbb/nttjj as r")
RFrame.SetTitle("")
RFrame.Draw()

line = TLine(RFrame.GetXaxis().GetXmin() ,0.5,RFrame.GetXaxis().GetXmax(),0.5)
line.SetLineColor(kRed)
line.Draw()

lineTbb = TLine(rttbb,RFrame.GetMaximum(),rttbb,0)
lineTbb.SetLineStyle(2)
lineTbb.Draw()

#lineTbb2 = TLine(0.0652239,RFrame.GetMaximum(),0.0652239,0)
#lineTbb2.SetLineStyle(3)
#lineTbb2.Draw()

l1 = make_legend(0.49,0.76,0.93,0.88)
l1.AddEntry(lineTbb,"prefit: r="+str(round(rttbb*10000)/10000),"l")
l1.AddEntry(RFrame,"fit: r="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","l")
l1.SetTextSize(0.04)
l1.SetFillColor(0)
l1.SetLineColor(0)
l1.Draw()

pt = addLegendCMS()
pt2 = addDecayMode("LL")
pt.Draw()
pt2.Draw()

cR10.Print("R.eps")
cR10.Print("R.png")
################
################
################
################
cR00 = TCanvas("R00", "R", 1)#500, 500)
nllK = model2.createNLL(data)
#nll = model2.createNLL(ttlf)
#RooMinuit(nk1).migrad() 
RFrameK = k.frame()
nllK.plotOn(RFrameK,RooFit.ShiftToZero()) 
RFrameK.SetMaximum(4.);RFrameK.SetMinimum(0)
RFrameK.GetXaxis().SetTitle("k")
RFrameK.SetTitle("")
RFrameK.Draw()

lineK = TLine(RFrameK.GetXaxis().GetXmin() ,0.5,RFrameK.GetXaxis().GetXmax(),0.5)
lineK.SetLineColor(kRed)
lineK.Draw()

lineTbbK = TLine(1,RFrameK.GetMaximum(),1,0)
lineTbbK.SetLineStyle(2)
lineTbbK.Draw()

#lineTbb2 = TLine(0.0652239,RFrame.GetMaximum(),0.0652239,0)
#lineTbb2.SetLineStyle(3)
#lineTbb2.Draw()

l1K = make_legend(0.49,0.76,0.93,0.88)
l1K.AddEntry(lineTbbK,"prefit: k=1.0","l")
l1K.AddEntry(RFrameK,"fit: k="+str(round(kVal*10000)/10000)+" #pm "+str(round(kValerror*10000)/10000)+"","l")
l1K.SetTextSize(0.04)
l1K.SetFillColor(0)
l1K.SetLineColor(0)
l1K.Draw()

ptK = addLegendCMS()
pt2K = addDecayMode("LL")
ptK.Draw()
pt2K.Draw()

cR00.Print("K.eps")
cR00.Print("K.png")


################
################
################
###########
cR11 = TCanvas("R11", "R", 1)# 500, 500)
xframe = x.frame()
data.plotOn(xframe, RooFit.DataError(RooAbsData.SumW2) ) 
model2.paramOn(xframe, RooFit.Layout(0.65,0.9,0.9) )
model2.plotOn(xframe)
chi2 = xframe.chiSquare(2)
ndof = xframe.GetNbinsX()
print "chi2 = "+ str(chi2)
print "ndof = "+ str(ndof)
xframe.Draw()

pt3 = addLegendCMS()
pt4 = addDecayMode("LL")
pt3.Draw()
pt4.Draw()

cR11.Print("jet3CSV.eps")
cR11.Print("jet3CSV.png")

cR12 = TCanvas("R12", "R", 1)#500, 500)
yframe = y.frame()
data.plotOn(yframe, RooFit.DataError(RooAbsData.SumW2) ) 
model2.paramOn(yframe, RooFit.Layout(0.65,0.9,0.9) )
model2.plotOn(yframe)
chi22 = yframe.chiSquare(2)
ndof2 = yframe.GetNbinsX()
print "chi2 = "+ str(chi22)
print "ndof = "+ str(ndof2)
yframe.Draw()

pt5=addLegendCMS()
pt6=addDecayMode("LL")
pt5.Draw()
pt6.Draw()

cR12.Print("jet4CSV.eps")
cR12.Print("jet4CSV.eps")



