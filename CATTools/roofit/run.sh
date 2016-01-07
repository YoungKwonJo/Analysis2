python roofitCSV.py 0 0 0 -b  > log.txt 
python roofitCSV.py 1 0 0 -b  >> log.txt
python roofitCSV.py 2 0 0 -b  >> log.txt 
python roofitCSV.py 3 0 0 -b  >> log.txt 
python roofitCSV.py 0 1 0 -b  >> log.txt
python roofitCSV.py 1 1 0 -b  >> log.txt
python roofitCSV.py 2 1 0 -b  >> log.txt
python roofitCSV.py 3 1 0 -b  >> log.txt
python roofitCSV.py 0 2 0 -b  >> log.txt
python roofitCSV.py 1 2 0 -b  >> log.txt
python roofitCSV.py 2 2 0 -b  >> log.txt
python roofitCSV.py 3 2 0 -b  >> log.txt
cat log.txt | grep FINAL > log2.txt
