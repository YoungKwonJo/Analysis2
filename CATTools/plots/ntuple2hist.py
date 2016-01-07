import sys 

from ntuple2hist_cff import *
from mcsample_cfi import * 
from monitors_cfi import *
from cut_cfi import *

if len(sys.argv) is 1:
  print "Please, add the name as like followings."
  print "> python  ntuple2hist.py [1,2,3, or 4] \n"
  sys.exit()

#gROOT.ProcessLine(".L MuonSF.C")
#mumusf ="((channel==3)*(MuonSF(lep1_pt,lep1_eta)*MuonSF(lep2_pt,lep2_eta)))"
#emusf ="((channel==1)*(MuonSF(lep2_pt,lep2_eta)))"
#eesf = "((channel==2)*(1.0))"
#lepsf = "("+mumusf+"+"+emusf+"+"+eesf+")"

arg = sys.argv[1]
ii=int(arg)
if ii>len(monitors)+1 : sys.exit()
#if ii>len(monitors) : sys.exit()

mon1=[]
if ii<len(monitors) :
  mon1 = [monitors[ii]]
  #print monitors[ii]

mon2=[]
iii = ii#-len(monitors)+1
for mon22 in monitors2d.keys():
  if mon22 == ("Mon"+str(iii)) :
    mon2+=monitors2d["Mon" +str(iii)]
    print "++"+str(mon2)+"++"

#mceventweight="puWeight"
mceventweight=["((weight/abs(weight))*(puweight)(lepweight))","csvweight",
"csvweight_JES_Up",          
"csvweight_JES_Down",        
"csvweight_LF_Up",           
"csvweight_LF_Down",         
"csvweight_HF_Up",           
"csvweight_HF_Down",         
"csvweight_HF_Stats1_Up",    
"csvweight_HF_Stats1_Down",  
"csvweight_HF_Stats2_Up",    
"csvweight_HF_Stats2_Down",  
"csvweight_LF_Stats1_Up",    
"csvweight_LF_Stats1_Down",  
"csvweight_LF_Stats2_Up",    
"csvweight_LF_Stats2_Down",  
"csvweight_Charm_Err1_Up",   
"csvweight_Charm_Err1_Down", 
"csvweight_Charm_Err2_Up",   
"csvweight_Charm_Err2_Down" 
#"csvt_sf","csvm_sf","csvl_sf","csvt_sfup","csvt_sfdw","csvm_sfup","csvm_sfdw","csvl_sfup","csvl_sfdw"
]

jsonMM = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
#"monitors" : monitors["Mon1"],
"monitors2" : mon2,
#"monitors2" : [],
"cuts" : mm_cuts, 
"cutsQCD" : mm_cutsQCD, 
"output" : "hist_mon" + arg +mm_cuts["channel"]+ ".root"
}

makehist(jsonMM)
#makehist2(json)

jsonEE = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
#"monitors" : monitors["Mon1"],
"monitors2" : mon2,
#"monitors2" : [],
"cuts" : ee_cuts,
"cutsQCD" : ee_cutsQCD, 
"output" : "hist_mon" + arg +ee_cuts["channel"]+ ".root"
}
makehist(jsonEE)

jsonEM = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
#"monitors" : monitors["Mon1"],
"monitors2" : mon2,
#"monitors2" : [],
"cuts" : em_cuts,
"cutsQCD" : em_cutsQCD, 
"output" : "hist_mon" + arg +em_cuts["channel"]+ ".root"
}
makehist(jsonEM)

