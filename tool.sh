#!/bin/sh
set -x
set -e


pushd /uscms_data/d1/eranken/CMSSW_7_4_7/src
mkdir CombineHarvester; cd CombineHarvester
git init
git remote add origin https://github.com/cms-analysis/CombineHarvester.git
git config core.sparsecheckout true; echo CombineTools/ >> .git/info/sparse-checkout
git pull origin master
popd
