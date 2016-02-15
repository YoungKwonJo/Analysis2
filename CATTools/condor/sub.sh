#!/bin/bash

loc=`pwd`
ii=$1
echo " $ii times"
cd $loc/jobR$ii
./submit.sh
cd $loc
