
#from mcsample_cfi import *

mm= "(channel==26)" 
ee= "(channel==22)"
em= "(channel==24)"

preselection = "(filtered==1)" 
trigger   = "(tri==1)"

cut = [ "(step1==1)", "(step2==1)",  "(step3==1)", "(step4==1)","(step5==1)","(step6==1)" ]
mm_cuts ={
"channel": "mm",
"cut": [
   mm,
#   preselection,
   trigger,
   cut[0], cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
ee_cuts = {
"channel": "ee",
"cut": [
   ee,
#   preselection,
   trigger,
   cut[0], cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
em_cuts = {
"channel": "em",
"cut":[
   em,
#   preselection,
   trigger,
   cut[0], cut[1], cut[2], cut[3], cut[4], cut[5]
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


