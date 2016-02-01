from ROOT import *
from os import listdir
from os.path import isfile, join

#def files(mypath):
#  return [mypath+"/"+f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".root") ]

import os,commands
import subprocess

def files(path):
    #import socket
    #hostname = socket.gethostname()
    #if hostname.find("home")>-1:
    #  llll = [""]
    #  return llll

    cmd, xrdbase = "xrd cms-xrdr.sdfarm.kr ls ","/xrd"
    size = 0
    l = set()
    for x in subprocess.check_output(cmd + xrdbase + path, shell=True).strip().split('\n'):
        xx = x.split()
        if len(xx) == 0: continue
        if xx[0][0] not in ('d', '-'): continue
        xpath = xx[-1]
        if len(xpath) == 0: continue
        xsize = int(xx[1])
        if xpath.startswith(xrdbase): xpath = xpath[len(xrdbase):]
        if xpath in l: continue
        l.add(xpath)
        size += xsize
    lll ="root://cms-xrdr.sdfarm.kr:1094///xrd" 
    llll = [ lll+l1 for l1 in l]
    #print llll
    return llll
    #return l, size

def getEntries(mypath):
  lcgls="lcg-ls -v -b -T srmv2 -D srmv2 --vo cms srm://cms-se.sdfarm.kr:8443/srm/v2/server?SFN="
  aaa = (lcgls_+mypath)
  aaa2= commands.getoutput(aaa)

  bbb = (lcgls_+"/000"+str(Idx_)+"/ | grep -c catTuple ")
  #print bbb
  ddd= commands.getoutput(bbb)
  ddd2= int(ddd)
  if ddd2==999: ddd2+=getEntries(lcgls_,Idx_+1)
  return ddd2

#loc = "../"
#loc = "/xrootd/store/user/youngjo/Cattools/v7-4-6v2/"
loc = "/store/user/youngjo/Cattools/v7-6-1v1/"
ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
ttcx=831.76

def mAND(aaa,bbb):
  return "(" +aaa+ " && "+bbb+")"
def mAND2(aaa):
  bbb=""
  for i,ii in enumerate(aaa):
    if i==0 : 
      bbb+= ii
    else : 
      bbb=mAND(ii,bbb)
  return bbb

visible="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
ttbb = mAND("(NbJets20>=4)",visible)
ttb = mAND("(NbJets20==3)",visible)
ttcc = mAND("((NcJets20>=2) && !(NbJets20>=3))",visible)
ttlf = mAND("(!(NbJets20>=4) && !(NbJets20==3) && !(NcJets20>=2))",visible)

old_definition="""
ll = " (partonInPhaseLep==1 && NgenJet>=4 )"
ttbb = mAND(" (genTtbarId%100>52) ", ll)
ttb  = mAND(" (genTtbarId%100>50 && genTtbarId%100<53) ", ll)
ttc  = mAND(" (genTtbarId%100>40 && genTtbarId%100<43) ", ll)
ttcc = mAND(" (genTtbarId%100>42 && genTtbarId%100<49) ", ll)
ttlf = mAND(" (genTtbarId%100 ==0) ", ll)
"""

def op_(aaa):
  return "!(" + aaa + ")"

def GW(sel="1"):
  return "(("+sel+"))"


ttothers = op_(visible)
#########

#    [ ttbb,     ttb,       ttcc,      ttc,       ttlf,     tt others ]
ColorLabelSet = {}
ColorLabelSet["ttbb"] = {"color":"#660000",  "label":"t#bar{t}+b#bar{b}      " }
ColorLabelSet["ttb"]  = {"color":"#ffcc00",  "label":"t#bar{t}+b        "      }
ColorLabelSet["ttcc"] = {"color":"#cc6600",  "label":"t#bar{t}+c#bar{c}      " }
ColorLabelSet["ttlf"] = {"color":"#ff0000",  "label":"t#bar{t}+lf       "      }
ColorLabelSet["ttot"] = {"color":"#ff6565",  "label":"t#bar{t} others"         }

ColorLabelSet["Singlet"] = {"color":"#ff00ff",  "label":"Single t"            } 
ColorLabelSet["VV"]      = {"color":"#ffffff",  "label":"VV            "      }
ColorLabelSet["WJets"]   = {"color":"#33cc33",  "label":"WJets      "         }
ColorLabelSet["ZJets"]   = {"color":"#3366ff",  "label":"DYJets    "          }
ColorLabelSet["ttV"]     = {"color":"#7676ff",  "label":"t#bar{t}V          " }
ColorLabelSet["ttH"]     = {"color":"#7676ff",  "label":"t#bar{t}H         "  }
ColorLabelSet["DATA"]    = {"color":"#000000",  "label":"DATA "               }


#     [ Single t,   VV,        WJets,    Z+Jets ,   ttV
#BCS = ["#ff00ff",   "#ffffff", "#33cc33","#3366ff", "#7676ff" ]
########
import json

def loadJson(name):
  with open(name) as data_file:    
    data = json.load(data_file)
    return data

data = loadJson('dataset.json')
cx = {}
for aa in data:
  cx[aa["name"]]=aa["xsec"]
print str(cx)

#["TTWlNu","TTWqq',"TTZll","TTZqq",  "STbt","STt","STbtW","STtW",  "WW","WZ","ZZ",  "WJets","DYJets","DYJets10",  "ttH2non","ttH2bb"]
#BCX=[0.2043,0.4062,0.2529,0.5297,    35.6,35.6,43.79844,26.0659,   110.8,47.13,16.523,  61526.7,6025.2,18610.0,     0.5058,0.5058]

z  ="v3"
zz ="v3"
zzz="v3"
mcsamples=[
{"name":"MG5ttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttbb"]    },
#{"name":"MG5tt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttbb"]   },
{"name":"MG5ttb",   "selection": GW(ttb),      "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttb"]     },
{"name":"MG5ttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttcc"]    },
#{"name":"MG5ttc",   "selection": GW(ttc),      "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttc"]    },   
{"name":"MG5ttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttlf"]    },
{"name":"MG5ttot",  "selection": GW(ttothers), "file": files(loc + ttbarMG5+zzz), "cx":cx[ttbarMG5], "ColorLabel": ColorLabelSet["ttot"]    },

{"name":"AMCttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttbb"]    },
#{"name":"AMCtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttbb"]   },
{"name":"AMCttb",   "selection": GW(ttb),      "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttb"]     },
{"name":"AMCttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttcc"]    },
#{"name":"AMCttc",   "selection": GW(ttc),      "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttc"]    },   
{"name":"AMCttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttlf"]    },
{"name":"AMCttot",  "selection": GW(ttothers), "file": files(loc + ttbarAMC+zzz), "cx":cx[ttbarAMC], "ColorLabel": ColorLabelSet["ttot"]    },

{"name":"POWttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttbb"]    },
#{"name":"POWtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttbb"]   },
{"name":"POWttb",   "selection": GW(ttb),      "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttb"]     },
{"name":"POWttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttcc"]    },
#{"name":"POWttc",   "selection": GW(ttc),      "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttc"]    },
{"name":"POWttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttlf"]    },
{"name":"POWttot",  "selection": GW(ttothers), "file": files(loc + ttbarPOW+zzz), "cx":cx[ttbarPOW], "ColorLabel": ColorLabelSet["ttot"]    },

{"name":"TTWlNu", "selection": "(1)", "file": files(loc + "ttWJetsToLNu"+z),  "cx":cx["ttWJetsToLNu"], "ColorLabel": ColorLabelSet["ttV"]    },
{"name":"TTWqq",  "selection": "(1)", "file": files(loc + "ttWJetsToQQ"+z),   "cx":cx["ttWJetsToQQ"],  "ColorLabel": ColorLabelSet["ttV"]    },
{"name":"TTZll",  "selection": "(1)", "file": files(loc + "ttZToLLNuNu"+z),   "cx":cx["ttZToLLNuNu"],  "ColorLabel": ColorLabelSet["ttV"]    },
{"name":"TTZqq",  "selection": "(1)", "file": files(loc + "ttZToQQ"+z),       "cx":cx["ttZToQQ"],      "ColorLabel": ColorLabelSet["ttV"]    },

{"name":"STbt",   "selection": "(1)", "file": files(loc + "SingleTbar_t"+z),  "cx":cx["SingleTbar_t"],  "ColorLabel": ColorLabelSet["Singlet"]   },
{"name":"STt",    "selection": "(1)", "file": files(loc + "SingleTop_t"+z),   "cx":cx["SingleTop_t"],   "ColorLabel": ColorLabelSet["Singlet"]   },
{"name":"STbtW",  "selection": "(1)", "file": files(loc + "SingleTbar_tW"+z), "cx":cx["SingleTbar_tW"], "ColorLabel": ColorLabelSet["Singlet"]   },
{"name":"STtW",   "selection": "(1)", "file": files(loc + "SingleTop_tW"+z),  "cx":cx["SingleTop_tW"],  "ColorLabel": ColorLabelSet["Singlet"]   },
{"name":"WW",     "selection": "(1)", "file": files(loc + "WW"+z),            "cx":cx["WW"],            "ColorLabel": ColorLabelSet["VV"]        },
{"name":"WZ",     "selection": "(1)", "file": files(loc + "WZ"+z),            "cx":cx["WZ"],            "ColorLabel": ColorLabelSet["VV"]        },
{"name":"ZZ",     "selection": "(1)", "file": files(loc + "ZZ"+z),            "cx":cx["ZZ"],            "ColorLabel": ColorLabelSet["VV"]        },

{"name":"WJets",  "selection": "(1)", "file": files(loc + "WJets"+z),         "cx":cx["WJets"],         "ColorLabel": ColorLabelSet["WJets"]     },

{"name":"DYJets", "selection": "(1)", "file": files(loc + "DYJets"+z),        "cx":cx["DYJets"],        "ColorLabel": ColorLabelSet["ZJets"]     },
{"name":"DYJets10", "selection": "(1)", "file": files(loc +"DYJets_10to50"+z),"cx":cx["DYJets_10to50"], "ColorLabel": ColorLabelSet["ZJets"]     },

{"name":"ttH2non", "selection": "(1)", "file": files(loc + "ttH_nonbb"+z),  "cx":cx["ttH_nonbb"],       "ColorLabel": ColorLabelSet["ttH"],   "isStack":False   },
{"name":"ttH2bb",  "selection": "(1)", "file": files(loc + "ttH_bb"+z),     "cx":cx["ttH_bb"],          "ColorLabel": ColorLabelSet["ttH"],   "isStack":False   },
]

mcsamples2=[
{"name":"DYJets", "selection": "(1)", "file": files(loc + "DYJets"+z),        "cx":cx["DYJets"],        "ColorLabel": ColorLabelSet["ZJets"]     },
{"name":"DYJets10", "selection": "(1)", "file": files(loc +"DYJets_10to50"+z),"cx":cx["DYJets_10to50"], "ColorLabel": ColorLabelSet["ZJets"]     },
]
datasamples=[

{"name":"MuMu1", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015C"+zz),  "ColorLabel": ColorLabelSet["DATA"] },
{"name":"MuMu2", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015D"+zz),  "ColorLabel": ColorLabelSet["DATA"] },

{"name":"ElEl1", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015C"+zz),    "ColorLabel": ColorLabelSet["DATA"] },
{"name":"ElEl2", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015D"+zz),    "ColorLabel": ColorLabelSet["DATA"] },

{"name":"MuEl1", "selection": "(1)", "file": files(loc + "MuonEG_Run2015C"+zz),      "ColorLabel": ColorLabelSet["DATA"] },
{"name":"MuEl2", "selection": "(1)", "file": files(loc + "MuonEG_Run2015D"+zz),      "ColorLabel": ColorLabelSet["DATA"] },

]
