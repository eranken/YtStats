from Framework.Core import *
import argparse,os


parser = argparse.ArgumentParser()
parser.add_argument('--input',action='store')
parser.add_argument('--year', action='store', type=str, default='2017')
parser.add_argument('--chan', action='store', type=str, default='all')

option = parser.parse_args()

inDir = 'Input/'+option.input+'/'
outDir = 'Output/'+option.input+'/'
print outDir
print inDir

year = option.year
chan = option.chan
sysfile = open(inDir+'combine_sys_'+year+chan+'.txt')
syslist = sysfile.read().split('\n')
syslist = filter(None, syslist) #
print syslist
shortyear = year[2:]
lumicorr = .0137
lumiunc = .0209
if shortyear == '17':
	lumiunc *- .23/.25
	lumiunc *= .23/.25
lumicorr+=1.
lumiunc+=1.

lumiunc=1.001

process = [
		"vj",
		"ttsig",
		"st",
		]

#if int(year) >= 2017:
#	process.append("ttbg")	

systematics = [
		#lnNSystematic("flat"	,["ttsig"]	,[1.03]),
		#lnNSystematic("hd"	,["ttsig"]	,[1.0152]),
		#lnNSystematic("tune"	,["ttsig"]	,[1.0074]),
		#lnNSystematic("lumi_corr"	,["ttsig","vj","st"]	,[lumicorr,lumicorr,lumicorr]),
		lnNSystematic("lumi_"+shortyear	,["ttsig","vj","st"]	,[lumiunc,lumiunc,lumiunc]),
		#lnNSystematic("vj_norm"	,["vj"]	,[1.15]),
		#lnNSystematic("tt_norm"	,["ttsig"]	,[1.1,1.1]),
		#lnNSystematic("st_norm"	,["st"]	,[1.15])
		#lnNSystematic("ltag"	,["ttsig"]	,[1.0015]),
		#lnNSystematic("isr"	,["ttsig"]	,[1.00145],),
		#ShapeSystematic("flat_shape"	,["ttsig"]),
		# ShapeSystematic("ltag"	,["ttsig"]),
		# ShapeSystematic("btag"	,["ttsig"]),
		# ShapeSystematic("fsr"	,["ttsig"]),
		# ShapeSystematic("isr"	,["ttsig"]),
		# ShapeSystematic("fs"	,["ttsig"]),
		# ShapeSystematic("rs"	,["ttsig"]),
		# ShapeSystematic("JER"	,["ttsig"]),
		# ShapeSystematic("JES"	,["ttsig"]),
		# ShapeSystematic("hd"	,["ttsig"]),
		# ShapeSystematic("tune"	,["ttsig"]),
		# ShapeSystematic("pu"	,["ttsig"]),
		# ShapeSystematic("mtop"	,["ttsig"]),
		# ShapeSystematic("bfrag"	,["ttsig"]),
		# ShapeSystematic("bdec"	,["ttsig"]),
		# ShapeSystematic("elrec"	,["ttsig"]),
		# ShapeSystematic("eltrg"	,["ttsig"]),
		# ShapeSystematic("murec"	,["ttsig"]),
		# ShapeSystematic("mutrg"	,["ttsig"]),
		# ShapeSystematic("pdf0"	,["ttsig"]),
		# ShapeSystematic("pdf1"	,["ttsig"]),
		# ShapeSystematic("pdf2"	,["ttsig"]),
		# ShapeSystematic("pdf3"	,["ttsig"]),
		# ShapeSystematic("pdf4"	,["ttsig"]),
		# ShapeSystematic("pdf5"	,["ttsig"]),
		# ShapeSystematic("pdf6"	,["ttsig"]),
		# ShapeSystematic("alphas"	,["ttsig"]),
		]



for sys in syslist:
	print sys
	#systematics.append(ShapeSystematic(sys,["ttsig"]))

rootFileReader = RootFileReader()
rootFileReader.readFile(inDir+'combine_'+year+chan+'.root')
binCollection = rootFileReader.createBinCollection(process,systematics)

textFilePath = inDir+'combine_EW_'+year+chan+'.txt'
# textFilePath = option.inDir+'qua.txt'
textFileReader = TextFileReader()
textFileReader.readTextFile(textFilePath,binCollection)

if not os.path.exists(outDir):
	os.makedirs(outDir)

for ibin,anaBin in binCollection.iteritems():
	dataCard = DataCard(anaBin)
	dataCard.makeCard(outDir,year,chan)
	dataCard.makeRootFile(outDir,year,chan)

rootFileReader.cleanUp()
