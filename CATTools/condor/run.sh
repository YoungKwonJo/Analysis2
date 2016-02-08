#!/bin/bash
if [ $# != 1 ]; then
    echo "JOB SECTION NUMBER IS MISSING!!!"
    exit 1
fi
SECTION=`printf %d $1`

MYPWD=`pwd`
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc491
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_16
eval `scramv1 runtime -sh`
cd $MYPWD

hostname
tar xzf job.tgz
cd plots



sysweight=0






echo BEGIN `date` python ntuple2hist.py ${SECTION} ${sysweight} -b
outputpath=root://cms-xrdr.sdfarm.kr:1094///xrd//store/user/youngjo/Cattools/v7-6-1v3/hist20160208 
python ntuple2hist.py ${SECTION} ${sysweight} -b 
xrdcp hist_mon${SECTION}ee.root $outputpath/hist_${sysweight}/hist_mon${SECTION}ee.root
xrdcp hist_mon${SECTION}mm.root $outputpath/hist_${sysweight}/hist_mon${SECTION}mm.root
xrdcp hist_mon${SECTION}em.root $outputpath/hist_${sysweight}/hist_mon${SECTION}em.root

ls -al
echo FINISHED `date` 
