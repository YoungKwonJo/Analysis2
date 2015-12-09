from ROOT import *
import copy
from array import array
from math import sqrt

################
log = False
#log = True
mainlumi=2110.

###################################################
def drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out,
                       rd_ee_in, rd_mm_in, rd_em_in):    
    kMM = sqrt(rd_mm_in/rd_ee_in)/2.
    kEE = sqrt(rd_ee_in/rd_mm_in)/2.
    print "kMM: "+str(kMM)+", KEE:"+str(kEE)

    rMC_mm = mc_mm_out/mc_mm_in
    rMC_ee = mc_ee_out/mc_ee_in
    
    nOutEst_mm = rMC_mm*(rd_mm_in - rd_em_in*kMM)
    nOutEst_ee = rMC_ee*(rd_ee_in - rd_em_in*kEE)
    return nOutEst_ee/mc_ee_out,nOutEst_mm/mc_mm_out

###################################################
def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetBorderSize(1)
  leg.SetTextFont(62)
  leg.SetTextSize(0.04)
  leg.SetLineStyle(1)
  leg.SetLineWidth(1)
  leg.SetLineColor(0)
  #leg.SetLineColor(1)
  leg.SetFillColor(0)
  #leg.SetFillColor(10)
  leg.SetFillStyle(1001)
  leg.SetMargin(0.15) #for size of the marker

  return leg

def make_banner(xmin,ymin,xmax,ymax):
  #pt = TPaveText(0.15,0.73, 0.5, 0.89,"brNDC");
  pt = TPaveText(xmin,ymin,xmax,ymax,"brNDC");
  pt.SetBorderSize(1)
  pt.SetTextFont(42)
  pt.SetTextSize(0.04)
  pt.SetLineColor(0)
  pt.SetLineStyle(1)
  pt.SetLineWidth(1)
  pt.SetFillColor(0)
  pt.SetFillStyle(1001)
  pt.SetTextAlign(12)
  pt.AddText("Work in progress")
  #pt.AddText("TTJets_madgraphMLM-pythia8")
  #pt.AddText("madgraphMLM-pythia8")
  pt.AddText("#sqrt{s} = 13 TeV")
  pt.Draw()

  return pt

def make_bannerLumi(xmin,ymin,xmax,ymax,lumi):
  #pt = TPaveText(0.15,0.73, 0.5, 0.89,"brNDC");
  pt = TPaveText(xmin,ymin,xmax,ymax,"brNDC");
  pt.SetBorderSize(1)
  pt.SetTextFont(42)
  pt.SetTextSize(0.04)
  pt.SetLineColor(0)
  pt.SetLineStyle(1)
  pt.SetLineWidth(1)
  pt.SetFillColor(0)
  pt.SetFillStyle(1001)
  pt.SetTextAlign(12)
  pt.AddText("Work in progress")
  #pt.AddText("TTJets_madgraphMLM-pythia8")
  #pt.AddText("madgraphMLM-pythia8")
  lumi2 = str(round(lumi*10)/10)
  pt.AddText( lumi2+" pb^{-1} at #sqrt{s} = 13 TeV")
  pt.Draw()

  return pt
def addLegendLumi(lumi):
  #lumi2 = str(round(lumi*10)/10)
  lumi2 = str(round(lumi/100)/10)
  #tex = TLatex(0.9760178,0.9146667,lumi2+" fb^{-1} (13 TeV)")
  #tex = TLatex(0.9380178,0.9146667,lumi2+" pb^{-1} (13 TeV)")
  tex = TLatex(0.9380178,0.9146667,lumi2+" fb^{-1} (13 TeV)")
  #tex = TLatex(0.9360178,0.9146667,lumi2+" pb^{-1} (13 TeV)")
  tex.SetNDC()
  tex.SetTextAlign(31)
  tex.SetTextFont(42)
  #tex.SetTextSize(0.07466666)
  tex.SetTextSize(0.06466666)
  tex.SetLineWidth(2)
  tex.Draw()

  return tex

def addLegendCMS():
  tex2 = TLatex(0.3715952,0.9146667,"Work in progress")
  #tex2 = TLatex(0.2015952,0.8620667,"CMS Work in progress")
  #tex2 = TLatex(0.2215952,0.8620667,"Work in progress")
  #tex2 = TLatex(0.2215952,0.8620667,"CMS Preliminary")
  tex2.SetNDC()
  #tex2.SetTextAlign(13)
  tex2.SetTextAlign(25)
  #tex2.SetTextFont(61)
  tex2.SetTextFont(42)
  #tex2.SetTextSize(0.09066667) # for CMS as short length
  tex2.SetTextSize(0.06466666)
  #tex2.SetTextSize(0.03566667)
  tex2.SetLineWidth(2)
  tex2.Draw()

  return tex2

#def addDecayMode(xmin,ymin,xmax,ymax,ll):
def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm}"
  if ll.find("em")>-1 : ll2="e^{#mp}#mu^{#pm}"
  if ll.find("mm")>-1 : ll2="#mu^{#mp}#mu^{#pm}"
  if ll.find("ee")>-1 : ll2="e^{#mp}e^{#pm}"

  tex3 = TLatex(0.2315952,0.8146667,ll2)
  tex3.SetNDC()
  tex3.SetTextAlign(5)
  tex3.SetTextFont(12)
  tex3.SetTextSize(0.04466666)
  tex3.SetLineWidth(1)
  tex3.Draw()

  return tex3


def make_banner2(xmin,ymin,xmax,ymax,bb,bb2):
  #pt = TPaveText(0.15,0.73, 0.5, 0.89,"brNDC");
  pt = TPaveText(xmin,ymin,xmax,ymax,"brNDC");
  pt.SetBorderSize(1)
  pt.SetTextFont(42)
  pt.SetTextSize(0.04)
  pt.SetLineColor(0)
  pt.SetLineStyle(1)
  pt.SetLineWidth(1)
  pt.SetFillColor(0)
  pt.SetFillStyle(1001)
  pt.SetTextAlign(12)
  pt.AddText("Work in progress")
  #pt.AddText("TTJets_madgraphMLM-pythia8")
  pt.AddText("madgraphMLM-pythia8")
  pt.AddText("#sqrt{s} = 13 TeV")
  pt.AddText( ("ttbb/ttjj : "+str("%.4f"%bb)+"")  )
  pt.AddText( ("(ttbb+ttb+tt2b)/ttjj : "+str("%.4f"%bb2)+" ") )
  pt.Draw()

  return pt

#########################
def plotTH2F(filename,mon,step,mcsamples):
  f = TFile.Open(filename,"read")
  n=len(mcsamples)
  gStyle.SetOptStat(0)
  c1 = TCanvas( 'c2', '', 500*3, 500*2 ) 
  c1.Divide(3,2)
  legs = []
  #pts  = []
  for i,mc in enumerate(mcsamples):
    c1.cd(i+1)
    histname = "h2_"+mc['name']+"_"+mon+"_"+step+"_Sumw2"
    h1 = f.Get(histname)
    if type(h1) is not TH2F :  
      return
    h1.SetTitle("")
    h1.SetLineColor(mc['color'])
    h1.Draw("colz")
    #pt = make_banner(0.15,0.73, 0.5, 0.89)
    #pts.append(copy.deepcopy(pt))
    #pts[i].Draw()
    leg = make_legend(0.5,0.91, 0.75,0.99)
    leg.AddEntry(h1, ("%s : "%mc['label']) + ("%.0f"%h1.Integral()), "l");
    legs.append(copy.deepcopy(leg))
    legs[i].Draw()
  output = "plots/TH2_"+mon+"_"+step+".eps"
  c1.Print(output)
  f.Close()
  c1.Close()


#########################
#########################
#########################
#########################
#########################
#########################
#########################
#########################
def myCanvas(name):
  c1 = TCanvas( name, '', 500, 500 )
#  gStyle.SetOptFit(1)
#  gStyle.SetOptStat(0)
  c1.Range(0,0,1,1)
  c1.SetFillColor(0)
  c1.SetBorderMode(0)
  c1.SetBorderSize(2)
  c1.SetTickx(1)
  c1.SetTicky(1)
  c1.SetLeftMargin(0.15)
  c1.SetRightMargin(0.05)
  c1.SetBottomMargin(0.15)
  c1.SetFrameBorderMode(0)

  return c1

def myPad1(name):
  pad1 = TPad(name, "",0,0.3,1,1)
  pad1.Range(-1.072875,-0.39794,5.364372,5.641005)
  pad1.SetFillColor(0)
  pad1.SetBorderMode(0)
  pad1.SetBorderSize(2)
  pad1.SetLogy()
  pad1.SetTickx(1)
  pad1.SetTicky(1)
  pad1.SetLeftMargin(0.1666667)
  pad1.SetRightMargin(0.05660377)
  pad1.SetBottomMargin(0)
  pad1.SetFrameBorderMode(0)
  pad1.SetFrameBorderMode(0)

  return pad1

def myPad2(name):
  if log :  print "pad2() step0"
  pad2 = TPad(name, "",0,0,1,0.3)
  if log :  print "pad2() step1"
  pad2.Range(-1.072875,-1.321429,5.364372,2.25)
  pad2.SetFillColor(0)
  pad2.SetBorderMode(0)
  pad2.SetBorderSize(2)
  pad2.SetTickx(1)
  pad2.SetTicky(1)
  pad2.SetLeftMargin(0.1666667)
  pad2.SetRightMargin(0.05660377)
  pad2.SetTopMargin(0.07)
  pad2.SetBottomMargin(0.37)
  pad2.SetFrameBorderMode(0)
  pad2.SetFrameBorderMode(0)

  return pad2

#################
def myDataHistSet(hdata):
  hdata.SetTitle("")
  hdata.SetStats(0)
  #hdata.SetMaximum(scale*400)
  #hdata.SetMinimum(0.005)
  hdata.GetYaxis().SetNdivisions(505);
  #hdata.GetYaxis().SetLabelFont(42);
  hdata.GetYaxis().SetLabelOffset(0.007);
  hdata.GetYaxis().SetLabelSize(0.05);
  hdata.GetYaxis().SetTitleSize(0.05);
  hdata.GetYaxis().SetTitleOffset(1.4);
  hdata.SetMarkerColor(kBlack)
  hdata.SetLineColor(kBlack)
  hdata.SetMarkerStyle(20)
  hdata.SetMarkerSize(1)
 
  return hdata

def myBottomDataPerMCSet(hdata):
  hdataMC = hdata.Clone("hdataMC")
  hdataMC.SetTitle("")
  hdataMC.SetMaximum(2.0)
  hdataMC.SetMinimum(0.0)
  hdataMC.GetXaxis().SetLabelOffset(0.007);
  hdataMC.GetXaxis().SetLabelSize(0.1);
  hdataMC.GetXaxis().SetTitleSize(0.14);
  hdataMC.GetXaxis().SetTitleOffset(1.1);
  #hdataMC.GetXaxis().SetTitleFont(42);
  hdataMC.GetYaxis().SetTitle("Data/MC");
  hdataMC.GetYaxis().SetNdivisions(505);
  #hdataMC.GetYaxis().SetLabelFont(42);
  hdataMC.GetYaxis().SetLabelOffset(0.007);
  hdataMC.GetYaxis().SetLabelSize(0.1);
  hdataMC.GetYaxis().SetTitleSize(0.14);
  hdataMC.GetYaxis().SetTitleOffset(0.4);
  #hdataMC.GetYaxis().SetTitleFont(42);
  hdataMC.SetMarkerColor(kBlack)
  hdataMC.SetLineColor(kBlack)
  hdataMC.SetMarkerStyle(20)
  hdataMC.SetMarkerSize(1)

  return hdataMC

def myHist2TGraphError(hist1):
  xx=[]
  xxer=[]
  yy=[]
  yyer=[]
  for i in range(0, hist1.GetNbinsX()+2 ):
    yy.append(  float(hist1.GetBinContent(i)))
    yyer.append(float(hist1.GetBinError(i)))
    xx.append(  float(hist1.GetBinCenter(i)))
    xxer.append(float(hist1.GetBinWidth(i)/2))

  x   = array("d",xx)
  xer = array("d",xxer)
  y   = array("d",yy)
  yer = array("d",yyer)
  gr = TGraphErrors(len(x), x,y,xer,yer)
  gr.SetFillColor(kBlack);
  #gr.SetFillStyle(3144);
  #gr.SetFillStyle(3005);
  #gr.SetFillStyle(3244);
  gr.SetFillStyle(3444);

  return gr
#####################


#####################
def drellYanEstimationRun(f,step): #,mcsamples,datasamples):
 
  step=step.replace("mm","")
  step=step.replace("ee","")
  step=step.replace("em","")
  mcs = ["DYJets","DYJets10"]
  mcxs = [6025.2,18271.92]
  datas = ["1","2","3"]

  hmceein = TH1F("mc_ee_in","",60,0,300)
  hmcmmin = TH1F("mc_mm_in","",60,0,300)
  hmcemin = TH1F("mc_em_in","",60,0,300)

  hmceeout = TH1F("mc_ee_out","",60,0,300)
  hmcmmout = TH1F("mc_mm_out","",60,0,300)

  hrdeein = TH1F("rd_ee_in","",60,0,300)
  hrdmmin = TH1F("rd_mm_in","",60,0,300)
  hrdemin = TH1F("rd_em_in","",60,0,300)

  for i,mc in enumerate(mcs) :
    inee = "h1_"+mc+"_ZMass_"+step+"ee_in"
    h1=f.Get(inee).Clone("hhhh_ee_"+mc) 
    h1.Scale(mainlumi*mcxs[i])
    hmceein.Add(h1)

    inmm = "h1_"+mc+"_ZMass_"+step+"mm_in"
    h2=f.Get(inmm).Clone("hhhh_mm_"+mc) 
    h2.Scale(mainlumi*mcxs[i])
    hmcmmin.Add(h2)

    inem = "h1_"+mc+"_ZMass_"+step+"em_in"
    h3=f.Get(inem).Clone("hhhh_em_"+mc) 
    h3.Scale(mainlumi*mcxs[i])
    hmcemin.Add(h3)

    outee = "h1_"+mc+"_ZMass_"+step+"ee_out"
    h11=f.Get(outee).Clone("hhhh_ee_"+mc) 
    h11.Scale(mainlumi*mcxs[i])
    hmceeout.Add(h11)

    outmm = "h1_"+mc+"_ZMass_"+step+"mm_out"
    h22=f.Get(outmm).Clone("hhhh_mm_"+mc) 
    h22.Scale(mainlumi*mcxs[i])
    hmcmmout.Add(h22)

  for data in datas :
    eein = "h1_ElEl"+data+"_ZMass_"+step+"ee_in"
    h1=f.Get(eein).Clone("hhhh_rd_ee"+data)
    hrdeein.Add(h1)

    mmin = "h1_MuMu"+data+"_ZMass_"+step+"mm_in"
    h2=f.Get(mmin).Clone("hhhh_rd_mm"+data)
    hrdmmin.Add(h2)

    emin = "h1_MuEl"+data+"_ZMass_"+step+"em_in"
    h3=f.Get(emin).Clone("hhhh_rd_em"+data)
    hrdemin.Add(h3)

  mc_ee_in   = hmceein.Integral()
  mc_ee_out  = hmceeout.Integral()
  mc_mm_in   = hmcmmin.Integral()
  mc_mm_out  = hmcmmout.Integral()
  rd_ee_in   = hrdeein.Integral()
  rd_mm_in   = hrdmmin.Integral()
  rd_em_in   = hrdemin.Integral()

  return drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out, rd_ee_in, rd_mm_in, rd_em_in)
 
def singleplotStack2(filename,mon,step,mcsamples,datasamples,useReturn):
  f = TFile.Open(filename,"read")
  singleplotStack(f,mon,step,mcsamples,datasamples,useReturn)
  f.Close()

def singleplotStack(f,mon,step,mcsamples,datasamples,useReturn):

  dyest = drellYanEstimationRun(f,step)

  #f = TFile.Open(filename,"read")
  canvasname = mon+step
  c1 = myCanvas(canvasname)
  #c1 = TCanvas( 'c1', '', 500, 500 )
  if log : print mon+step
  gStyle.SetOptFit(1)
  gStyle.SetOptStat(0)

  #pad1 = TPad("pad1", "",0,0.3,1,1);
  pad1 = myPad1(canvasname+"pad1") 
  pad1.Draw()
  pad1.cd()

  leg  = make_legend(0.74,0.64, 0.89,0.88)
  leg2 = make_legend(0.59,0.64, 0.74,0.88)
  #leg  = make_legend(0.67,0.64, 0.89,0.88)
  #leg2 = make_legend(0.43,0.605, 0.62,0.88)
  #lumi = 40.028
  #lumi = 42.0
  #lumi = 15.478
  #lumi = 1280.23
  lumi = mainlumi
  #lumi = 10.028
  hs = THStack("hs","")

  hmctotName = "h1_"+mcsamples[0]['name']+"_"+mon+"_"+step
  #if log : print "hmcTotal: "+hmctotName
  hmctot = f.Get(hmctotName).Clone("hmctot")
  hmcmerge = f.Get(hmctotName).Clone("hmcmerge")
  hmcSig = f.Get(hmctotName).Clone("hmcSig")
  hmctot.Reset()
  hmcmerge.Reset()
  hmcSig.Reset()
  hdata = hmctot.Clone("hdata")

  isStat = mon.find("Stat")>-1
  if isStat : 
    print "step: "+step

  for i,mc in enumerate(mcsamples):
    isMC = mc['label'].find("DATA")==-1
    if not isMC: continue

    histnameS = "h1_"+mc['name']+"_"+mon+"_"+step
    channel = step[2:4]
    h2 = f.Get(histnameS).Clone("h"+histnameS)
    if type(h2) is not TH1F :
      continue
    h2.GetYaxis().SetTitle("Events")

    h2.AddBinContent(h2.GetNbinsX(),h2.GetBinContent(h2.GetNbinsX()+1))
    #if h2.Integral()>0 :  h2.Scale(mc['cx']/Ntot*lumi)
    if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
    #if h2.Integral()>0 :  h2.Scale(lumi)

    ###############
    isDY = mc['name'].find("DYJet")>-1
    if isDY and int(step[1:2])>1: 
      if step.find("ee")>-1:
        h2.Scale(dyest[0])
      if step.find("mm")>-1:
        h2.Scale(dyest[1])

    isTTH = mc['name'].find("ttH")>-1
    if not isTTH:
      hmctot.Add( h2 )
    hmcmerge.Add(h2)
    #hs.Add(h2)

    selEvet=h2.Integral() 
    selEnts=h2.GetEntries()
    if log : print "mc:"+mc['file']+":"+str(round(selEvet))+", "+str(selEnts)
    isSameNext=False
    if i<len(mcsamples)-1 : isSameNext= mc['label'] is mcsamples[i+1]["label"]
    if  (not isSameNext) and i<7: 
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(mc['color'])
      h3.SetLineColor(kBlack)
      label = ("%s"%mc['label']) #+ (" %.0f"%(h3.Integral()) ).rjust(7)
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*100)/100)+" \pm "+str(round(h3.GetBinError(1)*100)/100)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
      leg.AddEntry(h3, label, "f")
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and not isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(mc['color'])
      h3.SetLineColor(kBlack)

      label = ("%s"%mc['label']) #+ (" %.0f"%(h3.Integral()) ).rjust(7)
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*100)/100)+" \pm "+str(round(h3.GetBinError(1)*100)/100)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      leg2.AddEntry(h3, label, "f")
      hs.Add(h3)
      #hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and  isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      #h3.SetLineColor(kBlack)
      hmcSig.Add(h3)
      hmcSig.SetLineColor(mc['color'])
      hmcSig.SetTitle(mc['label'])
#      label = ("%s"%mc['label']) + (" %.0f"%(hmcSig.Integral()) ).rjust(7)
#      leg2.AddEntry(hmcSig, label, "l")
      hmcmerge.Reset()

  hdata.Reset()
  for i,mc in enumerate(datasamples):
    histnameS = "h1_"+mc['name']+"_"+mon+"_"+step
    channel = step[2:4]
    h1 = f.Get(histnameS).Clone("h"+histnameS)
    if type(h1) is not TH1F :
      continue
    h1.GetYaxis().SetTitle("Events")

    h1.AddBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX()+1))
    selEvet=h1.Integral() 
    selEnts=h1.GetEntries()
 
    checkDataChannel = (channel=="mm" and mc['name'].find("MuMu")>-1 ) or (channel=="ee" and mc['name'].find("ElEl")>-1 ) or (channel=="em" and mc['name'].find("MuEl")>-1 )
    if checkDataChannel : 
      hdata.Add(h1)
      if log : print "data:"+mc['file']+": "+str(round(selEvet))+", "+str(selEnts)
################################
  scale = hmctot.GetMaximum()
  minimum = 0.05

  h1data = hdata.Clone("h1data")
  h2data = myDataHistSet(h1data)

  h2data.SetMaximum(scale*40)
  h2data.SetMinimum(minimum)
  labeltot = ("MC Total") #+ (" %.0f"%hmctot.Integral()).rjust(8)
  #leg2.AddEntry(hmctot,labeltot,"")
  if isStat:
    if hmctot.GetBinContent(1)<100 : print " Stat: "+("MC Total").rjust(10)+" & $ "+str(round(hmctot.GetBinContent(1)*100)/100)+" \pm "+str(round(hmctot.GetBinError(1)*100)/100)+" $"
    else                           : print " Stat: "+("MC Total").rjust(10)+" & $ "+str(round(hmctot.GetBinContent(1)))+" \pm "+str(round(hmctot.GetBinError(1)))+" $"
 
  label = ("%s"%hmcSig.GetTitle()) #+ (" %.0f"%(hmcSig.Integral()) ).rjust(7)
  if(hmcSig.Integral()>0) : leg2.AddEntry(hmcSig, label, "l")
  if isStat and (hmcSig.Integral()>0):
    if hmcSig.GetBinContent(1)<100 : print " Stat: "+("tth").rjust(10)+" & $ "+str(round(hmcSig.GetBinContent(1)*100)/100)+" \pm "+str(round(hmcSig.GetBinError(1)*100)/100)+" $"
    else                           : print " Stat: "+("tth").rjust(10)+" & $ "+str(round(hmcSig.GetBinContent(1)))+" \pm "+str(round(hmcSig.GetBinError(1)))+" $"
 
  labeldata = ("DATA     ")# + (" %.0f"%h2data.Integral()).rjust(8)
  leg2.AddEntry(h2data,labeldata,"p")
  if isStat :
    print " Stat: "+("DATA ").rjust(10)+" & $ "+str(round(h2data.GetBinContent(1)))+" $" # +" +- "+str(h2data.GetBinError(1))

#########################################
  h2data.GetYaxis().SetTitle("Events")
  h2data.Draw()
  gr = myHist2TGraphError(hmctot)
  hs.Draw("same,hist")
  gr.Draw("same,2")
  hmcSig.Draw("same")
  h2data.Draw("same")
#  h2data.Draw("sameaxis")


  leg.Draw()
  leg2.Draw()
  pad1.SetLogy()
  pt = addLegendLumi(lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode(channel)
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  pad1.Modified()
  c1.cd()
###########################################
  if log :  print "pad1 step"
  #pad2 = TPad("pad2", "",0,0,1,0.3)
  pad2 = myPad2(canvasname+"pad2")

  if log :  print "pad2 step1"
  pad2.Draw()
  pad2.cd()
  hdata.Divide(hmctot)

  hdataMC = myBottomDataPerMCSet(hdata)

  hdataMC.Draw()

  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  output = "plots/TH1_"+mon+"_"+step+".eps"
  c1.Print(output)

  #f.Close()
  #c1.Close()
  if useReturn : return c1,pad1,pad2,hs,gr,h2data,hdataMC,leg,leg2
  else : c1.Close() 
    
############################################
############################################
##################################################
##################################################
############################################
############################################
def singleplotStackLL2(filename,mon,step,mcsamples,datasamples,useReturn):
  f = TFile.Open(filename,"read")
  singleplotStackLL(f,mon,step,mcsamples,datasamples,useReturn)
  f.Close()

def singleplotStackLL(f,mon,step,mcsamples,datasamples,useReturn):

  dyest = drellYanEstimationRun(f,step)
  print "step : "+step+":"+str(dyest)
  #f = TFile.Open(filename,"read")
  canvasname = mon+step
  c1 = myCanvas(canvasname)
  #c1 = TCanvas( 'c1', '', 500, 500 )
  if log : print mon+step
  gStyle.SetOptFit(1)
  gStyle.SetOptStat(0)

  #pad1 = TPad("pad1", "",0,0.3,1,1);
  pad1 = myPad1(canvasname+"pad1") 
  pad1.Draw()
  pad1.cd()

  leg  = make_legend(0.74,0.64, 0.89,0.88)
  leg2 = make_legend(0.59,0.64, 0.74,0.88)
  #leg  = make_legend(0.67,0.64, 0.89,0.88)
  #leg2 = make_legend(0.43,0.605, 0.62,0.88)
  #lumi = 40.028
  #lumi = 42.0
  #lumi = 15.478
  #lumi = 1280.23
  lumi = mainlumi
  #lumi = 10.028
  hs = THStack("hs","")

  hmctotName = "h1_"+mcsamples[0]['name']+"_"+mon+"_"+step+"mm"
  if log : print "hmcTotal: "+hmctotName
  hmctot = f.Get(hmctotName).Clone("hmctot")
  hmcmerge = f.Get(hmctotName).Clone("hmcmerge")
  hmcSig = f.Get(hmctotName).Clone("hmcSig")
  hmctot.Reset()
  hmcmerge.Reset()
  hmcSig.Reset()
  hdata = hmctot.Clone("hdata")

  isStat = mon.find("Stat")>-1
  if isStat : 
    print "step: "+step

  for i,mc in enumerate(mcsamples):
    isMC = mc['label'].find("DATA")==-1
    if not isMC: continue

    histnameSmm = "h1_"+mc['name']+"_"+mon+"_"+step+"mm"
    histnameSee = "h1_"+mc['name']+"_"+mon+"_"+step+"ee"
    histnameSem = "h1_"+mc['name']+"_"+mon+"_"+step+"em"
    #channel = step[2:4]
    h2ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h2ee = f.Get(histnameSee).Clone("h"+histnameSee)
    h2em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h2ll) is not TH1F :
      continue


    h2ll.AddBinContent(h2ll.GetNbinsX(),h2ll.GetBinContent(h2ll.GetNbinsX()+1))
    h2ee.AddBinContent(h2ee.GetNbinsX(),h2ee.GetBinContent(h2ee.GetNbinsX()+1))
    h2em.AddBinContent(h2em.GetNbinsX(),h2em.GetBinContent(h2em.GetNbinsX()+1))
    ###############
    isDY = mc['name'].find("DYJet")>-1
    if isDY and int(step[1:2])>1: 
        h2ee.Scale(dyest[0])
        h2ll.Scale(dyest[1])


    #if h2.Integral()>0 :  h2.Scale(mc['cx']/Ntot*lumi)
    h2ll.Add(h2ee)
    h2ll.Add(h2em)

    if h2ll.Integral()>0 :  h2ll.Scale(mc['cx']*lumi)
    #if h2ll.Integral()>0 :  h2ll.Scale(lumi)

    ###############
    h2ll.SetFillColor(mc['color'])
    h2ll.SetLineColor(kBlack)
    isTTH = mc['name'].find("ttH")>-1
    if not isTTH:
      hmctot.Add( h2ll )
    hmcmerge.Add(h2ll)
    #hs.Add( h2ll )

    selEvet=h2ll.Integral() 
    selEnts=h2ll.GetEntries()
    if log : print "mc:"+mc['file']+":"+str(round(selEvet))+", "+str(selEnts)
    isSameNext=False
    if i<len(mcsamples)-1 : isSameNext= mc['label'] is mcsamples[i+1]["label"]
    if  (not isSameNext) and i<7:
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(mc['color'])
      h3.SetLineColor(kBlack)
      label = ("%s"%mc['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*100)/100)+" \pm "+str(round(h3.GetBinError(1)*100)/100)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and not isTTH :
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(mc['color'])
      h3.SetLineColor(kBlack)
      label = ("%s"%mc['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg2.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*100)/100)+" \pm "+str(round(h3.GetBinError(1)*100)/100)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and  isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      #h3.SetLineColor(kBlack)
      hmcSig.Add(h3)
      hmcSig.SetLineColor(mc['color'])
      hmcSig.SetTitle(mc['label'])
      #label = ("%s"%mc['label']) + (" %.0f"%(hmcSig.Integral()) ).rjust(7)
      #leg2.AddEntry(hmcSig, label, "l")
      hmcmerge.Reset()

  hdata.Reset()
  for i,mc in enumerate(datasamples):
    histnameSmm = "h1_"+mc['name']+"_"+mon+"_"+step+"mm"
    histnameSee = "h1_"+mc['name']+"_"+mon+"_"+step+"ee"
    histnameSem = "h1_"+mc['name']+"_"+mon+"_"+step+"em"
    channel = step[2:4]
    h1ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h1ee = f.Get(histnameSee).Clone("h"+histnameSee)
    h1em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h1ll) is not TH1F :
      continue
    h1ll.GetYaxis().SetTitle("Events")

    isMuMu = mc['name'].find("MuMu")==-1
    isElEl = mc['name'].find("ElEl")==-1
    isMuEl = mc['name'].find("MuEl")==-1
    if not isMuMu :
      h1ee.Reset()
      h1em.Reset()
    if not isElEl :
      h1ll.Reset()
      h1em.Reset()
    if not isMuEl :
      h1ee.Reset()
      h1ll.Reset()

    h1ll.AddBinContent(h1ll.GetNbinsX(),h1ll.GetBinContent(h1ll.GetNbinsX()+1))
    h1ee.AddBinContent(h1ee.GetNbinsX(),h1ee.GetBinContent(h1ee.GetNbinsX()+1))
    h1em.AddBinContent(h1em.GetNbinsX(),h1em.GetBinContent(h1em.GetNbinsX()+1))
    h1ll.Add(h1ee)
    h1ll.Add(h1em)

    selEvet=h1ll.Integral() 
    selEnts=h1ll.GetEntries()
 
    hdata.Add(h1ll)
    if log : print "data:"+mc['file']+": "+str(round(selEvet))+", "+str(selEnts)
    #if not (round(selEvet) == round(selEnts)) : return 
################################
  scale = hmctot.GetMaximum()
  minimum = 0.05

  h1data = hdata.Clone("h1data")
  h2data = myDataHistSet(h1data)

  h2data.SetMaximum(scale*40)
  h2data.SetMinimum(minimum)
  #if log :  print "dddd"+str(type(hmctot))+("bbbb: %f"%hmctot.Integral())
  labeltot = ("MC Total") + (" %.0f"%hmctot.Integral()).rjust(8)
  #leg2.AddEntry(hmctot,labeltot,"")
  if isStat:
    if hmctot.GetBinContent(1)<100 : print " Stat: "+("MC Total").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)*100)/100)+" \pm "+str(round(hmctot.GetBinError(1)*100)/100)+" $"
    else                           : print " Stat: "+("MC Totlal").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)))+" \pm "+str(round(hmctot.GetBinError(1)))+" $"
 
  label = ("%s"%hmcSig.GetTitle()) #+ (" %.0f"%(hmcSig.Integral()) ).rjust(7)
  if(hmcSig.Integral()>0) : leg2.AddEntry(hmcSig, label, "l")
  if isStat and (hmcSig.Integral()>0):
    if hmcSig.GetBinContent(1)<100 : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)*100)/100)+" \pm "+str(round(hmcSig.GetBinError(1)*100)/100)+" $"
    else                       : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)))+" \pm "+str(round(hmcSig.GetBinError(1)))+" $"
 
  labeldata = ("DATA     ") #+ (" %.0f"%h2data.Integral()).rjust(8)
  leg2.AddEntry(h2data,labeldata,"p")
  if isStat:
    print " Stat: "+("DATA").rjust(10)+" & $ "+str(round(h2data.GetBinContent(1)))+" $" #+" +- "+str(h2data.GetBinError(1))
 

#########################################
  h2data.GetYaxis().SetTitle("Events")
  h2data.Draw()
  hs.Draw("same,hist")
  gr = myHist2TGraphError(hmctot)
  gr.Draw("same,2")
  hmcSig.Draw("same")
  h2data.Draw("same")
#  h2data.Draw("sameaxis")


  leg.Draw()
  leg2.Draw()
  pad1.SetLogy()
  pt = addLegendLumi(lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode("ll")
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  pad1.Modified()
  c1.cd()
###########################################
  if log :  print "pad1 step"
  #pad2 = TPad("pad2", "",0,0,1,0.3)
  pad2 = myPad2(canvasname+"pad2")

  if log :  print "pad2 step1"
  pad2.Draw()
  pad2.cd()
  hdata.Divide(hmctot)

  #if log : print "divide start"+str(hdata.Integral())
  hdataMC = myBottomDataPerMCSet(hdata)

  #if log : print "divide end"
  hdataMC.Draw()

  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  output = "plots/TH1_"+mon+"_"+step+"LL.eps"
  c1.Print(output)

  #f.Close()
  #c1.Close()
  if useReturn : return c1,pad1,pad2,hs,gr,h2data,hdataMC,leg,leg2
  else : c1.Close() 
    
############################################
