import sys 

from ntuple2hist_cff import *
from mcsample_cfi import * 
from monitors_cfi import *
from cut_cfi import *

if len(sys.argv) is 1:
  print "Please, add the name as like followings."
  print "> python  ntuple2hist.py [1,2,3, or 4] \n"
  sys.exit()

arg = sys.argv[1]
ii=int(arg)
jj=len(mm_cuts["cut"])
iijj = int(ii/jj)
cuti= int(ii%jj)

if iijj>len(monitors)+1 : sys.exit()

mm_cut=cut_maker(mm_cuts,cuti)
ee_cut=cut_maker(ee_cuts,cuti)
em_cut=cut_maker(em_cuts,cuti)


mon1=[]
if iijj<len(monitors) :
  mon1 = [monitors[iijj]]
  #print monitors[ii]

mon2=[]
for mon22 in monitors2d.keys():
  if mon22 == ("Mon%d"%iijj) :
    mon2+=monitors2d[ ("Mon%d"%iijj) ]
    print "++"+str(mon2)+"++"

#mceventweight="puWeight"
baseWeight = "weight*puweight*lepweight"
mceventweight={
"CEN"                 : "("+baseWeight+")",
"csvweight"           : "("+baseWeight+"*csvweight)",
"PuWeightUp"          : "(weight*puweightUp*lepweight*csvweight)",
"PUWeightDN"          : "(weight*puweightDown*lepweight*csvweight)",
"JER_Up"              : "("+baseWeight+"*csvweight)",
"JER_Down"            : "("+baseWeight+"*csvweight)",
"csvweight_JES_Up"    : "("+baseWeight+"*csvweight_JES_Up)",        
"csvweight_JES_Down"  : "("+baseWeight+"*csvweight_JES_Down)",      
"csvweight_LF_Up"     : "("+baseWeight+"*csvweight_LF_Up)",         
"csvweight_LF_Down"   : "("+baseWeight+"*csvweight_LF_Down)",       
#]
#ddddd=[
"csvweight_HF_Up"          :  "("+baseWeight+"*csvweight_HF_Up)",           
"csvweight_HF_Down"        :  "("+baseWeight+"*csvweight_HF_Down)",         
"csvweight_HF_Stats1_Up"   :  "("+baseWeight+"*csvweight_HF_Stats1_Up)",    
"csvweight_HF_Stats1_Down" :  "("+baseWeight+"*csvweight_HF_Stats1_Down)",  
"csvweight_HF_Stats2_Up"   :  "("+baseWeight+"*csvweight_HF_Stats2_Up)",    
"csvweight_HF_Stats2_Down" :  "("+baseWeight+"*csvweight_HF_Stats2_Down)",  
"csvweight_LF_Stats1_Up"   :  "("+baseWeight+"*csvweight_LF_Stats1_Up)",    
"csvweight_LF_Stats1_Down" :  "("+baseWeight+"*csvweight_LF_Stats1_Down)",  
"csvweight_LF_Stats2_Up"   :  "("+baseWeight+"*csvweight_LF_Stats2_Up)",    
"csvweight_LF_Stats2_Down" :  "("+baseWeight+"*csvweight_LF_Stats2_Down)",  
"csvweight_Charm_Err1_Up"  :  "("+baseWeight+"*csvweight_Charm_Err1_Up)",   
"csvweight_Charm_Err1_Down":  "("+baseWeight+"*csvweight_Charm_Err1_Down)", 
"csvweight_Charm_Err2_Up"  :  "("+baseWeight+"*csvweight_Charm_Err2_Up)",   
"csvweight_Charm_Err2_Down":  "("+baseWeight+"*csvweight_Charm_Err2_Down)" 
#"csvt_sf","csvm_sf","csvl_sf","csvt_sfup","csvt_sfdw","csvm_sfup","csvm_sfdw","csvl_sfup","csvl_sfdw"
}

jsonMM = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : mm_cut, 
"output" : "hist_mon" + arg +mm_cut["channel"]+ ".root"
}

makehist(jsonMM)

jsonEE = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : ee_cut,
"output" : "hist_mon" + arg +ee_cut["channel"]+ ".root"
}
makehist(jsonEE)

jsonEM = {
"mcsamples" : mcsamples,
"mceventweight": mceventweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : em_cut,
"output" : "hist_mon" + arg +em_cut["channel"]+ ".root"
}
makehist(jsonEM)

