from ROOT import *
from mcsample_cfi import *


def ntuple2entries(files,name):
  vvv = "1"#"(weight)/abs(weight)"
  tt="(1)"
  #tt="(weight)"
  if name.find("aMC")>-1 :   tt ="(weight)"
  ttjj = "(partonInPhaseLep==1 && NgenJet>=4 )"
  ttbb = "("+ttjj+"&&"+"(genTtbarId%100>52))"
  ttb  = "("+ttjj+"&&"+"(genTtbarId%100>50 && genTtbarId%100<53))"
  ttcc = "("+ttjj+"&&"+"(genTtbarId%100>42 && genTtbarId%100<49))"
  ttc  = "("+ttjj+"&&"+"(genTtbarId%100>40 && genTtbarId%100<43))"
  ttlf = "("+ttjj+"&&"+"(genTtbarId%100 ==0))"

  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain

  htemp = TH1F("htemp"+name,"",1,-20,20)
  tree.Project("htemp"+name,vvv,tt) 
  print name+"  "+tt
  print "total events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttjj+"*"+tt)
  print "ttjj events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttbb+"*"+tt)
  print "ttbb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttb+"*"+tt)
  print "ttb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttcc+"*"+tt)
  print "ttcc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttc+"*"+tt)
  print "ttc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttlf+"*"+tt)
  print "ttlf events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))



ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
loc = "/store/user/youngjo/Cattools/v7-4-6v2/"
z="v7"

ntuple2entries(files(loc + ttbarMG5+z),ttbarMG5)
ntuple2entries(files(loc + ttbarAMC+z),ttbarAMC)
ntuple2entries(files(loc + ttbarPOW+z),ttbarPOW)





