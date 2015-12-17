
#from mcsample_cfi import *

#mm= "(pseudoTopChannel==3)"
#ee= "(pseudoTopChannel==2)"
#em= "(pseudoTopChannel==1)"

mm= "(channel==3)" 
ee= "(channel==2)"
em= "(channel==1)"

preselection = "(filtered==1)" 
trigger   = "((tri==1)*(filtered==1))"

cut = [ "(step1==1)", "(step2==1)",  "(step3==1)", "(step4==1)","(step5==1)","(step6==1)" ]
mm_cuts ={
"channel": "mm",
"cut": [
   "(1)",
#   preselection,
   "("+mm+"&&"+trigger+")",
   "("+cut[0]+"&&"+mm+"&&"+"(lep1_RelIso<0.15 && lep2_RelIso<0.15)"+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
ee_cuts = {
"channel": "ee",
"cut": [
   "(1)",
#   preselection,
   "("+ee+"&&"+trigger+")",
   "("+cut[0]+"&&"+ee+"&&"+"(lep1_RelIso<0.12 && lep2_RelIso<0.12)"+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
em_cuts = {
"channel": "em",
"cut":[
   "(1)", 
#   preselection,
   "("+em+"&&"+trigger+")",
   "("+cut[0]+"&&"+em+"&&"+"(lep1_RelIso<0.12 && lep2_RelIso<0.15)"+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}

##########
import copy

mm_cutsQCD = copy.deepcopy(mm_cuts)
#mm_cutsQCD["cut"][3]= ll_NonIsoOS

ee_cutsQCD = copy.deepcopy(ee_cuts)
#ee_cutsQCD["cut"][3]= ll_NonIsoOS

em_cutsQCD = copy.deepcopy(em_cuts)
#em_cutsQCD["cut"][3]= ll_NonIsoOS


