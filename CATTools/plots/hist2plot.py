from ROOT import *
import copy

from hist2plot_cff import *
from mcsample_cfi import *
from monitors_cfi import *

#import sys 
gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()

mon = monitors

mon2 = []
for i,ii in enumerate(monitors2d):
  #print monitors2d[ii]
  mon2.append(monitors2d[ii])

json = {
"file": "hist_all.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
"cuts" : [
"mm_S2","mm_S3","mm_S4",
"mm_S5", #"mm_S5csvweight", "mm_S5csvt_sf", "mm_S5csvm_sf", "mm_S5csvl_sf",
"mm_S6", "mm_S6csvweight", #"mm_S6csvt_sf", "mm_S6csvm_sf", "mm_S6csvl_sf",
#"mm_S7", "mm_S7csvweight", "mm_S7csvt_sf", "mm_S7csvm_sf", "mm_S7csvl_sf",
"ee_S2","ee_S3","ee_S4",
"ee_S5", #"ee_S5csvweight", "ee_S5csvt_sf", "ee_S5csvm_sf", "ee_S5csvl_sf",
"ee_S6", "ee_S6csvweight", #"ee_S6csvt_sf", "ee_S6csvm_sf", "ee_S6csvl_sf",
#"ee_S7", "ee_S7csvweight", "ee_S7csvt_sf", "ee_S7csvm_sf", "ee_S7csvl_sf",
"em_S2","em_S3","em_S4",
"em_S5", #"em_S5csvweight", "em_S5csvt_sf", "em_S5csvm_sf", "em_S5csvl_sf",
"em_S6", "em_S6csvweight", #"em_S6csvt_sf", "em_S6csvm_sf", "em_S6csvl_sf",
#"em_S7", "em_S7csvweight", "em_S7csvt_sf", "em_S7csvm_sf", "em_S7csvl_sf"
   ],
"monitors" : mon,
"monitors2" : mon2
}

#########
def mmeeem():
  #TH1F
  f = json['file'] #TFile.Open(json['file'],"read")
  #singleplotStack2(f,"MET","S2em",json['mcsamples'],json['datasamples'],False)
  ######
  for step in json['cuts']:
    for mon in json['monitors']:
      #singleplotStack2(f,mon['name'],step,json['mcsamples'],json['datasamples'],False)
      singleplotStack2(f,mon,step,json['mcsamples'],json['datasamples'],False)

def mmeeem2d():
  #TH2F
  ddd="""
  for step in json['cuts']:
    for ii,mon in enumerate(json['monitors2']):
      for i,mon1 in enumerate(mon):
        for j,mon2 in enumerate(mon):
          if i<j :
            mon_ = mon1['name']+"_"+mon2['name']
            #plotTH2F(f,mon_,step,json['mcsamples'],json['datasamples'])
  """

jsonLL = {
"file": "hist_all.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
"cuts" : [
#"S0","S1","S2","S3","S4","S5","S6","S7"
"S2","S3","S4",
"S5", #"S5csvweight", "S5csvt_sf", "S5csvm_sf", "S5csvl_sf",
"S6", "S6csvweight",# "S6csvt_sf", "S6csvm_sf", "S6csvl_sf",
#"S7", "S7csvweight", "S7csvt_sf", "S7csvm_sf", "S7csvl_sf"
   ],
"monitors" : mon,
"monitors2" : mon2
}

def ll():
  f1 = jsonLL['file'] #TFile.Open(json['file'],"read")
  for step1 in jsonLL['cuts']:
    for mon1 in jsonLL['monitors']:
      #singleplotStackLL2(f1,mon1['name'],step1,jsonLL['mcsamples'],jsonLL['datasamples'],False)
      singleplotStackLL2(f1,mon1,step1,jsonLL['mcsamples'],jsonLL['datasamples'],False)

import sys
if len(sys.argv) < 2:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)

if int(arg1)==0:
  mmeeem()
else :
  ll()

