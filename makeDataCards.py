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

syslist=['JES_AbsoluteScale','JES_FlavorQCD','flatsys','JES_PileupPtBB','mtop','JES_RelativeFSR','JES_RelativePtEC2','elrec','JES_RelativePtEC1','rs','eltrg','JES_AbsoluteMPFBias','mutrg','murec','JER','JES_Fragmentation','fs','bfrag','JES_SinglePionHCAL','bdec','JES_RelativePtBB','JES_RelativeSample','JES_RelativeBal','pdf2','pdf3','pdf0','pdf1','pdf7','pdf4','pdf5','alphas','JES_SinglePionECAL','btag','isr','pu','JES_PileupPtRef','JES_RelativeJEREC1','ltag','fsr','JES_PileupPtEC1','JES_PileupDataMC','JES_TimePtEta',]

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
