from ROOT import *
import os,commands
import subprocess

def files(path):
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
    return llll

ll=files("/store/user/youngjo/Cattools/v7-6-1v1/resultv3")
lls=len(ll)
ll2 = {}
for i in range(int(lls/20)):
  n = []
  for j,l in enumerate(ll):
    if (j%20) == i :
      n.append(l)
  ll2["h"+str(i)]=n
  
for j in ll2.keys():
  aa = "hadd hmon_"+str(j)+".root "
  for i,k in enumerate(ll2[j]):
    aa+=" "+k
  os.system(aa)

print "lls : "+str(lls)+" : "



