import os
import math
import copy
from ROOT import *
import math
from os import listdir
from os.path import isfile, join
from array import array


fileName = "FoM.root"
fileKaonRoot    = TFile(fileName )
gStyle.SetOptFit(1111)

cPida = TCanvas("cPida","cPida",600,600)
cPida.cd()


hKaonPIDA1   = fileKaonRoot.Get("hMean" )
hKaonPIDA2   = fileKaonRoot.Get("hStdDev" )
hKaonPIDA3   = fileKaonRoot.Get("hEndDist" )
hKaonPIDA4   = fileKaonRoot.Get("hVtxDist" )

hKaonPIDA1.SetLineColor(2);
hKaonPIDA2.SetLineColor(4);
hKaonPIDA3.SetLineColor(7);
hKaonPIDA4.SetLineColor(6);


hKaonPIDA1.SetLineWidth(2);
hKaonPIDA2.SetLineWidth(2);
hKaonPIDA3.SetLineWidth(2);
hKaonPIDA4.SetLineWidth(2);


hKaonPIDA1.GetYaxis().SetRangeUser(-10,10);
hKaonPIDA2.GetYaxis().SetRangeUser(0,30);
hKaonPIDA3.GetYaxis().SetRangeUser(35,50);
hKaonPIDA4.GetYaxis().SetRangeUser(89,100);

hKaonPIDA1.Draw("")
legend = TLegend(.44,.52,.74,.75)
legend.AddEntry(hKaonPIDA1,"Delta L Mean")
#legend.Draw("same")


cPida0 = TCanvas("cPida0","cPida0",600,600)
cPida0.cd()
hKaonPIDA2.Draw("same")
legend1 = TLegend(.44,.52,.74,.75)
legend1.AddEntry(hKaonPIDA2,"Delta L StdDev")
#legend1.Draw("same")


cPida2 = TCanvas("cPida2","cPida2",600,600)
cPida2.cd()
hKaonPIDA3.Draw("")
legend2 = TLegend(.44,.52,.74,.75)
legend2.AddEntry(hKaonPIDA3,"End Distance Ratio")
#legend2.Draw("same")

cPida3 = TCanvas("cPida3","cPida",600,600)
cPida3.cd()
hKaonPIDA4.Draw("")
legend1 = TLegend(.44,.52,.74,.75)
legend1.AddEntry(hKaonPIDA4,"Vtx Distance Ratio")
#legend1.Draw("same")









raw_input()  



 

