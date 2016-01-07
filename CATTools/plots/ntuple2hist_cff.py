from ROOT import *
import copy
from array import array
from math import sqrt

log = False
#log = True
#aMC=["AMCttbb","AMCttb","AMCttc","AMCttcc","AMCttlf","AMCttot","TTWlNu","TTWqq","TTZll","TTZqq","DYJets","DYJets10","WJets"]

def h1_maker(tree, mon, cut):
  h1 =  TH1D( mon['name'], mon['title'], mon['xbin_set'][0],mon['xbin_set'][1],mon['xbin_set'][2])
  h1.GetXaxis().SetTitle(mon['x_name'])
  h1.GetYaxis().SetTitle(mon['y_name'])
  h1.Sumw2()
  tree.Project(mon['name'],mon['var'],cut)
  if mon['name'].find("Stat")>-1:
    print " Stat: "+mon['name']+" = "+str(h1.GetBinContent(1))+" +- "+str(h1.GetBinError(1)) 
  return h1  

def h1_set(name,monitor,cutname):
  mon = {  "name" : "h1_"+name+"_"+monitor['name']+"_"+cutname, "title" : name+" "+monitor['var'],
           "var" : monitor['var'],            "xbin_set" : monitor['xbin_set'],
           "x_name": monitor['unit'], "y_name": "Entries"
        }
  return mon

def h_all_maker(tree,tree2,mc, monitors, cuts, eventweight,Ntot):
  h = []
  weight = "(1)"
  #if mc['name'] in aMC : weight = "(weight)"

  for cutname in cuts["cut"]:
    for i,ii in enumerate(monitors):
      mon = h1_set(mc['name'],monitors[i],cuts["channel"]+"_"+cutname)
      cut = "("+cuts["cut"][cutname]+" * "+mc['selection'] +")*("+eventweight[0]+"*"+weight+"/"+str(Ntot)+")"
      #if int(cutname[1:2])==6 : cut = cut+"*(csvm_sf)"
      #if int(cutname[1:2])==7 : cut = cut+"*(csvt_sf)"

      if(cutname.find("S0")>-1 or cutname.find("S1")>-1 ):
        continue
        #h1 = h1_maker(tree,mon,cut)
        #h.append(copy.deepcopy(h1))
      else :
        h1 = h1_maker(tree2,mon,cut)
        h.append(copy.deepcopy(h1))
      if(cutname.find("S6")>-1 or cutname.find("S7")>-1 or cutname.find("S8")>-1 or cutname.find("S5")>-1 ):
        for j,sysWeight in enumerate(eventweight): 
          if j>0:
            cut = "("+cuts["cut"][cutname]+" * "+mc['selection'] +")*("+eventweight[0]+"*("+sysWeight+")*"+weight+"/"+str(Ntot)+")"
            mon = h1_set(mc['name'],monitors[i],cuts["channel"]+"_"+cutname+sysWeight)
            h1 = h1_maker(tree2,mon,cut)
            h.append(copy.deepcopy(h1))

      #making shape for dy estimation
      if monitors[i]['name'].find("ZMass")>-1 and ((mc['name'].find("DYJets")>-1) or (mc['name'].find("Mu")>-1) or (mc['name'].find("El")>-1)):
        incut = "((ll_m > 76) * (ll_m < 106))"
        outcut ="(!((ll_m > 76) * (ll_m < 106)))"
        monIN = h1_set(mc['name'],monitors[i], cuts["channel"]+"_"+cutname+"_in")
        monOUT = h1_set(mc['name'],monitors[i],cuts["channel"]+"_"+cutname+"_out")
        newCut = cuts["cut"][cutname].replace("* (step2==1)","")
        cutIN = "("+newCut+" * "+incut+" * "+mc['selection'] +")*("+eventweight[0]+"*"+weight+"/"+str(Ntot)+")"
        cutOUT = "("+newCut+" * "+outcut+" * "+mc['selection'] +")*("+eventweight[0]+"*"+weight+"/"+str(Ntot)+")"
        if(cutname.find("S0")>-1 or cutname.find("S1")>-1 ):
          continue
          #h1 = h1_maker(tree,monIN,cutIN)
          #h.append(copy.deepcopy(h1))
          #h2 = h1_maker(tree,monOUT,cutOUT)
          #h.append(copy.deepcopy(h2))
        else :
          h1 = h1_maker(tree2,monIN,cutIN)
          h.append(copy.deepcopy(h1))
          h2 = h1_maker(tree2,monOUT,cutOUT)
          h.append(copy.deepcopy(h2))

  return h


######################
def h2_maker(tree, mon, cut):
  h2 =  TH2F( mon['name'], mon['title'], mon['xbin_set'][0],mon['xbin_set'][1],mon['xbin_set'][2], mon['ybin_set'][0],mon['ybin_set'][1],mon['ybin_set'][2])
  h2.GetXaxis().SetTitle(mon['x_name'])
  h2.GetYaxis().SetTitle(mon['y_name'])
  h2.Sumw2()
  tree.Project(mon['name'],mon['var'],cut)
  return h2  

def h2_set(name,monitor,monitor2,cutname):
  mon = {  "name" : "h2_"+name+"_"+monitor['name']+"_"+monitor2['name']+"_"+cutname, "title" : name+" "+monitor['var']+" vs "+monitor2['var'],
           "var" : monitor2['var']+":"+monitor['var'],         
           "xbin_set" : monitor['xbin_set'], "ybin_set" : monitor2['xbin_set'],
           "x_name": monitor['unit'], "y_name": monitor2['unit']
        }
  return mon

def h2_all_maker(tree,mc, monitors, cuts,eventweight,Ntot):
  h = []
  for cutname in cuts["cut"]:
    if( cutname.find("S5")>-1 or cutname.find("S6")>-1 or cutname.find("S7")>-1 or cutname.find("S8")>-1):
      for i,ii in enumerate(monitors):
        for j,jj in enumerate(monitors):
          if i<j:
            mon2 = h2_set(mc['name'],monitors[i],monitors[j],cuts["channel"]+"_"+cutname)
            cut = "("+cuts["cut"][cutname]+" * "+mc['selection']+")*("+eventweight[0]+"/"+str(Ntot)+")"
            h2 = h2_maker(tree,mon2,cut)
            h.append(copy.deepcopy(h2))
            for k,sysWeight in enumerate(eventweight): 
              if k>0:
                cut = "("+cuts["cut"][cutname]+" * "+mc['selection'] +")*("+eventweight[0]+"*("+sysWeight+")/"+str(Ntot)+")"
                mon2 = h2_set(mc['name'],monitors[i],monitors[j],cuts["channel"]+"_"+cutname+sysWeight)
                h2 = h2_maker(tree,mon2,cut)
                h.append(copy.deepcopy(h2))
  return h

######################
######################
######################
######################
######################

def cut_maker(cuts_):
  cuts  = {}
  for i,cut in enumerate(cuts_["cut"]):
    if i==0 :
      cuts["S%d"%i]=cut
    else:
      cuts["S%d"%i]= cuts["S%d"%(i-1)] + " * " + cut
  cutsN = {"channel":cuts_["channel"],"cut":cuts}
  if log : print cutsN
  return cutsN

def cut_maker2(cuts_):
  cuts  = {}
  for i,cut in enumerate(cuts_["cut"]):
      cuts["S%d"%i]=cut
  cutsN = {"channel":cuts_["channel"],"cut":cuts}
  return cuts
####################
####################
####################
####################
####################

def ntuple2hist(json,cuts):
  h = []
  mcsamples = json['mcsamples']
  mceventweight = json['mceventweight']
  monitors=json['monitors']
  datasamples = json['datasamples']
  for i,mc in enumerate(mcsamples):
    chain = TChain("cattree/nom")
    chain2 = TChain("cattree/nom2")
    for afile in mcsamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
      chain2.Add(afile)
    #f = TFile.Open(mcsamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain
    tree2 = chain2

    htemp = TH1D("htemp"+mcsamples[i]['name'],"",1,-2,2)
    tree.Project("htemp"+mcsamples[i]['name'],"1","weight/abs(weight)")
    Ntot = htemp.GetBinContent(1)
    #if not mc['name'] in aMC : Ntot = htemp.GetEntries()
    #htot = f.Get("hNEvent")
    #htot = f.Get("hsumWeight")
    #Ntot = htot.GetBinContent(1)
    #if log : print "total:"+str(mc['file'])+":"+str(round(Ntot))

    h= h+h_all_maker(tree,tree2,mcsamples[i],monitors,cuts,mceventweight,Ntot)
    #f.Close()
  for i,mc in enumerate(datasamples):
    chain = TChain("cattree/nom")
    chain2 = TChain("cattree/nom2")
    for afile in datasamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
      chain2.Add(afile)
    #f = TFile.Open(datasamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain
    tree2 = chain2
    #htot = f.Get("hNEvent")
    #htot = f.Get("hsumWeight")
    Ntot = 1 #htot.GetBinContent(1)
    #if log : print "total:"+str(mc['file'])+":"+str(round(Ntot))

    h= h+h_all_maker(tree,tree2,datasamples[i],monitors,cuts,["1"],1)
    #f.Close()

  return h


################
def ntuple2hist2d(json,cuts):
  h = []
  mcsamples = json['mcsamples']
  mceventweight = json['mceventweight']
  monitors2=json['monitors2']
  datasamples = json['datasamples']
  print "2d plot ...."
  for i,mc in enumerate(mcsamples):
    chain = TChain("cattree/nom")
    chain2 = TChain("cattree/nom2")
    for afile in mcsamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
      chain2.Add(afile)
    #f = TFile.Open(mcsamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain
    tree2 = chain2

    htemp = TH1D("htemp"+mcsamples[i]['name'],"",1,-2,2)
    tree.Project("htemp"+mcsamples[i]['name'],"1","weight/abs(weight)")
    Ntot = htemp.GetBinContent(1)


    h= h+h2_all_maker(tree2,mcsamples[i],monitors2,cuts,mceventweight,Ntot)
   # f.Close()

  for i,mc in enumerate(datasamples):
    chain = TChain("cattree/nom")
    chain2 = TChain("cattree/nom2")
    for afile in datasamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
      chain2.Add(afile)
    #f = TFile.Open(datasamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain
    tree2 = chain2
    #htot = f.Get("hNEvent")
    #htot = f.Get("hsumWeight")
    Ntot = 1 #htot.GetBinContent(1)

    h= h+h2_all_maker(tree2,datasamples[i],monitors2,cuts,["1"],1)
  return h


def makeoutput(outputname, h):
  fout = TFile("root/"+outputname,"RECREATE")
  for a in h:
    a.Write()
  fout.Write()
  fout.Close()

#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
def makehist(json):
  cuts_  = cut_maker(json['cuts']) 
  cutsQCD_  = cut_maker(json['cutsQCD']) 
  h=[]
  if len(json['monitors'])>0 :
    h += ntuple2hist(json,cuts_)
    #h += ntuple2histQCD(json,cutsQCD_)
  if len(json['monitors2'])>0 :
    h += ntuple2hist2d(json,cuts_)
    #h += ntuple2hist2dQCD(json,cutsQCD_)
  makeoutput(json['output'],h)

def makehist2(json):
  cuts_  = cut_maker2(json['cuts']) 
  cutsQCD_  = cut_maker(json['cutsQCD']) 
  h=[]
  if len(json['monitors'])>0 :
    h += ntuple2hist(json,cuts_)
    #h += ntuple2histQCD(json,cutsQCD_)
  if len(json['monitors2'])>0 :
    h += ntuple2hist2d(json,cuts_)
    #h += ntuple2hist2dQCD(json,cutQCD_)
  makeoutput(json['output'],h)


###################################################
###################################################

