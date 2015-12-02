from ROOT import *
from os import listdir
from os.path import isfile, join

def files(mypath):
  return [mypath+"/"+f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".root") ]


#loc = "../"
loc = "/xrootd/store/user/youngjo/Cattools/v7-4-6/"
ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
ttcx=815.96

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

"""
         int category =0; // 0:tt+lf, 1:tt+cc, 2:tt+bb, 3:tt+2b, 4:tt+b  
         int categorytb =0;
         if(genTtbarId%100 == 0)                   category=0;
         else if( ((int)(genTtbarId%100)/10) == 4) category=1;
         else if( ((int)(genTtbarId%100)) == 51)   category=4;
         else if( ((int)(genTtbarId%100)) == 52)   category=3;
         else if( ((int)(genTtbarId%100)) == 53)   category=2;
         else if( ((int)(genTtbarId%100)) == 54)   category=2;
         else if( ((int)(genTtbarId%100)) == 55)   category=2;
         categorytb=(int)(genTtbarId/100);
"""
ll = " (partonInPhaseLep==1 && NgenJet>=4 )"
ttbb = mAND(" (genTtbarId%100>52) ", ll)
ttb  = mAND(" (genTtbarId%100==51) ", ll)
tt2b = mAND(" (genTtbarId%100==52) ", ll)
ttc  = mAND(" (genTtbarId%100==41) ", ll)
ttcc = mAND(" (genTtbarId%100>41 && genTtbarId%100<49) ", ll)
ttlf = mAND(" (genTtbarId%100 ==0) ", ll)

def op_(aaa):
  return "!(" + aaa + ")"

def GW(sel="1"):
  return "(("+sel+")*(weight/abs(weight)))"

ttotheslist = [op_(ttbb), op_(ttb), op_(tt2b),op_(ttc), op_(ttcc),op_(ttlf) ]
ttothers = mAND2(ttotheslist)

CS = [kOrange, kRed-7, kRed+2, kMagenta,kMagenta,kMagenta+2,kRed ]
BCS = [kBlue,kGreen+2,kGray,kViolet,kCyan]

mcsamples=[

{"name":"MG5ttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[0],   "label":"t#bar{t}+b#bar{b}      " },
{"name":"MG5tt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[2],   "label":"t#bar{t}+2b      "       },
{"name":"MG5ttb",   "selection": GW(ttb),      "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[1],   "label":"t#bar{t}+b        "      },
{"name":"MG5ttc",   "selection": GW(ttc),      "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[3],   "label":"t#bar{t}+c        " },
{"name":"MG5ttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[4],   "label":"t#bar{t}+c#bar{c}      " },
{"name":"MG5ttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[5],   "label":"t#bar{t}+lf       "      },
{"name":"MG5ttot",  "selection": GW(ttothers), "file": files(loc + ttbarMG5), "cx":ttcx, "color": CS[6],   "label":"t#bar{t} others"         },

{"name":"AMCttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[0],   "label":"t#bar{t}+b#bar{b}      " },
{"name":"AMCtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[2],   "label":"t#bar{t}+2b      "       },
{"name":"AMCttb",   "selection": GW(ttb),      "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[1],   "label":"t#bar{t}+b        "      },
{"name":"AMCttc",   "selection": GW(ttc),      "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[3],   "label":"t#bar{t}+c        " },
{"name":"AMCttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[4],   "label":"t#bar{t}+c#bar{c}      " },
{"name":"AMCttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[5],   "label":"t#bar{t}+lf       "      },
{"name":"AMCttot",  "selection": GW(ttothers), "file": files(loc + ttbarAMC), "cx":ttcx, "color": CS[6],   "label":"t#bar{t} others"         },

{"name":"POWttbb",  "selection": GW(ttbb),     "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[0],  "label":"t#bar{t}+b#bar{b}      " },
{"name":"POWtt2b",  "selection": GW(tt2b),     "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[2],  "label":"t#bar{t}+2b      "       },
{"name":"POWttb",   "selection": GW(ttb),      "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[1],  "label":"t#bar{t}+b        "      },
{"name":"POWttc",   "selection": GW(ttc),      "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[3],  "label":"t#bar{t}+c        " },
{"name":"POWttcc",  "selection": GW(ttcc),     "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[4],  "label":"t#bar{t}+c#bar{c}      " },
{"name":"POWttlf",  "selection": GW(ttlf),     "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[5],  "label":"t#bar{t}+lf        "      },
{"name":"POWttot",  "selection": GW(ttothers), "file": files(loc + ttbarPOW), "cx":ttcx, "color": CS[6],  "label":"t#bar{t} others"         },

{"name":"TTWlNu", "selection": GW(), "file": files(loc + "ttWJetsToLNu"),  "cx":1.152,  "color": BCS[0],   "label":"t#bar{t}W          "    },
{"name":"TTWqq",  "selection": GW(), "file": files(loc + "ttWJetsToQQ"),   "cx":1.152,  "color": BCS[0],   "label":"t#bar{t}W          "    },
{"name":"TTZll",  "selection": GW(), "file": files(loc + "ttZToLLNuNu"),   "cx":2.232,  "color": BCS[0],   "label":"t#bar{t}Z          "    },
{"name":"TTZqq",  "selection": GW(), "file": files(loc + "ttZToQQ"),       "cx":2.232,  "color": BCS[0],   "label":"t#bar{t}Z          "    },

{"name":"STbt",   "selection": GW(), "file": files(loc + "SingleTbar_t"),  "cx":80.95,  "color": BCS[3],   "label":"SingleTop"    },
{"name":"STt",    "selection": GW(), "file": files(loc + "SingleTop_t"),   "cx":136.02, "color": BCS[3],   "label":"SingleTop"    },
{"name":"STbtW",  "selection": GW(), "file": files(loc + "SingleTbar_tW"), "cx":35.6,   "color": BCS[3],   "label":"SingleTop"      },
{"name":"STtW",   "selection": GW(), "file": files(loc + "SingleTop_tW"),  "cx":35.6,   "color": BCS[3],   "label":"SingleTop"      },
{"name":"WJets",  "selection": GW(), "file": files(loc + "WJets"),         "cx":61526.7,"color": BCS[1],   "label":"WJets      "       },
{"name":"WW",     "selection": GW(), "file": files(loc + "WW"),            "cx":110.8,  "color": BCS[2],   "label":"VV            "    },
{"name":"WZ",     "selection": GW(), "file": files(loc + "WZ"),            "cx":66.1,   "color": BCS[2],   "label":"VV            "   },
{"name":"ZZ",     "selection": GW(), "file": files(loc + "ZZ"),            "cx":15.4,   "color": BCS[2],   "label":"VV            "   },

{"name":"DYJets", "selection": GW(), "file": files(loc + "DYJets"),        "cx":6025.2, "color": BCS[1], "label":"DYJets    "      },
{"name":"DYJets10", "selection": GW(), "file": files(loc + "DYJets_10to50"),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },

#{"name":"DYRin", "selection": GW("(ll_zmass-91.2<=15)"), "file": files(loc + "DYJets"),        "cx":6025.2, "color": BCS[1], "label":"DYJets    "      },
#{"name":"DYRout", "selection": GW("(ll_zmass-91.2>15)"), "file": files(loc + "DYJets"),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },
#{"name":"DYRout", "selection": GW(), "file": files(loc + "DYJets_10to50"),"cx":18271.92, "color": BCS[1], "label":"DYJets    "      },


{"name":"ttH2non", "selection": GW(), "file": files(loc + "ttH_nonbb"),  "cx":0.5058,   "color": BCS[2],   "label":"t#bar{t}H         " ,"isStack":False   },
{"name":"ttH2bb",  "selection": GW(), "file": files(loc + "ttH_bb"),     "cx":0.5058,   "color": BCS[2],   "label":"t#bar{t}H         " ,"isStack":False   },
]

datasamples=[

{"name":"MuMu1", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015C"),  "color":kBlack,  "label":"DATA " },
{"name":"MuMu2", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015D"),  "color":kBlack,  "label":"DATA " },
{"name":"MuMu3", "selection": "(1)", "file": files(loc + "DoubleMuon_Run2015Dprompt"),  "color":kBlack,  "label":"DATA " },

{"name":"ElEl1", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015C"),    "color":kBlack,  "label":"DATA " },
{"name":"ElEl2", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015D"),    "color":kBlack,  "label":"DATA " },
{"name":"ElEl3", "selection": "(1)", "file": files(loc + "DoubleEG_Run2015Dprompt"),    "color":kBlack,  "label":"DATA " },

{"name":"MuEl1", "selection": "(1)", "file": files(loc + "MuonEG_Run2015C"),      "color":kBlack,  "label":"DATA " },
{"name":"MuEl2", "selection": "(1)", "file": files(loc + "MuonEG_Run2015D"),      "color":kBlack,  "label":"DATA " },
{"name":"MuEl3", "selection": "(1)", "file": files(loc + "MuonEG_Run2015Dprompt"),      "color":kBlack,  "label":"DATA " },

]
