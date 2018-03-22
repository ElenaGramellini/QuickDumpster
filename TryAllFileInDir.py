import os
import math
import copy
from ROOT import *
import math
from os import listdir
from os.path import isfile, join
from array import array



gStyle.SetOptStat(0)

dirName = "/lariat/data/users/elenag/tmp/ana/"
dirName = "/lariat/data/users/elenag/trackingOpt/optimizationData/"
onlyfiles = [f for f in listdir(dirName) if isfile(join(dirName, f)) and f.find(".root") != -1]
combo     = [x.replace('.root', '').replace('ana_', '') for x in onlyfiles]

if len(onlyfiles) != len(combo) :
    exit("Different list length, please look back at whatttadoing!")
nComboAvailable = len(onlyfiles)

print onlyfiles
print combo
print "Number of combinations available ", nComboAvailable

temp_List    = []
temp_List2   = []
temp_ListVtx = []
temp_ListEnd = []

skipFile = 0



for i in xrange(len(combo)) :
    print i, len(combo)
    f = onlyfiles[i]
    rootFileName = dirName+f
    statinfo = os.stat(rootFileName)
    print rootFileName, statinfo.st_size
    if ( statinfo.st_size < 5600000):
        skipFile += 1
        continue
    rootFile  = TFile( rootFileName )
    temp_Tree = rootFile.Get("TruthTeller/effTree") 
    temp_h  = TH1D("temp_h" ,"Reco Length - True Length C"+ combo[i]+"; Reco L - True L [cm]" ,400,-100,100)
    temp_h2 = TH1D("temp_h2","Reco Length - True Length C"+ combo[i]+"; Reco L - True L [cm]" ,400,-100,100)
    _hVtxDist          = TH1D("hVtxDist"          , "hVtxDist         ;  Vtx Dist [cm]" ,200,0,100)
    _hEndDist          = TH1D("hEndDist"          , "hEndDist         ;  End Dist [cm]" ,200,0,100)                                              
    
    temp_Tree.Draw("vtxDist>>hVtxDist"        , "recoL>0")
    temp_Tree.Draw("endDist>>hEndDist"        , "recoL>0")
    temp_Tree.Draw("(recoL-trueL)>>temp_h" , "recoL>0&&trueL>0.4")
    temp_Tree.Draw("(recoL-trueL)>>temp_h2", "recoL>0&&trueL>0.4&&(recoL-trueL)>-2.5&&(recoL-trueL)<2.5")
    temp_h.SetLineColor(4)
    temp_h.GetYaxis().SetRangeUser(0,1650)
    temp_h.SetLineWidth(2)
    temp_h2.SetLineColor(2)
    temp_h2.SetFillColor(2)
    temp_h2.SetLineWidth(2)
    
    
    temp_List .append(copy.copy(temp_h .Clone("h_" +combo[i] )))
    temp_List2.append(copy.copy(temp_h2.Clone("h2_"+combo[i] )))

    temp_ListVtx.append(copy.copy(_hVtxDist.Clone("_hVtxDist"+combo[i] )))
    temp_ListEnd.append(copy.copy(_hEndDist.Clone("_hEndDist"+combo[i] )))

print temp_List

f = TFile( 'FoM.root', 'recreate' )
t = TTree( 't1', 'tree with histos' )
comboCode      = array( 'i', [ 0 ] )
integral       = array( 'd', [ 0 ] )
integralR      = array( 'd', [ 0 ] )
integralL      = array( 'd', [ 0 ] )
integral2      = array( 'd', [ 0 ] )
integralRatio  = array( 'd', [ 0 ] )
mean           = array( 'd', [ 0 ] )
stdDev         = array( 'd', [ 0 ] )
vtxDistRatio   = array( 'd', [ 0 ] )
endDistRatio   = array( 'd', [ 0 ] )

t.Branch( 'comboCode'     ,comboCode     , 'comboCode/I'     )
t.Branch( 'integral'      ,integral      , 'integral/D'      )
t.Branch( 'integralR'     ,integralR     , 'integralR/D'     )
t.Branch( 'integralL'     ,integralL     , 'integralL/D'     )
t.Branch( 'integral2'     ,integral2     , 'integral2/D'     )
t.Branch( 'integralRatio' ,integralRatio , 'integralRatio/D')
t.Branch( 'mean'          ,mean          , 'mean/D'          )
t.Branch( 'stdDev'        ,stdDev        , 'stdDev/D'        )
t.Branch( 'vtxDistRatio'  ,vtxDistRatio  , 'vtxDistRatio/D'      )
t.Branch( 'endDistRatio'  ,endDistRatio  , 'endDistRatio/D'      )
    
cNTOF1 = TCanvas("s","s",600,600)

nComboAvailable = len(combo) - skipFile
cNTOF1.Divide(int(nComboAvailable/4.)+1, int(nComboAvailable/4.)+1)



for i in xrange(nComboAvailable):
    print comboCode[0], mean[0], i
    cNTOF1.cd(i+1)
    cNTOF1.Update()
    temp_List[i].Draw("")
    temp_List2[i].Draw("same")
    temp_List[i].Draw("same")
    cNTOF1.Update()
 
    comboCode      [0] = int(combo[i])
    integral       [0] = temp_List[i].Integral()
    integralR      [0] = temp_List[i].Integral(204,-1)
    integralL      [0] = temp_List[i].Integral(1,196)
    integral2      [0] = temp_List[i].Integral(196,204)
    integralRatio  [0] = 100*temp_List[i].Integral(196,204)/temp_List[i].Integral()
    mean           [0] = temp_List[i].GetMean()
    stdDev         [0] = temp_List[i].GetStdDev()
    

    endDistRatio   [0]  = 100*temp_ListEnd[i].Integral(0,2)/temp_List[i].Integral()
    vtxDistRatio   [0]  = 100*temp_ListVtx[i].Integral(0,2)/temp_List[i].Integral()

    print comboCode[0], mean[0]
    t.Fill()

 



zipped = zip(combo, temp_List, temp_ListEnd, temp_ListVtx )
zipped.sort()
combo, temp_List, temp_ListEnd, temp_ListVtx  = zip(*zipped)

#combo, temp_List = zip(*sorted(zip(combo, temp_List)))

cNTOF3 = TCanvas("cft3","ctf3",600,600)
cNTOF3.cd()
f.cd()
hMean      = TH1D("hMean","hMean; Configuration index; Delta L Mean",162,-0.5,161.5)
for i in xrange(len(combo)):
    print i+1, combo[i]
    hMean.SetBinContent(i+1, temp_List[i].GetMean())
hMean.Draw("")


cNTOF4 = TCanvas("cft4","ctf4",600,600)
cNTOF4.cd()
f.cd()
hStdDev      = TH1D("hStdDev","hStdDev; Configuration index; Delta L StdDev",162,-0.5,161.5)
for i in xrange(len(combo)):
    hStdDev.SetBinContent(i+1, temp_List[i].GetStdDev())
hStdDev.Draw("")


cNTOF5 = TCanvas("cft5","ctf5",600,600)
cNTOF5.cd()
f.cd()
hEndDist      = TH1D("hEndDist","hEndDist; Configuration index; EndDist Ratio",162,-0.5,161.5)
for i in xrange(len(combo)):
    hEndDist.SetBinContent(i+1, 100*temp_ListEnd[i].Integral(0,2)/temp_List[i].Integral())
hEndDist.Draw("")


cNTOF6 = TCanvas("cft6","ctf6",600,600)
cNTOF6.cd()
f.cd()
hVtxDist      = TH1D("hVtxDist","hVtxDist; Configuration index; VtxDist Ratio",162,-0.5,161.5)
for i in xrange(len(combo)):
    hVtxDist.SetBinContent(i+1, 100*temp_ListVtx[i].Integral(0,2)/temp_List[i].Integral())
hVtxDist.Draw("")

#f.Add(hMean)
#f.Add(hStdDev)
#f.Add(hVtxDist)
#f.Add(hEndDist)

f.Write()
f.Close()

raw_input()  



 

