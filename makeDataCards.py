from Framework.Core import *
import argparse,os


parser = argparse.ArgumentParser()
parser.add_argument('--inDir',action='store')
parser.add_argument('--outDir',action='store')
parser.add_argument('--year', action='store', type=str, default='17')
parser.add_argument('--chan', action='store', type=str, default='all')

option = parser.parse_args()

inDir = option.inDir
year = option.year
chan = option.chan
sysfile = open(inDir+'combine_sys_'+year+chan+'.txt')
syslist = sysfile.read().split('\n')
syslist = filter(None, syslist) #
print syslist

process = [
		"vj",
		"ttbg",
		"ttsig",
		"st",
		]

systematics = [
		#lnNSystematic("flat"	,["ttsig"]	,[1.03]),
		#lnNSystematic("hd"	,["ttsig"]	,[1.0152]),
		#lnNSystematic("tune"	,["ttsig"]	,[1.0074]),
		lnNSystematic("lumi"	,["ttsig","ttbg","vj","st"]	,[1.023,1.023,1.023,1.023])
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
	systematics.append(ShapeSystematic(sys,["ttsig"]))

rootFileReader = RootFileReader()
rootFileReader.readFile(option.inDir+'combine_'+year+chan+'.root')
binCollection = rootFileReader.createBinCollection(process,systematics)

textFilePath = option.inDir+'combine_EW_'+year+chan+'.txt'
# textFilePath = option.inDir+'qua.txt'
textFileReader = TextFileReader()
textFileReader.readTextFile(textFilePath,binCollection)

if not os.path.exists(option.outDir):
	os.makedirs(option.outDir)

for ibin,anaBin in binCollection.iteritems():
	dataCard = DataCard(anaBin)
	dataCard.makeCard(option.outDir)
	dataCard.makeRootFile(option.outDir)

rootFileReader.cleanUp()
