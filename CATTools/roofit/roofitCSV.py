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
  tex2.SetY(0.97)
  tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  #tex2.Draw()

  return tex2

def addLegend(GEN):
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,GEN)
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.70)
  tex2.SetY(0.97)
  #tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  #tex2.Draw()

  return tex2

def addLegend2(text, xxx, yyy):
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,text)
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(xxx)
  tex2.SetY(yyy)
  #tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)

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
  chtitle.SetY(0.85)
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

def loadHistogram(arg1, arg2):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
  from mcsample_cfi import mcsamples,datasamples 
  lumi = 2110. 
  Step = "S6"
  
  freeTTB  = False
  freeTTCC = False
  if int(arg1)==1 : freeTTB=True
  if int(arg1)==2 : freeTTCC=True
  if int(arg1)==3 : 
    freeTTCC=True
    freeTTB=True
  
  GEN="MG5"
  if int(arg2)==1 : GEN="POW"
  if int(arg2)==2 : GEN="AMC"
  
  #histograms = ["name":"name","hist": ]
  histograms = {}
  
  f = TFile.Open("hist_all.root")
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
  
    h11 = f.Get("h1_"+name+"_"+HN1+"_"+Step+"mm").Clone("h11_"+name+"_"+Step+"LL")
    h21 = f.Get("h1_"+name+"_"+HN1+"_"+Step+"ee")
    h31 = f.Get("h1_"+name+"_"+HN1+"_"+Step+"em")
    h11.Add(h21)
    h11.Add(h31)
  
    ci = TColor.GetColor(mc['color'])  
    h11.SetLineColor(ci)
  
    h12 = f.Get("h1_"+name+"_"+HN2+"_"+Step+"mm").Clone("h12_"+name+"_"+Step+"LL")
    h22 = f.Get("h1_"+name+"_"+HN2+"_"+Step+"ee")
    h32 = f.Get("h1_"+name+"_"+HN2+"_"+Step+"em")
    h12.Add(h21)
    h12.Add(h31)
  
    ci = TColor.GetColor(mc['color'])  
    h12.SetLineColor(ci)
  
    histograms[name]={"h1":copy.deepcopy(h1),"color":color,"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12)}
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
  print str(histograms[GEN+"ttbb"]["color"])
  print str(histograms[GEN+"ttbb"]["exp"])
  print ""
  print str(histograms["DATA"]["color"])
  print str(histograms["DATA"]["exp"])
  
  #signals1= [GEN+'ttbb', GEN+'ttb']
  signals2= [GEN+'ttcc', GEN+'ttlf']#, GEN+'ttot']
  backgrounds1= [GEN+"ttot"]
  backgrounds2= ['TTWlNu', 'TTWqq', 'TTZll', 'TTZqq', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ', 'DYJets']
  higgs= ['ttH2non', 'ttH2bb']
  
  bkghist = histograms[GEN+'ttot']["h1"].Clone("bkghist")
  bkghist.Reset()
  
  ttcclfhist = histograms[GEN+'ttot']["h1"].Clone("ttcclfhist")
  ttcclfhist.Reset()
  for hh in signals2:
    h = histograms[hh]["h1"]
    ttcclfhist.Add(h)
  histograms[GEN+"ttcclf"]={"h1":copy.deepcopy(ttcclfhist),"color":kOrange,"exp":ttcclfhist.Integral()}
  
  for hh in backgrounds2:
    h = histograms[hh]["h1"]
    bkghist.Add(h)
    #print "FINAL "+hh
  histograms["bkg"]={"h1":copy.deepcopy(bkghist),"color":kGray,"exp":bkghist.Integral()}
  f.Close()
  return histograms, freeTTB, freeTTCC,GEN

##############################################
##############################################
##############################################
##############################################
def resultPrint(result, freeTTB, freeTTCC, GEN):

  print "FINAL: ----------------------   "
  print "FINAL: MC:"+ str(GEN)
  fsig = result["fsig"]
  rttbb = result["rttbb"]
  recoR      = fsig.getVal()
  recoRerror = fsig.getError()
  print "FINAL: prefit: R="+str(round(rttbb*10000)/10000)
  print "FINAL: $R = "+ str(round(recoR*10000)/10000)+" \pm "+str(round(recoRerror*10000)/10000)+"$"
  
  recoR2=1.
  recoR2error=0.0
  if freeTTB:
    print "FINAL: freeTTB : "+str(freeTTB)
    fsig2 = result["fsig2"]
    rttb = result["rttb"]
    recoR2      = fsig2.getVal()
    recoR2error = fsig2.getError()
    print "FINAL: prefit: R2="+str(round(rttb*10000)/10000)
    print "FINAL: $R2 = "+ str(round(recoR2*10000)/10000)+" \pm "+str(round(recoR2error*10000)/10000)+"$"
  else:
    print "FINAL: freeTTB : "+str(freeTTB)
    fsig2con = result["fsig2con"]
    recoR2      = fsig2con.getVal()
    rttb = result["rttb"]
    #recoR2error = fsig2con.getError()
    print "FINAL: prefit: R2="+str(round(rttb*10000)/10000)
    print "FINAL: $R2 = "+ str(round(recoR2*10000)/10000)#+" \pm "+str(round(recoR2error*10000)/10000)+"$"
  
  recoRcc=1.
  recoRccerror=0.0
  if freeTTCC:
    print "FINAL: freeTTCC : "+str(freeTTCC)
    fsigcc = result["fsigcc"]
    rttcc = result["rttcc"]
    recoRcc      = fsigcc.getVal()
    recoRccerror = fsigcc.getError()
    print "FINAL: prefit: Rcc="+str(round(rttcc*10000)/10000)
    print "FINAL: $Rcc = "+ str(round(recoRcc*10000)/10000)+" \pm "+str(round(recoRccerror*10000)/10000)+"$"
  else:
    print "FINAL: freeTTCC : "+str(freeTTCC)
    #recoRcc      = fsigcc.getVal()
    #recoRccerror = fsigcc.getError()
    rttcc = result["rttcc"]
    print "FINAL: prefit: Rcc="+str(round(rttcc*10000)/10000)
    #print "FINAL: $Rcc = "+ str(round(recoRcc*10000)/10000)+" \pm "+str(round(recoRccerror*10000)/10000)+"$"
  
  
  k = result["k"]
  kVal      = k.getVal()
  kValerror = k.getError()
  print "FINAL: $k = "+str(round(kVal*10000)/10000)+" \pm "+str(round(kValerror*10000)/10000)+"$"
  result2 = {"recoR":copy.deepcopy(recoR), "recoRerror":copy.deepcopy(recoRerror), "recoR2":copy.deepcopy(recoR2), "recoR2error":copy.deepcopy(recoR2error), "recoRcc":copy.deepcopy(recoRcc), "recoRccerror":copy.deepcopy(recoRccerror), "kVal":copy.deepcopy(kVal), "kValerror":copy.deepcopy(kValerror)  }

  return result2 
################
################
################
################
################
def newTemplate(h1):
  #test_ttbb = histograms[GEN+"ttbb"]["h1"].Clone()
  test_h1 = h1.Clone(h1.GetName()+"_test")
  test_h1.Reset()
  for i in range(int(h1.GetEntries())):
    xxx, yyy = Double(0), Double(0)
    h1.GetRandom2(xxx, yyy)
    test_h1.Fill(xxx,yyy)
  return copy.deepcopy(test_h1)

################
################
def fitting(histograms, freeTTB, freeTTCC, GEN, onlyPrint, isPullTest):
  res = {}
  n_ttbb = histograms[GEN+"ttbb"]["exp"]
  n_ttb  = histograms[GEN+"ttb"]["exp"]
  #n_tt2b = histograms[GEN+"tt2b"]["exp"]
  n_ttcc = histograms[GEN+"ttcc"]["exp"]#+histograms[GEN+"ttc"]["exp"]
  #n_ttc = histograms[GEN+"ttc"]["exp"]
  n_ttlf = histograms[GEN+"ttlf"]["exp"]
  n_ttcclf = histograms[GEN+"ttcclf"]["exp"]
  n_ttot = histograms[GEN+"ttot"]["exp"]
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
  
  x=RooRealVar("x","x",histograms["bkg"]["h1"].GetXaxis().GetXmin(),histograms["bkg"]["h1"].GetXaxis().GetXmax()) 
  y=RooRealVar("y","y",histograms["bkg"]["h1"].GetYaxis().GetXmin(),histograms["bkg"]["h1"].GetYaxis().GetXmax()) 
  
  RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
  RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
  #Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
  RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);
  
  fsig   =RooRealVar(    "fsig",                "fsig",           rttbb, 0.0, 0.18) 
  fsig2con  =RooFormulaVar("fsig2con",               "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )  # constraint fsig2 with fsig
  fsig2  =RooRealVar(   "fsig2",                "fsig2",          rttb, 0.0, 0.3)  # free fsig2
  fsigcc =RooRealVar(  "fsigcc",              "fsigcc",           rttcc, 0.0, 0.4)  # free fsigcc
  k      =RooRealVar(       "k","normalization factor",           1, 0.5, 1.5) 
  
  nttjj =RooRealVar(    "nttjj","number of ttjj events",                            n_ttjj , n_ttjj, n_ttjj)
  knttjj=RooFormulaVar("knttjj","number of ttjj events after fitting","k*nttjj",    RooArgList(k,nttjj) )
  nttot =RooRealVar(    "nttot","number of ttot events",                            n_ttot , n_ttot, n_ttot)
  knttot=RooFormulaVar("knttot","number of ttot events after fitting","k*nttot",    RooArgList(k,nttot) )
  nbkg  =RooRealVar(     "nbkg","number of background events",                      n_bkg , n_bkg, n_bkg)
  knbkg=RooFormulaVar("knbkg","number of background events after fitting","k*nbkg", RooArgList(k,nbkg) )
  
  ######
  nttcc =RooRealVar(   "nttcc","number of ttcc events",                         n_ttcc , n_ttcc, n_ttcc)
  knttcc=RooFormulaVar("knttcc","number of ttcc events after fitting","k*nttcc",RooArgList(k,nttcc) )
  
  """
  #from ctypes import *
  test_ttbb = histograms[GEN+"ttbb"]["h1"].Clone()
  test_ttbb.Reset()
  for i in range(int(histograms[GEN+"ttbb"]["h1"].GetEntries()/10)):
    xxx, yyy = Double(0), Double(0)
    histograms[GEN+"ttbb"]["h1"].GetRandom2(xxx, yyy)
    test_ttbb.Fill(xxx,yyy)
  """ 
  
  #histogram
  data    = RooDataHist("data",    "data set with (x)",   RooArgList(x, y), histograms["DATA"]["h1"])
  #ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   RooArgList(x, y), test_ttbb)
  ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   RooArgList(x, y), histograms[GEN+"ttbb"]["h1"])
  ttb     = RooDataHist("ttb",     "ttb  set with (x)",   RooArgList(x, y), histograms[GEN+"ttb"]["h1"])
  #tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",  RooArgList(x, y), histograms[GEN+"tt2b"]["h1"])
  ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   RooArgList(x, y), histograms[GEN+"ttcc"]["h1"] )
  ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   RooArgList(x, y), histograms[GEN+"ttlf"]["h1"])
  ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", RooArgList(x, y), histograms[GEN+"ttcclf"]["h1"])
  ttot    = RooDataHist("ttot",    "ttot set with (x)",   RooArgList(x, y), histograms[GEN+"ttot"]["h1"])
  bkg     = RooDataHist("bkg",     "bkg  set with (x)",   RooArgList(x, y), histograms["bkg"]["h1"])

  if isPullTest is True:
    ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   RooArgList(x, y), newTemplate(histograms[GEN+"ttbb"]["h1"]))
    ttb     = RooDataHist("ttb",     "ttb  set with (x)",   RooArgList(x, y), newTemplate(histograms[GEN+"ttb"]["h1"]))
    #tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",  RooArgList(x, y), newTemplate(histograms[GEN+"tt2b"]["h1"]))
    ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   RooArgList(x, y), newTemplate(histograms[GEN+"ttcc"]["h1"] ))
    ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   RooArgList(x, y), newTemplate(histograms[GEN+"ttlf"]["h1"]))
    ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", RooArgList(x, y), newTemplate(histograms[GEN+"ttcclf"]["h1"]))
    ttot    = RooDataHist("ttot",    "ttot set with (x)",   RooArgList(x, y), newTemplate(histograms[GEN+"ttot"]["h1"]))
    bkg     = RooDataHist("bkg",     "bkg  set with (x)",   RooArgList(x, y), newTemplate(histograms["bkg"]["h1"]))

 

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
  if freeTTB and not freeTTCC  : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, ttcclfpdf), RooArgList(fsig,fsig2))
  elif not freeTTB and freeTTCC: model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, ttccpdf, ttlfpdf), RooArgList(fsig,fsig2con, fsigcc))
  elif freeTTB and freeTTCC    : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, ttccpdf, ttlfpdf), RooArgList(fsig,fsig2, fsigcc))
  else                         : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf, ttcclfpdf), RooArgList(fsig,fsig2con))
  
  #model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf),              RooArgList(knttjj,knttot,knbkg)) # k*bkg
  model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf),              RooArgList(knttjj,knttot,nbkg)) # fixing bkg
  model2.fitTo(data)
  #model2.fitTo(ttlf)
  #nll0 = model2.createNLL(data)

  result = {
      "fsig":copy.deepcopy(fsig), 
      "fsig2":copy.deepcopy(fsig2), 
      "fsig2con":copy.deepcopy(fsig2con), 
      "fsigcc":copy.deepcopy(fsigcc), 
      "k":copy.deepcopy(k), 
      "rttbb":copy.deepcopy(rttbb), 
      "rttb":copy.deepcopy(rttb), 
      "rttcc":copy.deepcopy(rttcc),
      #"nll":copy.deepcopy(nll0),
      #"x":copy.deepcopy(x),
      #"y":copy.deepcopy(y),
      #"model2":copy.deepcopy(model2)
  }
  #return result
  result2=resultPrint(result, freeTTB, freeTTCC, GEN)
  recoR=result2["recoR"]
  recoRerror=result2["recoRerror"]
  recoR2=result2["recoR2"]
  recoR2error=result2["recoR2error"]
  recoRcc=result2["recoRcc"]
  recoRccerror=result2["recoRccerror"]
  kVal=result2["kVal"]
  kValerror=result2["kValerror"]

  if onlyPrint : return recoR, recoRerror

  ################
  ################
  pt = addLegendCMS()
  pt2 = addDecayMode("LL")
  pt3 = addLegend("Madgraph")
  if GEN == "POW": pt3=addLegend("Powheg")
  if GEN == "AMC": pt3=addLegend("aMC@NLO")

  ################
  lineKKK = TLine(0,0,0,0)
  lineKKK.SetLineColor(kBlue)
  lineKKK.SetLineWidth(3)
  ################
  ################
  cR10 = TCanvas("R10", "R", 1)#500, 500)
  nll = model2.createNLL(data)
  #nll = model2.createNLL(ttlf)
  #RooMinuit(nk1).migrad() 
  RFrame = fsig.frame()
  nll.plotOn(RFrame,RooFit.ShiftToZero()) 
  RFrame.SetMaximum(4.);RFrame.SetMinimum(0)
  RFrame.GetXaxis().SetTitle("Rreco as ttbb/ttjj")
  RFrame.SetTitle("")
  RFrame.Draw()
  
  line = TLine(RFrame.GetXaxis().GetXmin() ,0.5,RFrame.GetXaxis().GetXmax(),0.5)
  line.SetLineColor(kRed)
  line.Draw()
  
  lineTbb = TLine(rttbb,RFrame.GetMaximum(),rttbb,0)
  lineTbb.SetLineStyle(2)
  lineTbb.Draw()
  
  l1 = make_legend(0.49,0.76,0.93,0.88)
  l1.AddEntry(lineTbb,"prefit: R="+str(round(rttbb*10000)/10000),"l")
  l1.AddEntry(lineKKK,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","l")
  l1.SetTextSize(0.04)
  l1.SetFillColor(0)
  l1.SetLineColor(0)
  l1.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB:
    cR10.Print("plots/"+GEN+"_R_freeTTB.eps")
    cR10.Print("plots/"+GEN+"_R_freeTTB.png")
  elif freeTTCC:              
    cR10.Print("plots/"+GEN+"_R_freeTTCC.eps")
    cR10.Print("plots/"+GEN+"_R_freeTTCC.png")
  else :                      
    cR10.Print("plots/"+GEN+"_R_constraintTTB.eps")
    cR10.Print("plots/"+GEN+"_R_constraintTTB.png")
  #return cR10
  
  ################
  ################
  ################
  ################
  cR00 = TCanvas("R00", "R", 1)#500, 500)
  nllK = model2.createNLL(data)
  #nllK = result["nll"]#model2.createNLL(data)
  #nll = model2.createNLL(ttlf)
  #RooMinuit(nk1).migrad() 
  RFrameK = k.frame()
  nllK.plotOn(RFrameK,RooFit.ShiftToZero()) 
  RFrameK.SetMaximum(4.);RFrameK.SetMinimum(0)
  RFrameK.GetXaxis().SetTitle("k")
  RFrameK.SetTitle("")
  #RFrameK.SetLineColor(kBlue)
  RFrameK.Draw()
  print "RFameK: "+str(type(RFrameK))
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
  l1K.AddEntry(lineKKK,"fit: k="+str(round(kVal*10000)/10000)+" #pm "+str(round(kValerror*10000)/10000)+"","l")
  l1K.SetTextSize(0.04)
  l1K.SetFillColor(0)
  l1K.SetLineColor(0)
  l1K.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB:
    cR00.Print("plots/"+GEN+"_K_freeTTB.eps")
    cR00.Print("plots/"+GEN+"_K_freeTTB.png")
  elif freeTTCC:              
    cR00.Print("plots/"+GEN+"_K_freeTTCC.eps")
    cR00.Print("plots/"+GEN+"_K_freeTTCC.png")
  else :                      
    cR00.Print("plots/"+GEN+"_K_constraintTTB.eps")
    cR00.Print("plots/"+GEN+"_K_constraintTTB.png")
  
  
  ################
  ################
  ################
  ################
  cR11 = TCanvas("R11", "R", 1)# 500, 500)
  xframe = x.frame()
  data.plotOn(xframe, RooFit.DataError(RooAbsData.SumW2) ) 
  model2.paramOn(xframe, RooFit.Layout(0.65,0.9,0.9) )
  model2.plotOn(xframe)
  chi2 = xframe.chiSquare(2)
  ndof = xframe.GetNbinsX()
  print "chi2 = "+ str(chi2)
  print "ndof = "+ str(ndof)
  xframe.SetMaximum(xframe.GetMaximum()*1.5)
  xframe.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB:
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTB.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTB.png")
  elif freeTTCC:              
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTCC.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTCC.png")
  else :                      
    cR11.Print("plots/"+GEN+"_jet3CSV_constraintTTB.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_constraintTTB.png")
  
  ################
  ################
  ################
  ################
  ################
  cR12 = TCanvas("R12", "R", 1)#500, 500)
  yframe = y.frame()
  data.plotOn(yframe, RooFit.DataError(RooAbsData.SumW2) ) 
  model2.paramOn(yframe, RooFit.Layout(0.65,0.9,0.9) )
  model2.plotOn(yframe)
  chi22 = yframe.chiSquare(2)
  ndof2 = yframe.GetNbinsX()
  print "chi2 = "+ str(chi22)
  print "ndof = "+ str(ndof2)
  yframe.SetMaximum(yframe.GetMaximum()*1.5)
  yframe.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB:
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTB.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTB.png")
  elif freeTTCC:
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTCC.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTCC.png")
  else :
    cR12.Print("plots/"+GEN+"_jet4CSV_constraintTTB.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_constraintTTB.png")
  ###########################
  ###########################
  ###########################
  ###########################
  ###########################
  ###########################
  cNLLContourb = TCanvas("cNLLContourb", "cNLLContourb", 1)
  if freeTTB:  
    nll22 = model2.createNLL(data)
    m=RooMinuit(nll22)
    frameNLLContour = m.contour(fsig, fsig2,1,2,3)
    #cNLLContour = TCanvas("cNLLContour", "cNLLContour", 1)
  
    frameNLLContour.GetXaxis().SetTitle("R as ttbb/ttjj")
    frameNLLContour.GetYaxis().SetTitle("R2 as ttb/ttjj")
    frameNLLContour.SetMarkerStyle(21)
    frameNLLContour.Draw()
  
    preM = TMarker(rttbb,rttb,20)
    preM.SetMarkerColor(kRed)
    preM.Draw()
    preM2 = TMarker(rttbb,rttb,20)
    preM2.SetMarkerColor(kBlack)
  
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
  
    l2 = make_legend(0.49,0.7,0.93,0.88)
    l2.AddEntry(preM,"prefit: R="+str(round(rttbb*10000)/10000),"p")
    l2.AddEntry(preM,"prefit: R2="+str(round(rttb*10000)/10000),"p")
  
    l2.AddEntry(preM2,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","p")
    l2.AddEntry(preM2,"fit: R2="+str(round(recoR2*10000)/10000)+" #pm "+str(round(recoR2error*10000)/10000)+"","p")
    l2.SetTextSize(0.04)
    l2.SetFillColor(0)
    l2.SetLineColor(0)
    l2.Draw()
  
    cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTB.eps")
    cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTB.png")
  
  ###########################
  ###########################
  ###########################
  ###########################
  cNLLContourc = TCanvas("cNLLContourc", "cNLLContourc", 1)
  if freeTTCC:  
    nll22 = model2.createNLL(data)
    m=RooMinuit(nll22)
    frameNLLContour = m.contour(fsig, fsigcc,1,2,3)
    #cNLLContourc = TCanvas("cNLLContourc", "cNLLContourc", 1)
  
    frameNLLContour.GetXaxis().SetTitle("R as ttbb/ttjj")
    frameNLLContour.GetYaxis().SetTitle("R3 as ttcc/ttjj")
    frameNLLContour.SetMarkerStyle(21)
    frameNLLContour.Draw()
  
    preM = TMarker(rttbb,rttcc,20)
    preM.SetMarkerColor(kRed)
    preM.Draw()
    preM2 = TMarker(rttbb,rttcc,20)
    preM2.SetMarkerColor(kBlack)
   
  
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
  
    l2 = make_legend(0.49,0.7,0.93,0.88)
    l2.AddEntry(preM,"prefit: R="+str(round(rttbb*10000)/10000),"p")
    l2.AddEntry(preM,"prefit: Rcc="+str(round(rttcc*10000)/10000),"p")
    l2.AddEntry(preM2,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","p")
    l2.AddEntry(preM2,"fit: Rcc="+str(round(recoRcc*10000)/10000)+" #pm "+str(round(recoRccerror*10000)/10000)+"","p")
    l2.SetTextSize(0.04)
    l2.SetFillColor(0)
    l2.SetLineColor(0)
    l2.Draw()
  
    cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTCC.eps")
    cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTCC.png")
  
  ###########################
  ###########################
  ###########################
  cN = TCanvas("cN", "cN", 1)
  #histograms[GEN+"ttcc"]["h11"].Add(histograms[GEN+"ttc"]["h11"])
  
  histograms[GEN+"ttbb"]["h11"].DrawNormalized("HIST")
  histograms[GEN+"ttb"]["h11"].DrawNormalized("sameHIST")
  histograms[GEN+"ttcc"]["h11"].DrawNormalized("sameHIST")
  histograms[GEN+"ttlf"]["h11"].DrawNormalized("sameHIST")
  l21 = make_legend(0.69,0.6,0.85,0.88)
  l21.AddEntry(histograms[GEN+"ttbb"]["h11"],"ttbb","l")
  l21.AddEntry(histograms[GEN+"ttb"]["h11"],"ttb","l")
  l21.AddEntry(histograms[GEN+"ttcc"]["h11"],"ttcc","l")
  l21.AddEntry(histograms[GEN+"ttlf"]["h11"],"ttlf","l")
  l21.SetTextSize(0.04)
  l21.SetFillColor(0)
  l21.SetLineColor(0)
  l21.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  
  
  cN.Print("plots/"+GEN+"_Norm1.eps")
  cN.Print("plots/"+GEN+"_Norm1.png")
  ###########################
  cN2 = TCanvas("cN2", "cN2", 1)
  #histograms[GEN+"ttcc"]["h12"].Add(histograms[GEN+"ttc"]["h12"])
  
  histograms[GEN+"ttbb"]["h12"].DrawNormalized("HIST")
  histograms[GEN+"ttb"]["h12"].DrawNormalized("sameHIST")
  histograms[GEN+"ttcc"]["h12"].DrawNormalized("sameHIST")
  histograms[GEN+"ttlf"]["h12"].DrawNormalized("sameHIST")
  l22 = make_legend(0.69,0.6,0.85,0.88)
  l22.AddEntry(histograms[GEN+"ttbb"]["h12"],"ttbb","l")
  l22.AddEntry(histograms[GEN+"ttb"]["h12"],"ttb","l")
  l22.AddEntry(histograms[GEN+"ttcc"]["h12"],"ttcc","l")
  l22.AddEntry(histograms[GEN+"ttlf"]["h12"],"ttlf","l")
  l22.SetTextSize(0.04)
  l22.SetFillColor(0)
  l22.SetLineColor(0)
  l22.Draw()
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  
  cN2.Print("plots/"+GEN+"_Norm2.eps")
  cN2.Print("plots/"+GEN+"_Norm2.png")

 ###########################
  return cR10, cR00, cR11, cR12, cNLLContourb,cNLLContourc, cN, cN2


################
################
################
################
################
################
################
################
################
################
################
################
import sys
if len(sys.argv) < 3:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)
arg2 = sys.argv[2] # MG5, AMC, POW

arg3="0"
if len(sys.argv) > 3:
  arg3 = sys.argv[3]

histograms,freeTTB,freeTTCC,GEN=loadHistogram(arg1, arg2)
orig_r = 0.0316 # MG5

if int(arg3)==0:
  aaa=fitting(histograms, freeTTB, freeTTCC, GEN,False,False)
else:
  #a = []
  hpull = TH1F("recoR_pull","pull test for recoR",80,-2,2)
  #hpull = TH1F("recoR_pull","pull test for recoR",100,0,100)
  #hpull2= TH1F("recoR_pull2","pull test for recoR",100,0,100)
  for i in range(500):
    r,r_err = fitting(histograms, freeTTB, freeTTCC, GEN,True,True)
    #a.append( {i, result})
    hpull.Fill((orig_r-r)/r_err)
    #hpull.SetBinContent(i+1,r)
    #hpull.SetBinError(i+1,r_err)
  
 #0.0316 \pm 0.007
  #hpull2.SetBinContent(50,0.0316)
  #hpull2.SetBinError(50,0.007)
  #hpull2.SetLineColor(kRed)
  #hpull2.SetMarkerColor(kRed)

  #print "test : "+str(a)
  cpull = TCanvas("cpull", "cpull", 1)
  #hpull.GetXaxis().SetTitle("Counts")
  #hpull.GetYaxis().SetTitle("recoR")
  hpull.GetYaxis().SetTitle("Counts ")
  hpull.GetXaxis().SetTitle("(R_orig-R_i)/Rerr_i")
  pt = addLegendCMS()
  pt2 = addDecayMode("LL")
  pt3 = addLegend("Madgraph")
  if GEN == "POW": pt3=addLegend("Powheg")
  if GEN == "AMC": pt3=addLegend("aMC@NLO")
  hpull.Draw()
  hpull.Fit("gaus","0")
  #hpull2.Draw("same")
  fit1 = hpull.GetFunction("gaus")
  fit1.SetLineColor(kRed)
  fit1.Draw("same")
  mytext= ("Mean: "+str(round(fit1.GetParameter(1)*1000)/1000))
  mytext2= ("Sigma: "+str(round(fit1.GetParameter(2)*10000)/10000))
  pt4 = addLegend2(mytext,0.7,0.8)
  pt5 = addLegend2(mytext2,0.7,0.75)
  pt4.Draw()
  pt5.Draw()

  cpull.Print("plots/recoR_pull_test"+GEN+".eps")
  cpull.Print("plots/recoR_pull_test"+GEN+".png")


