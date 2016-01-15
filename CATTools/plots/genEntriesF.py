from ROOT import *
from mcsample_cfi import *

def getDictionary(tree, vvv, sel1, br):
  htemp = TH1D("htemp1","",1,-20,20)
  tree.Project("htemp1",vvv,sel1)
  cx = htemp.GetEntries()*831.76/19757190./br
  bbbb= str(int(htemp.GetEntries()))+", cx:"+str((cx) )
  print bbbb
  selection1_={"events":htemp.GetEntries(),"cx":cx}
  return selection1_ 

def getDictionary2(tree, vvv, sel1):
  htemp = TH1D("htemp1","",1,-20,20)
  tree.Project("htemp1",vvv,sel1)
  cx = htemp.GetEntries()*831.76/19757190.
  bbbb= str(int(htemp.GetEntries()))+", cx:"+str((cx) )
  print bbbb
  selection1_={"events":htemp.GetEntries(),"cx":cx}
  return selection1_ 


def ntuple2entries(files,name):
  vvv = "1"
  tt="(1)"
  
  dileptonic0  ="(diLeptonic0==1 )"
  dileptonicm1 ="(diLeptonicM1==1)"
  dileptonicp1 ="(diLeptonicP1)"

  semiLeptonic0 ="( semiLeptonic0 == 1)"
  semiLeptonicm1 ="( semiLeptonicM1 == 1)"
  semiLeptonicp1 ="( semiLeptonicP1 == 1)"

  allHadronic ="( allHadronic == 1)"

  TTBB = "(NaddbJets20 >= 2)"
  TTJJ = "(NaddJets20 >= 2)"
  dibr = ((0.1086+0.1086)*(0.1086+0.1086))
  sebr = ((0.1086+0.1086))
  habr = (0.66)  

  FS = {
#   "di0":  {"sel":  dileptonic0, "br": dibr}   ,
   "di0":   dileptonic0  ,
   "dim1":   dileptonicm1  ,
   "dip1":   dileptonicp1  ,
#   "semi0": {"sel": semiLeptonic0, "br": sebr} ,
   "semi0": semiLeptonic0,
   "semim1": semiLeptonicm1,
   "semip1": semiLeptonicp1,
#   "hadron": {"sel": allHadronic, "br": habr},
   "hadron": allHadronic,
#   "full": {"sel":"(1)", "br": 1.0}
   "full": "(1)"
  }

  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  summary = {}

  for ii in FS.keys():
    #summary['ttbb'+ii]=getDictionary(tree, vvv, tt+"*"+FS[ii]["sel"]+"*"+TTBB, FS[ii]["br"])
    #summary['ttjj'+ii]=getDictionary(tree, vvv, tt+"*"+FS[ii]["sel"]+"*"+TTJJ, FS[ii]["br"])
    summary['ttbb'+ii]=getDictionary2(tree, vvv, tt+"*"+FS[ii]+"*"+TTBB)
    summary['ttjj'+ii]=getDictionary2(tree, vvv, tt+"*"+FS[ii]+"*"+TTJJ)


  return summary


ttbarPOW = "TT_powheg"
loc = "/store/user/youngjo/Cattools/v7-4-6v5/"
z="v2"

pow=ntuple2entries(files(loc + ttbarPOW+z),ttbarPOW)

allsummary={}
allsummary["POW"]=pow

#print str(allsummary)
for ii in pow.keys():
  print (ii.rjust(13))+" : "+(str(pow[ii]["events"]).rjust(6))+", cx:"+str(round(pow[ii]["cx"]*10000)/10000)



