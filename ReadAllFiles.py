'''
import os
import math
import copy
from ROOT import *
import math
from os import listdir
from os.path import isfile, join
from array import array
'''
from os import listdir
from os.path import isfile, join


from FunctionReadOneFile import readOneFileFunction

f = TFile( 'FoM.root', 'recreate' )
t = TTree( 't1', 'tree with histos' )
comboName                           = array( 'i', [ 0 ] )
matchingEfficiency                  = array( 'd', [ 0 ] )
rigthMatchingEfficiency             = array( 'd', [ 0 ] )
percentageOfCorrectlyMatchedTracks  = array( 'd', [ 0 ] )
percentageOfWronglyMatchedTracks    = array( 'd', [ 0 ] )
percentageRightVtx                  = array( 'd', [ 0 ] )
percentageRightEnd                  = array( 'd', [ 0 ] )
percentageRightDeltaL               = array( 'd', [ 0 ] )
percentageLongDeltaL                = array( 'd', [ 0 ] )
percentageShortDeltaL               = array( 'd', [ 0 ] )
funnyBusinness                      = array( 'd', [ 0 ] )

t.Branch( 'comboName'                          , comboName                           , 'comboName'                            )
t.Branch( 'matchingEfficiency'                 , matchingEfficiency                  , 'matchingEfficiency'                   )
t.Branch( 'rigthMatchingEfficiency'            , rigthMatchingEfficiency             , 'rigthMatchingEfficiency'              )
t.Branch( 'percentageOfCorrectlyMatchedTracks' , percentageOfCorrectlyMatchedTracks  , 'percentageOfCorrectlyMatchedTracks'   )
t.Branch( 'percentageOfWronglyMatchedTracks'   , percentageOfWronglyMatchedTracks    , 'percentageOfWronglyMatchedTracks'     )
t.Branch( 'percentageRightVtx'                 , percentageRightVtx                  , 'percentageRightVtx'                   )
t.Branch( 'percentageRightEnd'                 , percentageRightEnd                  , 'percentageRightEnd'                   )
t.Branch( 'percentageRightDeltaL'              , percentageRightDeltaL               , 'percentageRightDeltaL'                )
t.Branch( 'percentageLongDeltaL'               , percentageLongDeltaL                , 'percentageLongDeltaL'                 )
t.Branch( 'percentageShortDeltaL'              , percentageShortDeltaL               , 'percentageShortDeltaL'                )
t.Branch( 'funnyBusinness'                     , funnyBusinness                      , 'funnyBusinness'                       )


dirName = "/Volumes/BROCKU/Elena/"
onlyfiles = [f for f in listdir(dirName) if isfile(join(dirName, f)) and f.find(".root") != -1]


_comboName                           = TH1F("__comboName"                        ,"_comboName                         ;BinCount ;comboName                         ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_matchingEfficiency                  = TH1F("_matchingEfficiency"                ,"_matchingEfficiency                ;comboCode;matchingEfficiency                ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_rigthMatchingEfficiency             = TH1F("_rigthMatchingEfficiency"           ,"_rigthMatchingEfficiency           ;comboCode;rigthMatchingEfficiency           ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageOfCorrectlyMatchedTracks  = TH1F("_percentageOfCorrectlyMatchedTracks","_percentageOfCorrectlyMatchedTracks;comboCode;percentageOfCorrectlyMatchedTracks",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageOfWronglyMatchedTracks    = TH1F("_percentageOfWronglyMatchedTracks"  ,"_percentageOfWronglyMatchedTracks  ;comboCode;percentageOfWronglyMatchedTracks  ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageRightVtx                  = TH1F("_percentageRightVtx"                ,"_percentageRightVtx                ;comboCode;percentageRightVtx                ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageRightEnd                  = TH1F("_percentageRightEnd"                ,"_percentageRightEnd                ;comboCode;percentageRightEnd                ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageRightDeltaL               = TH1F("_percentageRightDeltaL"             ,"_percentageRightDeltaL             ;comboCode;percentageRightDeltaL             ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageLongDeltaL                = TH1F("_percentageLongDeltaL"              ,"_percentageLongDeltaL              ;comboCode;percentageLongDeltaL              ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 
_percentageShortDeltaL               = TH1F("_percentageShortDeltaL"             ,"_percentageShortDeltaL             ;comboCode;percentageShortDeltaL             ",len(onlyfiles)+2, -0.5,len(onlyfiles)-0.5) 


for i in xrange(len(onlyfiles)) :
    f = onlyfiles[i]
    rootFileName = dirName+f
    tupla = readOneFileFunction(rootFileName)
    
    comboName[0]                           = tupla[0]
    matchingEfficiency[0]                  = tupla[1] 
    rigthMatchingEfficiency[0]             = tupla[2] 
    percentageOfCorrectlyMatchedTracks[0]  = tupla[3] 
    percentageOfWronglyMatchedTracks[0]    = tupla[4]
    percentageRightVtx[0]                  = tupla[5] 
    percentageRightEnd[0]                  = tupla[6]
    percentageRightDeltaL[0]               = tupla[7] 
    percentageLongDeltaL[0]                = tupla[8] 
    percentageShortDeltaL[0]               = tupla[9]
    funnyBusinness[0]                      = tupla[10]

    if !funnyBusinness[0]:
        t.Fill()
        _comboName                           .SetBinContent(i,comboName[0]                            )
        _matchingEfficiency                  .SetBinContent(i,matchingEfficiency[0]                   )
        _rigthMatchingEfficiency             .SetBinContent(i,rigthMatchingEfficiency[0]              )
        _percentageOfCorrectlyMatchedTracks  .SetBinContent(i,percentageOfCorrectlyMatchedTracks[0]   )
        _percentageOfWronglyMatchedTracks    .SetBinContent(i,percentageOfWronglyMatchedTracks[0]     )
        _percentageRightVtx                  .SetBinContent(i,percentageRightVtx[0]                   )
        _percentageRightEnd                  .SetBinContent(i,percentageRightEnd[0]                   )
        _percentageRightDeltaL               .SetBinContent(i,percentageRightDeltaL[0]                )
        _percentageLongDeltaL                .SetBinContent(i,percentageLongDeltaL[0]                 )
        _percentageShortDeltaL               .SetBinContent(i,percentageShortDeltaL[0]                )




maxRightEndBin    = _percentageRightEnd   .GetMaximumBin()
maxRightDeltaLBin = _percentageRightDeltaL.GetMaximumBin()

maxRightEnd    = _percentageRightEnd   .GetMaximum()
maxRightDeltaL = _percentageRightDeltaL.GetMaximum()

if maxRightEnd != _percentageRightEnd.GetBinContent(maxRightEndBin):
    print "WRONG END"

if maxRightDeltaL != _percentageRightDeltaL.GetMaximum.GetBinContent(maxRightDeltaLBin):
    print "WRONG DeltaL"


maxComboCode_maxEnd               = _comboName               .GetBinContent(maxRightEndBin) 
rigthVtx_maxEnd                   = _percentageRightVtx      .GetBinContent(maxRightEndBin) 
rightDeltaL_maxEnd                = _percentageRightDeltaL   .GetBinContent(maxRightEndBin) 
rigthMatchingEfficiency_maxEnd    = _rigthMatchingEfficiency .GetBinContent(maxRightEndBin) 

maxComboCode_maxDeltaL            = _comboName               .GetBinContent(maxRightDeltaLBin) 
rigthVtx_maxDeltaL                = _percentageRightVtx      .GetBinContent(maxRightDeltaLBin) 
rightEnd_maxDeltaL                = __percentageRightEnd     .GetBinContent(maxRightDeltaLBin) 
rigthMatchingEfficiency_maxDeltaL = _rigthMatchingEfficiency .GetBinContent(maxRightDeltaLBin) 


print "Maximum percentage of Right End: ", maxRigthEnd    , "for combo code "   , maxComboCode_maxEnd 
print "Corresponding Values: Right Vtx: ", rigthVtx_maxEnd, "%,  Right DeltaL: ", rightDeltaL_maxEnd, "%, ", rigthMatchingEfficiency_maxEnd

print "Maximum percentage of Right DeltaL: ", maxRigthDeltaL    , "for combo code "   , maxComboCode_maxEnd
print "Corresponding Values: Right Vtx: "   , rigthVtx_maxDeltaL, "%,  Right DeltaL: ", rightEnd_maxDeltaL, "%, ", rigthMatchingEfficiency_maxDeltaL

f.Write()
f.Close()
          

raw_input()  
