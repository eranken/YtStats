import os

chan = 'all'
inDir = ''

sysfile1 = open(inDir+'combine_sys_2016all.txt')
sysfile2 = open(inDir+'combine_sys_2017all.txt')
sysfile3 = open(inDir+'combine_sys_2018all.txt')
syslist1 = sysfile1.read().split('\n')
syslist1 = filter(None, syslist1)
syslist2 = sysfile2.read().split('\n')
syslist2 = filter(None, syslist2)
syslist3 = sysfile3.read().split('\n')
syslist3 = filter(None, syslist3)
extrashit = ['EWunc','vj_norm','tt_norm','r','st_norm','vv_norm','lumi_corr','lumi_16','lumi_17','lumi18']

syslist=syslist1+syslist2+syslist3+extrashit

print syslist
print len(syslist)

syslist = list(dict.fromkeys(syslist))

print syslist
print len(syslist)

print ' '

for sys in syslist:
	print sys+','
