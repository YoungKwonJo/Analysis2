from ROOT import *
from mcsample_cfi import *


def ntuple2entries(files,name):
  vvv = "1"#"(weight)/abs(weight)"
  #tt="(1)"
  tt="(weight/abs(weight))"
  #if name.find("aMC")>-1 :   tt ="(weight/abs(weight))"
  ttjj = "(partonInPhaseLep==1 && NgenJet>=4 )"
  ttbb = "("+ttjj+"&&"+"(genTtbarId%100>52))"
  ttb  = "("+ttjj+"&&"+"(genTtbarId%100>50 && genTtbarId%100<53))"
  ttcc = "("+ttjj+"&&"+"(genTtbarId%100>42 && genTtbarId%100<49))"
  ttc  = "("+ttjj+"&&"+"(genTtbarId%100>40 && genTtbarId%100<43))"
  ttlf = "("+ttjj+"&&"+"(genTtbarId%100 ==0))"

  trigger = "((channel==3||(channel==2)||(channel==1)) && (tri==1)&&(filtered==1))"
  S1 = trigger+"&&( (step1==1) &&((channel==3)&&(lep1_RelIso<0.15 && lep2_RelIso<0.15)) ||((channel==2)&&(lep1_RelIso<0.12 && lep2_RelIso<0.12)) ||((channel==1)&&(lep1_RelIso<0.12 && lep2_RelIso<0.15)) )"
  S6 = "("+S1+"&&(step2==1)&&(step3==1)&&(step4==1)&&(step5==1))"

  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain

  htemp = TH1D("htemp"+name,"",1,-20,20)
  tree.Project("htemp"+name,vvv,tt) 
  print name+"  "+tt
  aaaa="total events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,tt+"*"+S6) 
  print aaaa+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttjj+"*"+tt)
  bbbb="ttjj events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttjj+"*"+tt+"*"+S6)
  print bbbb+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))

  #ddd=""" 
  tree.Project("htemp"+name,vvv,ttbb+"*"+tt)
  cccc="ttbb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttbb+"*"+tt+"*"+S6)
  print cccc+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttb+"*"+tt)
  dddd="ttb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttb+"*"+tt+"*"+S6)
  print dddd+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttcc+"*"+tt)
  eeee="ttcc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttcc+"*"+tt+"*"+S6)
  print eeee+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttc+"*"+tt)
  ffff="ttc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttc+"*"+tt+"*"+S6)
  print ffff+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttlf+"*"+tt)
  gggg="ttlf events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tree.Project("htemp"+name,vvv,ttlf+"*"+tt+"*"+S6)
  print gggg+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  #"""


ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
loc = "/store/user/youngjo/Cattools/v7-4-6v2/"
z="v7"

ntuple2entries(files(loc + ttbarMG5+z),ttbarMG5)
ntuple2entries(files(loc + ttbarAMC+z),ttbarAMC)
ntuple2entries(files(loc + ttbarPOW+z),ttbarPOW)





