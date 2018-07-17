import argparse,os
import sys
from subprocess import call

#comment

parser = argparse.ArgumentParser()
parser.add_argument('--o',action='store', type=str, default = "diffNuisances.root")
parser.add_argument('--M',action='store', type=str, default = "MaxLikelihoodFit")
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--freeze',action='store', type=str, default = "r")
parser.add_argument('--set',action='store', type=str, default = "r=1")
parser.add_argument('--poi',action='store', type=str, default = "gt")
parser.add_argument('--opt',action='store', type=str, default = "")

args = parser.parse_args()

os.system('cmsenv')

os.system('combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' --doInitialFit --robustFit 1 -t '+args.t)
os.system('combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' --doFits --robustFit 1 -t '+args.t)
os.system('combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' -o'+args.o+'.json')
os.system('plotImpacts.py -i '+args.o+'.json -o '+args.o)
os.system('gitup '+args.o+'.pdf')
