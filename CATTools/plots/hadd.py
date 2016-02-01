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

ll=files("/store/user/youngjo/Cattools/v7-6-1v1/resultv32")
lls=len(ll)
ll2 = {}
dd = 40
n = []
jj=0
for i,ii in enumerate(ll):
  n.append(ii)
  if i%dd ==39 or i is lls-1:
    ll2["h"+str(jj)]=n
    jj+=1
    n = []
  
for j in ll2.keys():
  aa = "hadd hmon_"+str(j)+".root "
  for i,k in enumerate(ll2[j]):
    aa+=" "+k
  os.system(aa)

print "lls : "+str(lls)+" : "+str(len(ll2.keys()))



