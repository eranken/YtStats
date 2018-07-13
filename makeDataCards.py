from Framework.Core import *
import argparse,os

#test comment
#testagain

process = [
		"vj",
		"ttbg",
		"ttsig",
		"st",
		]

systematics = [
		lnNSystematic("btag"	,["ttsig"]	,[1.03]),
		lnNSystematic("ltag"	,["ttsig"]	,[1.0014]),
		lnNSystematic("lumi"	,["ttsig","ttbg","vj","st"]	,[1.023,1.023,1.023,1.023]),
		#ShapeSystematic("btag"	,["ttsig"]),
		#ShapeSystematic("ltag"	,["ttsig"]),
		#ShapeSystematic("fsr"	,["ttsig"]),
		#ShapeSystematic("isr"	,["ttsig"]),
		#ShapeSystematic("fs"	,["ttsig"]),
		#ShapeSystematic("rs"	,["ttsig"]),
		#ShapeSystematic("JER"	,["ttsig"]),
		#ShapeSystematic("JES"	,["ttsig"]),
		#ShapeSystematic("isr"	,["ttsig"]),
		#ShapeSystematic("fsr"	,["ttsig"]),
		#ShapeSystematic("hd"	,["ttsig"]),
		#ShapeSystematic("tune"	,["ttsig"]),
		]

parser = argparse.ArgumentParser()
parser.add_argument('--inDir',action='store')
parser.add_argument('--outDir',action='store')

option = parser.parse_args()

rootFileReader = RootFileReader()
rootFileReader.readFile(option.inDir+'combine.root')
binCollection = rootFileReader.createBinCollection(process,systematics)

textFilePath = option.inDir+'qua.txt'
textFileReader = TextFileReader()
textFileReader.readTextFile(textFilePath,binCollection)

if not os.path.exists(option.outDir):
	os.makedirs(option.outDir)

for ibin,anaBin in binCollection.iteritems():
	dataCard = DataCard(anaBin)
	dataCard.makeCard(option.outDir)
	dataCard.makeRootFile(option.outDir)

rootFileReader.cleanUp()
