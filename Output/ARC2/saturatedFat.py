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

filedir = sys.argv[1]

def LLplot(filename):
	gROOT.cd()

	treefile = TFile.Open(filename,'READ')
	tree = treefile.Get('limit')

	leaves = tree.GetListOfLeaves()

	for i in range(0,leaves.GetEntries() ) :
		leaf = leaves.At(i)
		print 'LEAF:',leaves.GetName()

	nEntries = tree.GetEntries()
	print 'NUMBER OF ENTRIES:',nEntries

	gROOT.cd()
	theplot = TH1D(filename+'_teststat_distribution','some_name',400,0.,100.)
	theplot.SetDirectory(gROOT)

	for i in range(0,nEntries):
		tree.GetEntry(i)
		statval = tree.GetLeaf('limit').GetValue()
		theplot.Fill(statval,1.)

	print "PLOTTTTT:", theplot.GetName(),theplot.Integral()

	return theplot

def Datastat(filename):
	gROOT.cd()

	DATAtreefile = TFile.Open(filename,'READ')
	DATAtree = DATAtreefile.Get('limit')

	nEntries = DATAtree.GetEntries()
	print 'NUMBER OF ENTRIES:',nEntries

	DATAtree.GetEntry(0)
	testStatistic = DATAtree.GetLeaf('limit').GetValue()

	return testStatistic

testplot = LLplot(filedir+'/GOF.root')
datastat = Datastat(filedir+'/gofdata.root')
databin=testplot.FindFixBin(datastat)
Nbins=testplot.GetNbinsX()

pval = float(testplot.Integral(databin,Nbins+1))/float(Nbins)
print 'THE P VAL is', pval

c1 = TCanvas()
testplot.Draw()
