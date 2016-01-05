from ROOT import *

f=TFile("MuonSF_IDISO_POG25ns.root")
h=f.Get("GlobalSF")

for i in range(1, h.GetXaxis().GetNbins()+1 ):
  for j in range(1, h.GetYaxis().GetNbins()+1 ):
    print "else if(pt > "+str(h.GetYaxis().GetBinLowEdge(j))+" && pt <="+str(h.GetYaxis().GetBinUpEdge(j))+" && eta >"+str(h.GetXaxis().GetBinLowEdge(i))+" && eta <="+str(h.GetXaxis().GetBinUpEdge(i))+") "+" return (float) "+str(h.GetBinContent(i,j))+"; "
