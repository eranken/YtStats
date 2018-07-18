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
os.system('combine -M '+args.M+' -d card.root --redefineSignalPOIs '+args.poi+' --freezeNuisances '+args.freeze+' --setPhysicsModelParameters '+args.set+' -t '+args.t+' '+args.opt)
os.system('python ../../diffNuisances.py --poi '+args.poi+' -a mlfit.root -g '+args.o)
