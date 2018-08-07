import argparse,os
import sys
from subprocess import call

#comment

parser = argparse.ArgumentParser()
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--width',action='store', type=str, default = "2.5")
parser.add_argument('--freeze',action='store', type=str, default = "")
parser.add_argument('--pts',action='store', type=str, default = "500")
parser.add_argument('--set',action='store', type=str, default = "")
parser.add_argument('--poi',action='store', type=str, default = "")
parser.add_argument('--opt',action='store', type=str, default = "")
parser.add_argument('--P',action='store', type=str, default = "gt")
parser.add_argument('--gtpos',dest='gtpos', action='store_true')
parser.add_argument('--out',action='store', type=str, default = "2dscan.root")
parser.set_defaults(gtpos=False)

(args, opts) = parser.parse_known_args()
width = args.width

# default vals
gtmax = '10'
gtmin = '-10'

# overwrite defaults if scanning gt
if args.P == 'gt':
	gtmin = -width
	gtmax = width

# finally, overwrite minimum if constraining gt > 0 is desired
if args.gtpos:
	gtmin = '0'

mystr = 'combine -M MultiDimFit -d card.root --algo=grid --points='+args.pts
mystr += ' --redefineSignalPOIs '+args.P
if args.P !='gt':
	mystr+=',gt'
mystr += ' --freezeParameters r,'+args.freeze
mystr += ' --setParameters r=1,'+args.set
mystr += ' -t '+args.t
mystr += ' -P '+args.P
mystr += ' --setParameterRanges gt='+gtmin+','+gtmax
if args.P !='gt':
	mystr+=':'+args.P+'-'+width+','+width
mystr += ' --saveInactivePOI 1 --floatOtherPOIs=1'
for opt in opts:
	mystr += ' '+opt

print mystr
os.system(mystr)
print 'mv higgsCombineTest.MultiDimFit.mH120.root '+args.out
os.system('mv higgsCombineTest.MultiDimFit.mH120.root '+args.out)
