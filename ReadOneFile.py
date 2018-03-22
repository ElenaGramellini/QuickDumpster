import os
import math
import copy
from ROOT import *
import math
from os import listdir
from os.path import isfile, join
from array import array


gStyle.SetOptStat(1111)

# Plotting variables
deltaL         = "recoL - trueL"     
vtx            = "vtxDist"   
end            = "endDist" 
isPrimaryInTPC = "isPrimaryInTPC"
isTrackMatched = "isTrackMatched"


# Temporary Histograms
_hDeltaL    = TH1D("hDeltaL"   , "Reco Length - True Length ; Reco L - True L [cm]" ,400,-100,100)
_hDeltaLXC  = TH1D("hDeltaLXC" , "Reco Length - True Length ; Reco L - True L [cm]" ,400,-100,100)
_hVtxDist   = TH1D("hVtxDist"  , "hVtxDist         ; Vtx Dist [cm]"     ,200,0,100)
_hEndDist   = TH1D("hEndDist"  , "hEndDist         ; End Dist [cm]"     ,200,0,100)                                              
_hPrimary   = TH1D("hPrimary"  , "Primary In TPC   ; is Primary in TPC" ,2,-0.5,1.5)                                              
_hMatched   = TH1D("hMatched"  , "Matched Particle ; is Primary Matched",2,-0.5,1.5)                                              
_hMatchedR  = TH1D("hMatchedR" , "Right Matched Particle ; is Primary Matched",2,-0.5,1.5)                                              
_hMatchedW  = TH1D("hMatchedW" , "Wrong Matched Particle ; is Primary Matched",2,-0.5,1.5)                                              


# Temporary File names
rootFileName = "/Volumes/BROCKU/Elena/OptTrack11110.root"
rootFile  = TFile( rootFileName )
temp_Tree = rootFile.Get("TruthTeller/effTree")

c0 = TCanvas("s0","s0",600,600)
c0.cd()
temp_Tree.Draw(deltaL        +">>hDeltaL(400,-100,100)" , "recoL>0 && isTrackMatched&&isPrimaryInTPC")
c1 = TCanvas("s1","s1",600,600)
c1.cd()
temp_Tree.Draw(vtx           +">>hVtxDist(200,0,100)"   , "recoL>0 && isTrackMatched&&isPrimaryInTPC")
c2 = TCanvas("s2","s2",600,600)
c2.cd()
temp_Tree.Draw(end           +">>hEndDist(200,0,100)"   , "recoL>0 && isTrackMatched&&isPrimaryInTPC")
c3 = TCanvas("s3","s3",600,600)
c3.cd()
temp_Tree.Draw(isPrimaryInTPC+">>hPrimary(2,-0.5,1.5)"        , "")
c4 = TCanvas("s4","s4",600,600)
c4.cd()
temp_Tree.Draw(isTrackMatched+">>hMatched(2,-0.5,1.5)"        , "")
c5 = TCanvas("s5","s5",600,600)
c5.cd()
temp_Tree.Draw(isTrackMatched+">>hMatchedR(2,-0.5,1.5)"        , "( isPrimaryInTPC) && isTrackMatched") # If the track is matched and the primary was in TPC, good!
c6 = TCanvas("s6","s6",600,600)
c6.cd()
temp_Tree.Draw(isTrackMatched+">>hMatchedW(2,-0.5,1.5)"        , "(!isPrimaryInTPC) && isTrackMatched") # If the track is matched and the primary was NOT in TPC, BAD!



NPrimaryInTPC      = float(hPrimary.GetBinContent(2))
RightMatchedTracks = float(hMatchedR.GetBinContent(2))
WrongMatchedTracks = float(hMatchedW.GetBinContent(2))
TotalMatchedTracks = float(hMatched.GetBinContent(2))
percentageOfCorrectlyMatchedTracks =  100*RightMatchedTracks/TotalMatchedTracks
percentageOfWronglyMatchedTracks   =  100*WrongMatchedTracks/TotalMatchedTracks
matchingEfficiency                 =  100*TotalMatchedTracks/NPrimaryInTPC
rigthMatchingEfficiency            =  100*RightMatchedTracks/NPrimaryInTPC
print "Match Eff", matchingEfficiency, "Right Eff: ",rigthMatchingEfficiency, " Purity ", percentageOfCorrectlyMatchedTracks , " Impurity ", percentageOfWronglyMatchedTracks

rightDeltaL     = 0.
shortRecoDeltaL = 0.
longRecoDeltaL  = 0.

maxBin    = hDeltaL.GetMaximumBin()
maxXValue = hDeltaL.GetXaxis().GetBinCenter(maxBin)
print maxBin, maxXValue

for iBin in xrange(1,hDeltaL.GetSize()-1):
    if iBin > maxBin+4:
        longRecoDeltaL+= float(hDeltaL.GetBinContent(iBin))
    elif iBin < maxBin-4:
        shortRecoDeltaL+= float(hDeltaL.GetBinContent(iBin))
    else:
        rightDeltaL += float(hDeltaL.GetBinContent(iBin))
        _hDeltaLXC.SetBinContent(iBin, hDeltaL.GetBinContent(iBin))
#print longRecoDeltaL, shortRecoDeltaL, rightDeltaL, longRecoDeltaL+shortRecoDeltaL+rightDeltaL 

c0.cd()
_hDeltaLXC.SetLineColor(kRed)
_hDeltaLXC.Draw("same")
rightVtx    = float(hVtxDist.GetBinContent(1) + hVtxDist.GetBinContent(2) + hVtxDist.GetBinContent(3) + hVtxDist.GetBinContent(4))
rightEnd    = float(hEndDist.GetBinContent(1) + hEndDist.GetBinContent(2) + hEndDist.GetBinContent(3) + hEndDist.GetBinContent(4))
percentageRightVtx    = 100.*rightVtx/RightMatchedTracks
percentageRightEnd    = 100.*rightEnd/RightMatchedTracks
percentageRightDeltaL = 100.*rightDeltaL/RightMatchedTracks
percentageLongDeltaL  = 100.*longRecoDeltaL/RightMatchedTracks
percentageShortDeltaL = 100.*shortRecoDeltaL/RightMatchedTracks
print "Right Vtx: ", percentageRightVtx, " Right End: " , percentageRightEnd, " Right DeltaL: " , percentageRightDeltaL, " Long DeltaL: " , percentageLongDeltaL, " Short DeltaL: " , percentageShortDeltaL

############################### Sanity checks ##########################
funnyBusinness = 0
sumBins = 0
for iBin in xrange(1,hDeltaL.GetSize()-1):
    sumBins += hDeltaL.GetBinContent(iBin)
overFlow  = hDeltaL.GetBinContent(hDeltaL.GetSize())
underFlow = hDeltaL.GetBinContent(0)
#print sumBins,  overFlow, underFlow, sumBins+overFlow+underFlow, hDeltaL.GetEntries()
funnyBusinness += (sumBins+overFlow+underFlow - hDeltaL.GetEntries())

sumBins = 0
for iBin in xrange(1,hVtxDist.GetSize()-1):
    sumBins += hVtxDist.GetBinContent(iBin)
overFlow  = hVtxDist.GetBinContent(hVtxDist.GetSize())
underFlow = hVtxDist.GetBinContent(0)
#print sumBins,  overFlow, underFlow, sumBins+overFlow+underFlow, hVtxDist.GetEntries()
funnyBusinness += (sumBins+overFlow+underFlow - hVtxDist.GetEntries())

sumBins = 0
for iBin in xrange(1,hEndDist.GetSize()-1):
    sumBins += hEndDist.GetBinContent(iBin)
overFlow  = hEndDist.GetBinContent(hEndDist.GetSize())
underFlow = hEndDist.GetBinContent(0)
#print sumBins,  overFlow, underFlow, sumBins+overFlow+underFlow, hEndDist.GetEntries()
funnyBusinness += (sumBins+overFlow+underFlow - hEndDist.GetEntries())

# Let's check the entries in each plotting metrics are the number of correctly matched tracks
funnyBusinness += ( hMatchedR.GetBinContent(2) - hDeltaL.GetEntries() ) 
funnyBusinness += ( hMatchedR.GetBinContent(2) - hVtxDist.GetEntries()) 
funnyBusinness += ( hMatchedR.GetBinContent(2) - hEndDist.GetEntries()) 
# Let's check that the total number of right and wrong tracks is equal to the sum 
funnyBusinness += (  RightMatchedTracks + WrongMatchedTracks - TotalMatchedTracks) 
#print "Sanity Check:"
#print "The number of matched events, ", hMatchedR.GetBinContent(2), 
#print "Needs to be equal to entries in delta and edges plots: ", hDeltaL.GetEntries(), hVtxDist.GetEntries(), hEndDist.GetEntries()
#print "Sanity Check: sum of wrong and right needs to be total", RightMatchedTracks + WrongMatchedTracks, TotalMatchedTracks 
#print "Matching Efficiency ", RightMatchedTracks/NPrimaryInTPC, " Matching Purity ", percentageOfCorrectlyMatchedTracks
#print "Number of wrong matches ", WrongMatchedTracks

comboName =0
print  comboName
print  matchingEfficiency , rigthMatchingEfficiency, percentageOfCorrectlyMatchedTracks , percentageOfWronglyMatchedTracks,
print  percentageRightVtx , percentageRightEnd     , 
print  percentageRightDeltaL, percentageLongDeltaL, percentageShortDeltaL
print  funnyBusinness


raw_input()  
