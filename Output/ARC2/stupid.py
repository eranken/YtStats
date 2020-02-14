import ROOT as r
from ROOT import *
import sys

blue=r.kAzure+4
green=r.kTeal+4
orange=r.kOrange+4
purple=r.kViolet-5
gray=r.kGray+2
black=r.kBlack
red=r.kRed+1

plots =[]

testplot = TH1D('hi','hi',10,0,10.)

for i in range(1,11):
	testplot.SetBinContent(i,1.)

print testplot.Integral(2,3)
