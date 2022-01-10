rm ./data/stocks/*.csv
echo '---------------------- CLEAR STAT ----------------------'
python3 study/emptyJson.py
echo '---------------------- SYMBOLS ----------------------'
python3 symbols.py
echo '---------------------- SNAPSHOT ----------------------'
python3 alpacaSnapshot.py
echo '---------------------- DOWNLOAD HISTORICAL ----------------------'
python3 alpacaHistorical.py
echo '---------------------- FILTER ATR ----------------------'
python3 study/filterATR.py
echo '---------------------- FILTER EMA ----------------------'
python3 study/filterEma.py
echo '---------------------- FILTER KEYLEVEL ----------------------'
python3 study/filterKeylevels.py
echo '---------------------- FILTER FIBONACHI ----------------------'
python3 study/filterFibonachiRetracement.py
echo '---------------------- FILTER THREEBARS ----------------------'
python3 study/filterThreeBars.py
echo '---------------------- FILTER RELATIVE VOLUME ----------------------'
python3 study/filterRelativeVolume.py
echo '---------------------- FILTER VOLUME PROFILE ----------------------'
python3 study/filterVolumeProfile.py
echo '---------------------- DONE ----------------------'
echo 'LOOK AT THE data/symbols.json FILE FOR THE RESULTS'
echo 'filter based on study/findstocks.py'
echo '{filteratr": true, "atr": 20.52, "close": 567.06, "avgatr": 24.66, "trendup": false, "trenddown": false, "keylevel": false, "fibonachi": true, "threebars": false}'
echo ''

export FLASK_APP=app; flask run
