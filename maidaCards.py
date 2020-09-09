from Framework.Core import *
import argparse,os


parser = argparse.ArgumentParser()
parser.add_argument('--input',action='store')
parser.add_argument('--year', action='store', type=str, default='2017')

option = parser.parse_args()

inDir = 'Input/'+option.input+'/'
outDir = 'Output/'+option.input+'/'
print outDir
print inDir

year = option.year
chan = option.chan
sysfile = open(inDir+'combine_sys_'+year+'.txt')
syslist = sysfile.read().split('\n')
syslist = filter(None, syslist) #
print syslist
shortyear = year[2:]
if shortyear == '17':
	lumiunc =0.023
else:
	lumiunc = 0.025
lumiunc+=1.


process = [
		"vj",
		"ttsig",
		"st",
		]

systematics = [
		lnNSystematic("lumi_corr"	,["ttsig","vj","st"]	,[lumicorr,lumicorr,lumicorr]),
		lnNSystematic("lumi_"+shortyear	,["ttsig","vj","st"]	,[lumiunc,lumiunc,lumiunc]),
		lnNSystematic("vj_norm"	,["vj"]	,[1.15]),
		lnNSystematic("tt_norm"	,["ttsig","ttbg"]	,[1.1,1.1]),
		lnNSystematic("st_norm"	,["st"]	,[1.15])
		]

for sys in syslist:
	print sys
	systematics.append(ShapeSystematic(sys,["ttsig"]))

rootFileReader = RootFileReader()
rootFileReader.readFile(inDir+'combine_'+year+'.root')
binCollection = rootFileReader.createBinCollection(process,systematics)

textFilePath = inDir+'combine_EW_'+year+'.txt'
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
