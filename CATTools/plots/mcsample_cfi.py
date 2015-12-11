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
loc = "/store/user/youngjo/Cattools/v7-4-6v2/"
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

ll = " (partonInPhaseLep==1 && NgenJet>=4 )"
ttbb = mAND(" (genTtbarId%100>52) ", ll)
ttb  = mAND(" (genTtbarId%100>50 && genTtbarId%100<53) ", ll)
#ttb = mAND(" (genTtbarId%100==51) ", ll)
#tt2b = mAND(" (genTtbarId%100==52) ", ll)
ttc  = mAND(" (genTtbarId%100==41) ", ll)
ttcc = mAND(" (genTtbarId%100>41 && genTtbarId%100<49) ", ll)
ttlf = mAND(" (genTtbarId%100 ==0) ", ll)

def op_(aaa):
  return "!(" + aaa + ")"

def GW(sel="1"):
  return "(("+sel+"))"#*(puweight)*(csvweight))"
  #return "(("+sel+")*(weight/abs(weight))*(puweight)*(csvweight))"

def GW2(sel="1"):
  return "(("+sel+"))"#*(puweight)*(csvweight))"

#ttotheslist = [op_(ttbb), op_(ttb), op_(tt2b),op_(ttc), op_(ttcc),op_(ttlf) ]
ttotheslist = [op_(ttbb), op_(ttb), op_(ttc), op_(ttcc),op_(ttlf) ]
ttothers = mAND2(ttotheslist)

CS = [kOrange, kOrange-1, kRed-7, kRed+2, kMagenta,kMagenta+2, kRed ]
BCS = [kBlue,kGreen+2,kGray,kViolet,kCyan]

z="v7"
zz="v6"
mcsamples=[

{"name":"MG5ttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[0],   "label":"t#bar{t}+b#bar{b}      " },
#{"name":"MG5tt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[2],   "label":"t#bar{t}+2b      "       },
{"name":"MG5ttb",   "selection": GW(ttb),      "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[1],   "label":"t#bar{t}+b        "      },
{"name":"MG5ttc",   "selection": GW(ttc),      "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[3],   "label":"t#bar{t}+c        " },
{"name":"MG5ttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[4],   "label":"t#bar{t}+c#bar{c}      " },
{"name":"MG5ttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[5],   "label":"t#bar{t}+lf       "      },
{"name":"MG5ttot",  "selection": GW(ttothers), "file": files(loc + ttbarMG5+z), "cx":ttcx, "color": CS[6],   "label":"t#bar{t} others"         },

{"name":"AMCttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[0],   "label":"t#bar{t}+b#bar{b}      " },
#{"name":"AMCtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[2],   "label":"t#bar{t}+2b      "       },
{"name":"AMCttb",   "selection": GW(ttb),      "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[1],   "label":"t#bar{t}+b        "      },
{"name":"AMCttc",   "selection": GW(ttc),      "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[3],   "label":"t#bar{t}+c        " },
{"name":"AMCttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[4],   "label":"t#bar{t}+c#bar{c}      " },
{"name":"AMCttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[5],   "label":"t#bar{t}+lf       "      },
{"name":"AMCttot",  "selection": GW(ttothers), "file": files(loc + ttbarAMC+z), "cx":ttcx, "color": CS[6],   "label":"t#bar{t} others"         },

{"name":"POWttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[0],  "label":"t#bar{t}+b#bar{b}      " },
#{"name":"POWtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[2],  "label":"t#bar{t}+2b      "       },
{"name":"POWttb",   "selection": GW(ttb),      "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[1],  "label":"t#bar{t}+b        "      },
{"name":"POWttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[3],  "label":"t#bar{t}+c#bar{c}      " },
{"name":"POWttc",   "selection": GW(ttc),      "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[4],  "label":"t#bar{t}+c        " },
{"name":"POWttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[5],  "label":"t#bar{t}+lf        "      },
{"name":"POWttot",  "selection": GW(ttothers), "file": files(loc + ttbarPOW+z), "cx":ttcx, "color": CS[6],  "label":"t#bar{t} others"         },

{"name":"TTWlNu", "selection": GW(), "file": files(loc + "ttWJetsToLNu"+z),  "cx":1.152,  "color": BCS[0],   "label":"t#bar{t}V          "    },
{"name":"TTWqq",  "selection": GW(), "file": files(loc + "ttWJetsToQQ"+z),   "cx":1.152,  "color": BCS[0],   "label":"t#bar{t}V          "    },
{"name":"TTZll",  "selection": GW(), "file": files(loc + "ttZToLLNuNu"+z),   "cx":2.232,  "color": BCS[0],   "label":"t#bar{t}V          "    },
{"name":"TTZqq",  "selection": GW(), "file": files(loc + "ttZToQQ"+z),       "cx":2.232,  "color": BCS[0],   "label":"t#bar{t}V          "    },

{"name":"STbt",   "selection": GW(), "file": files(loc + "SingleTbar_t"+z),  "cx":80.95,  "color": BCS[3],   "label":"Single t"    },
{"name":"STt",    "selection": GW(), "file": files(loc + "SingleTop_t"+z),   "cx":136.02, "color": BCS[3],   "label":"Single t"    },
{"name":"STbtW",  "selection": GW(), "file": files(loc + "SingleTbar_tW"+z), "cx":35.6,   "color": BCS[3],   "label":"Single t"      },
{"name":"STtW",   "selection": GW(), "file": files(loc + "SingleTop_tW"+z),  "cx":35.6,   "color": BCS[3],   "label":"Single t"      },
{"name":"WW",     "selection": GW(), "file": files(loc + "WW"+z),            "cx":110.8,  "color": BCS[2],   "label":"VV            "    },
{"name":"WZ",     "selection": GW(), "file": files(loc + "WZ"+z),            "cx":66.1,   "color": BCS[2],   "label":"VV            "   },
{"name":"ZZ",     "selection": GW(), "file": files(loc + "ZZ"+z),            "cx":15.4,   "color": BCS[2],   "label":"VV            "   },

{"name":"WJets",  "selection": GW(), "file": files(loc + "WJets"+z),         "cx":61526.7,"color": BCS[1],   "label":"WJets      "       },
{"name":"DYJets", "selection": GW(), "file": files(loc + "DYJets"+z),        "cx":6025.2, "color": BCS[1], "label":"DYJets    "      },
{"name":"DYJets10", "selection": GW(), "file": files(loc + "DYJets_10to50"+z),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },

#{"name":"DYRin", "selection": GW("(ll_zmass-91.2<=15)"+z), "file": files(loc + "DYJets"+z),        "cx":6025.2, "color": BCS[1], "label":"DYJets    "      },
#{"name":"DYRout", "selection": GW("(ll_zmass-91.2>15)"+z), "file": files(loc + "DYJets"+z),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },
#{"name":"DYRout", "selection": GW(), "file": files(loc + "DYJets_10to50"+z),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },


{"name":"ttH2non", "selection": GW(), "file": files(loc + "ttH_nonbb"+z),  "cx":0.5058,   "color": BCS[2],   "label":"t#bar{t}H         " ,"isStack":False   },
{"name":"ttH2bb",  "selection": GW(), "file": files(loc + "ttH_bb"+z),     "cx":0.5058,   "color": BCS[2],   "label":"t#bar{t}H         " ,"isStack":False   },
]

datasamples=[

{"name":"MuMu1", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015C"+zz),  "color":kBlack,  "label":"DATA " },
{"name":"MuMu2", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015D"+zz),  "color":kBlack,  "label":"DATA " },
{"name":"MuMu3", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015Dprompt"+zz),  "color":kBlack,  "label":"DATA " },

{"name":"ElEl1", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015C"+zz),    "color":kBlack,  "label":"DATA " },
{"name":"ElEl2", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015D"+zz),    "color":kBlack,  "label":"DATA " },
{"name":"ElEl3", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015Dprompt"+zz),    "color":kBlack,  "label":"DATA " },

{"name":"MuEl1", "selection": "(1)", "file": files(loc + "MuonEG_Run2015C"+zz),      "color":kBlack,  "label":"DATA " },
{"name":"MuEl2", "selection": "(1)", "file": files(loc + "MuonEG_Run2015D"+zz),      "color":kBlack,  "label":"DATA " },
{"name":"MuEl3", "selection": "(1)", "file": files(loc + "MuonEG_Run2015Dprompt"+zz),      "color":kBlack,  "label":"DATA " },

]
