#!/bin/bash
if [ $# != 1 ]; then
    echo "JOB SECTION NUMBER IS MISSING!!!"
    exit 1
fi
SECTION=`printf %d $1`

MYPWD=`pwd`
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc491
cd /cms/scratch/youngjo/CMSSW/CMSSW_7_4_16/src
eval `scramv1 runtime -sh`
cd $MYPWD

hostname
tar xzf job.tgz
cd plots

echo BEGIN `date` python ntuple2hist.py ${SECTION} -b 
python ntuple2hist.py ${SECTION} -b 
xrdcp hist_mon${SECTION}ee.root root://cms-xrdr.sdfarm.kr:1094///xrd//store/user/youngjo/Cattools/v7-6-1v1/resultv3/hist_mon${SECTION}ee.root
xrdcp hist_mon${SECTION}mm.root root://cms-xrdr.sdfarm.kr:1094///xrd//store/user/youngjo/Cattools/v7-6-1v1/resultv3/hist_mon${SECTION}mm.root
xrdcp hist_mon${SECTION}em.root root://cms-xrdr.sdfarm.kr:1094///xrd//store/user/youngjo/Cattools/v7-6-1v1/resultv3/hist_mon${SECTION}em.root

ls -al
time  ${SECTION}
EXITCODE=$?
ls -al
if [ $EXITCODE == 0 ]; then
   echo ENDED `date` python ntuple2hist.py ${SECTION} -b 
else
   rm -f core.*
   echo TERMINATED_$EXITCODE `date` python ntuple2hist.py ${SECTION} -b
   exit 1
fi

echo FINISHED `date` 
