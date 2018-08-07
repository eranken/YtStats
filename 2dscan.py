import argparse,os
import sys
from subprocess import call

#comment

parser = argparse.ArgumentParser()
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--width',action='store', type=str, default = "2.5")
parser.add_argument('--freeze',action='store', type=str, default = "")
parser.add_argument('--pts',action='store', type=str, default = "2500")
parser.add_argument('--set',action='store', type=str, default = "")
parser.add_argument('--poi',action='store', type=str, default = "")
parser.add_argument('--opt',action='store', type=str, default = "")
parser.add_argument('--P',action='store', type=str, default = "gt")

(args, opts) = parser.parse_known_args()
width = args.width

params = args.P.split(',')
for param in params:
	print param

mystr = 'combine -M MultiDimFit -d card.root --algo=grid --points='+args.pts
mystr += ' --redefineSignalPOIs '
for param in params:
	mystr += param+','
mystr += ' --freezeParameters r,'+args.freeze
mystr += ' --setParameters r=1,'+args.set
mystr += ' -t '+args.t
for param in params:
	mystr += ' -P '+param
mystr += ' --setParameterRanges '
for param in params:
	if param =='gt':
		mystr+='gt=0,'+width+':'
	else: mystr+= param+'=-'+width+','+width+':'
mystr += ' --saveInactivePOI 1 --floatOtherPOIs=1'
for opt in opts:
	mystr += ' '+opt

os.system(mystr)
