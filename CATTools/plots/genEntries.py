from ROOT import *
from mcsample_cfi import *

def mAND(aaa,bbb):
  return "(" +aaa+ " && "+bbb+")"

def ntuple2entries(files,name):
  vvv = "1"#"(weight)/abs(weight)"
  #tt="(1)"
  tt="(weight/abs(weight))"
  #if name.find("aMC")>-1 :   tt ="(weight/abs(weight))"
  visible="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
  ttjj = visible
  ttbb = mAND("(NbJets20>=4)",visible)
  ttb = mAND("(NbJets20==3)",visible)
  ttcc = mAND("((NcJets20>=2) && !(NbJets20>=3))",visible)
  ttlf = mAND("(!(NbJets20>=4) && !(NbJets20==3) && !(NcJets20>=2))",visible)

  old="""
  ttjj = "(partonInPhaseLep==1 && NgenJet>=4 )"
  ttbb = "("+ttjj+"&&"+"(genTtbarId%100>52))"
  ttb  = "("+ttjj+"&&"+"(genTtbarId%100>50 && genTtbarId%100<53))"
  ttcc = "("+ttjj+"&&"+"(genTtbarId%100>42 && genTtbarId%100<49))"
  ttc  = "("+ttjj+"&&"+"(genTtbarId%100>40 && genTtbarId%100<43))"
  ttlf = "("+ttjj+"&&"+"(genTtbarId%100 ==0))"
  """

  trigger = "((channel==3||(channel==2)||(channel==1)) && (tri==1)&&(filtered==1))"
  S1 = trigger+"&&( (step1==1) &&((channel==3)&&(lep1_RelIso<0.15 && lep2_RelIso<0.15)) ||((channel==2)&&(lep1_RelIso<0.12 && lep2_RelIso<0.12)) ||((channel==1)&&(lep1_RelIso<0.12 && lep2_RelIso<0.15)) )"
  S6 = "("+S1+"&&(step2==1)&&(step3==1)&&(step4==1)&&(step5==1))"

  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  summary = {}
  htemp = TH1D("htemp"+name,"",1,-20,20)
  tree.Project("htemp"+name,vvv,tt) 
  print name+"  "+tt
  aaaa="total events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  tot_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,tt+"*"+S6) 
  print aaaa+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  totS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['total']={"GEN":tot_,"S6":totS6_, "eff1":totS6_["events"]/tot_["events"], "eff2":totS6_["integral"]/tot_["integral"]}  

  tree.Project("htemp"+name,vvv,ttjj+"*"+tt)
  bbbb="ttjj events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttjj_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,ttjj+"*"+tt+"*"+S6)
  print bbbb+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttjjS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['ttjj']={"GEN":ttjj_,"S6":ttjjS6_, "eff1":ttjjS6_["events"]/ttjj_["events"], "eff2":ttjjS6_["integral"]/ttjj_["integral"]}  

  #ddd=""" 
  tree.Project("htemp"+name,vvv,ttbb+"*"+tt)
  cccc="ttbb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttbb_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,ttbb+"*"+tt+"*"+S6)
  print cccc+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttbbS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['ttbb']={"GEN":ttbb_,"S6":ttbbS6_, "eff1":ttbbS6_["events"]/ttbb_["events"], "eff2":ttbbS6_["integral"]/ttbb_["integral"]}  
  
  tree.Project("htemp"+name,vvv,ttb+"*"+tt)
  dddd="ttb events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttb_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,ttb+"*"+tt+"*"+S6)
  print dddd+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttbS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['ttb']={"GEN":ttb_,"S6":ttbS6_, "eff1":ttbS6_["events"]/ttb_["events"], "eff2":ttbS6_["integral"]/ttb_["integral"]}  
  
  tree.Project("htemp"+name,vvv,ttcc+"*"+tt)
  eeee="ttcc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttcc_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,ttcc+"*"+tt+"*"+S6)
  print eeee+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttccS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['ttcc']={"GEN":ttcc_,"S6":ttccS6_, "eff1":ttccS6_["events"]/ttcc_["events"], "eff2":ttccS6_["integral"]/ttcc_["integral"]}  
  
  #tree.Project("htemp"+name,vvv,ttc+"*"+tt)
  #ffff="ttc events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  #tree.Project("htemp"+name,vvv,ttc+"*"+tt+"*"+S6)
  #print ffff+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  
  tree.Project("htemp"+name,vvv,ttlf+"*"+tt)
  gggg="ttlf events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttlf_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  tree.Project("htemp"+name,vvv,ttlf+"*"+tt+"*"+S6)
  print gggg+" S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  ttlfS6_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  summary['ttlf']={"GEN":ttlf_,"S6":ttlfS6_, "eff1":ttlfS6_["events"]/ttlf_["events"], "eff2":ttlfS6_["integral"]/ttlf_["integral"] }  
  summary["ratio"]={"events":ttbb_["events"]/ttjj_["events"],"integral":ttbb_["integral"]/ttjj_["integral"],"eventsS6":ttbbS6_["events"]/ttjjS6_["events"],"integralS6":ttbbS6_["integral"]/ttjjS6_["integral"]}
  #"""
  return summary

ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
loc = "/store/user/youngjo/Cattools/v7-4-6v4/"
z="v3GenTopTest"

mg5=ntuple2entries(files(loc + ttbarMG5+z),ttbarMG5)
amc=ntuple2entries(files(loc + ttbarAMC+z),ttbarAMC)
pow=ntuple2entries(files(loc + ttbarPOW+z),ttbarPOW)

allsummary={}
allsummary["MG5"]=mg5
allsummary["AMC"]=amc
allsummary["POW"]=pow

print str(allsummary)

for j  in allsummary.keys():
  print j
  for i  in allsummary[j].keys():
    if i.find("ratio")==-1:
      print i+"  &  "+str(int(allsummary[j][i]["GEN"]["events"]))+"  &  "+str(int(allsummary[j][i]["S6"]["events"]))+" & "+str(round(allsummary[j][i]["eff1"]*100000)/1000)+"\%  \\\\ "
  print " &"+str(round(allsummary[j]["ratio"]["events"]*100000)/1000)+" \% &  "+str(round(allsummary[j]["ratio"]["eventsS6"]*100000)/1000)+" \% &  \\\\ "

for j  in allsummary.keys():
  print j
  for i  in allsummary[j].keys():
    if i.find("ratio")==-1:
      print i+"  &  "+str(int(allsummary[j][i]["GEN"]["integral"]))+"  &  "+str(int(allsummary[j][i]["S6"]["integral"]))+" & "+str(round(allsummary[j][i]["eff2"]*100000)/1000)+"\%  \\\\ "
  print " &"+str(round(allsummary[j]["ratio"]["integral"]*100000)/1000)+" \%  &  "+str(round(allsummary[j]["ratio"]["integralS6"]*100000)/1000)+" \% &  \\\\ "



