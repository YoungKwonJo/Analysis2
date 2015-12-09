from ROOT import *
import copy

from hist2plot_cff import *
from mcsample_cfi import *
from monitors_cfi import *

#import sys 

mon = monitors
#for i,ii in enumerate(monitors):
#  #print monitors[ii]
#  mon+=monitors[ii]

mon2 = []
for i,ii in enumerate(monitors2d):
  #print monitors2d[ii]
  mon2.append(monitors2d[ii])

json = {
"file": "hist_all.root",
#"file": "hist_all2.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
#"cuts" : ["S0","S1","S2","S3","S4","S5"],
#"cuts" : ["S0","S1","S2","S3"],
#"cuts" : ["S0","S1","S2","S3","S4","S5","S6"],
"cuts" : [
"S0mm","S1mm","S2mm","S3mm","S4mm","S5mm","S6mm","S7mm",
"S0ee","S1ee","S2ee","S3ee","S4ee","S5ee","S6ee","S7ee",
"S0em","S1em","S2em","S3em","S4em","S5em","S6em","S7em"
   ],
#"cuts" : ["S6"],

#"monitors" : monitors["jetMon3"]
"monitors" : mon,
"monitors2" : mon2
}

#########
#TH1F
f = json['file'] #TFile.Open(json['file'],"read")
#singleplotStack2(f,"MET","S2em",json['mcsamples'],json['datasamples'],False)
######
#for step in json['cuts']:
#  for mon in json['monitors']:
#    singleplotStack2(f,mon['name'],step,json['mcsamples'],json['datasamples'],False)


#########
#TH2F
#for step in json['cuts']:
#  for ii,mon in enumerate(json['monitors2']):
#    for i,mon1 in enumerate(mon):
#      for j,mon2 in enumerate(mon):
#        if i<j :
#          mon_ = mon1['name']+"_"+mon2['name']
#          plotTH2F(f,mon_,step,json['mcsamples'],json['datasamples'])

jsonLL = {
"file": "hist_all.root",
#"file": "hist_all2.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
#"cuts" : ["S0","S1","S2","S3","S4","S5"],
#"cuts" : ["S0","S1","S2","S3"],
#"cuts" : ["S0","S1","S2","S3","S4","S5","S6"],
"cuts" : [
"S0","S1","S2","S3","S4","S5","S6","S7"
   ],
#"cuts" : ["S6"],

#"monitors" : monitors["jetMon3"]
"monitors" : mon,
"monitors2" : mon2
}

f1 = jsonLL['file'] #TFile.Open(json['file'],"read")
for step1 in jsonLL['cuts']:
  for mon1 in jsonLL['monitors']:
    singleplotStackLL2(f1,mon1['name'],step1,jsonLL['mcsamples'],jsonLL['datasamples'],False)


