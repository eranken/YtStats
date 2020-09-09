#!/usr/bin/env python2

import argparse,os
import sys
import subprocess
import numpy as np
import json

parser = argparse.ArgumentParser()
parser.add_argument('--o',action='store', type=str, default = "diffNuisances.root")
parser.add_argument('--M',action='store', type=str, default = "FitDiagnostics")
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--freeze',action='store', type=str, default = "r")
parser.add_argument('--set',action='store', type=str, default = "r=1")
parser.add_argument('--poi',action='store', type=str, default = "yt")
parser.add_argument('--opt',action='store', type=str, default = "--robustFit=1 --do95=1 --cminPreScan")

args = parser.parse_args()

cmssw = os.environ['CMSSW_BASE']
if "CMSSW_10_2_" not in cmssw:
	print 'ENV NOT LOADED'
	
commands = []
outputs = {}
#kwargs = []
#kwargs.append('combine')
#kwargs.append('-M ')

vals = np.arange(0.1,2.5,.1)

for val in vals:
	kwargs = '-M '+args.M+' -d card.root --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters r=1,yt='+str(val)+' -t '+args.t+' '+args.opt

	print 'running: combine '+kwargs
	#output=subprocess.call(['combine',kwargs])
	#output = subprocess.Popen( ['combine',kwargs], stdout=subprocess.PIPE  ).communicate()[0]
	output = os.popen('combine '+kwargs).readlines()
	outputs[val]=output

outcomes = {}
uncs = {}

for val in vals:
	outcomelist =[]
	for j in range(len(outputs[val])):
		print val,j,outputs[val][j]
		if outputs[val][j].startswith('Best fit'):
			outcome = outputs[val][j].split(' ')
			print 'OUTCOME',outcome
			for i in range(len(outcome)):
				if outcome[i].startswith('yt'):
					print 'ourcome2',outcome
					outval = float(outcome[i+1])
					uncstrings = outcome[i+3].split('/')
					print 'float:',uncstrings
					uncs = [float(thing.replace('+','')) for thing in uncstrings]
					uncdown = uncs[0]
					uncup = uncs[1]
					if outval+uncdown <0:
						uncdown = -1*outval
					outcomes[val]=[outval]+[uncdown,uncup]

		
print outcomes

with open('calibrate.json', 'w') as f:
	json.dump(outcomes, f)

#command2 = 'python ../../diffNuisances.py --poi '+args.poi+' -a fitDiagnostics.root -g '+args.o
#print 'running diffNuisances:',command2
#os.system(command2)
