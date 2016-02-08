#!/bin/bash

rm -rf jobR*
for i in {0..24}
do
   echo " $i times"
   mkdir jobR$i
   mkdir jobR$i/log
   head -n 18 run.sh > jobR$i/run.sh 
   echo sysweight=$i >> jobR$i/run.sh
   tail -n 10 run.sh >> jobR$i/run.sh
   chmod 755 jobR$i/run.sh
   #cp job.tgz jobR$i/
   cp submit.jds jobR$i/
   cp submit.sh jobR$i/
done

