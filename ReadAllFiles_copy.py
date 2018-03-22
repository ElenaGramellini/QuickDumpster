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

dirName = "/Volumes/BROCKU/Elena/"
onlyfiles = [f for f in listdir(dirName) if isfile(join(dirName, f)) and f.find(".root") != -1]
for i in xrange(len(onlyfiles)) :
    f = onlyfiles[i]
    rootFileName = dirName+f
    puppa1 = readOneFileFunction(rootFileName)
    print puppa1


raw_input()  
