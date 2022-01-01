rm ./data/stocks/*.csv
echo '---------------------- SYMBOLS ----------------------'
python3 symbols.py
echo '---------------------- SNAPSHOT ----------------------'
python3 alpacaSanpshot.py
echo '---------------------- DOWNLOAD HISTORICAL ----------------------'
python3 alpacaHistorical.py
echo '---------------------- FILTER KEYLEVEL ----------------------'
python3 study/filterKeyLevels.py
echo '---------------------- FILTER RETRACEMENT ----------------------'
python3 studyfilterRetracement.py
echo '---------------------- DONE ----------------------'
echo 'LOOK AT THE data/symbols.csv FILE FOR THE RESULTS'
echo ''
