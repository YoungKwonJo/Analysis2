from ROOT import *
import copy
from array import array
from math import sqrt

log = False
#log = True

def h1_maker(tree, mon, cut):
  h1 =  TH1F( mon['name'], mon['title'], mon['xbin_set'][0],mon['xbin_set'][1],mon['xbin_set'][2])
  h1.GetXaxis().SetTitle(mon['x_name'])
  h1.GetYaxis().SetTitle(mon['y_name'])
  h1.Sumw2()
  tree.Project(mon['name'],mon['var'],cut)
  return h1  

def h1_set(name,monitor,cutname):
  mon = {  "name" : "h1_"+name+"_"+monitor['name']+"_"+cutname, "title" : name+" "+monitor['var'],
           "var" : monitor['var'],            "xbin_set" : monitor['xbin_set'],
           "x_name": monitor['unit'], "y_name": "Entries"
        }
  return mon

def h_all_maker(tree,mc, monitors, cuts, eventweight,Ntot):
  h = []
  for cutname in cuts["cut"]:
    for i,ii in enumerate(monitors):
      mon = h1_set(mc['name'],monitors[i],cutname+cuts["channel"])
      cut = "("+cuts["cut"][cutname]+" && "+mc['selection'] +")*("+str(eventweight)+"/"+str(Ntot)+")"
      h1 = h1_maker(tree,mon,cut)
      h.append(copy.deepcopy(h1))
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
    for i,ii in enumerate(monitors):
      for j,jj in enumerate(monitors):
        if i<j:
          mon2 = h2_set(mc['name'],monitors[i],monitors[j],cutname+cuts["channel"])
          cut = "("+cuts["cut"][cutname]+" && "+mc['selection']+")*("+str(eventweight)+"/"+str(Ntot)+")"
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
      cuts["S%d"%i]= cuts["S%d"%(i-1)] + " && " + cut
  cutsN = {"channel":cuts_["channel"],"cut":cuts}
  #if log : print cutsN
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
    for afile in mcsamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
    #f = TFile.Open(mcsamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain

    htemp = TH1F("htemp","",1,-2,2)
    tree.Project("htemp","1","weight")
    Ntot = htemp.GetBinContent(1)
    #htot = f.Get("hNEvent")
    #htot = f.Get("hsumWeight")
    #Ntot = htot.GetBinContent(1)
    if log : print "total:"+mc['file']+":"+str(round(Ntot))

    h= h+h_all_maker(tree,mcsamples[i],monitors,cuts,mceventweight,Ntot)
    f.Close()
  for i,mc in enumerate(datasamples):
    chain = TChain("cattree/nom")
    for afile in datasamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      chain.Add(afile)
    #f = TFile.Open(datasamples[i]['file'],"read")
    #tree = f.ntuple
    tree = chain
    #htot = f.Get("hNEvent")
    #htot = f.Get("hsumWeight")
    Ntot = 1 #htot.GetBinContent(1)
    if log : print "total:"+mc['file']+":"+str(round(Ntot))

    h= h+h_all_maker(tree,datasamples[i],monitors,cuts,1,1)
    f.Close()

  return h


################
def ntuple2hist2d(json,cuts):
  h = []
  mcsamples = json['mcsamples']
  mceventweight = json['mceventweight']
  monitors2=json['monitors2']
  datasamples = json['datasamples']
  for i,mc in enumerate(mcsamples):
    f = TFile.Open(mcsamples[i]['file'],"read")
    #tree = f.ntuple
    tree = f.myresult2

    #htot = f.Get("hNEvent")
    htot = f.Get("hsumWeight")
    Ntot = htot.GetBinContent(1)
    #if log : print "mc:"+mc['name']+":"+str(round(Ntot))

    h= h+h2_all_maker(tree,mcsamples[i],monitors2,cuts,mceventweight,Ntot)
    f.Close()

  for i,mc in enumerate(datasamples):
    f = TFile.Open(mcsamples[i]['file'],"read")
    #tree = f.ntuple
    tree = f.myresult2
    h= h+h2_all_maker(tree,datasamples[i],monitors2,cuts,1,1)
    f.Close()
  return h


def makeoutput(outputname, h):
  fout = TFile(outputname,"RECREATE")
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

