rm ./data/stocks/*.csv
echo '---------------------- CLEAR STAT ----------------------'
cp ./data/symbols-empty.json ./data/symbols.json
echo '---------------------- SYMBOLS ----------------------'
python3 symbols.py
echo '---------------------- SNAPSHOT ----------------------'
python3 alpacaSnapshot.py
echo '---------------------- DOWNLOAD HISTORICAL ----------------------'
python3 alpacaHistorical.py
echo '---------------------- CLEAN UP STOCK DATA ----------------------'
python3 study/filterRemoveNoDataStocks.py
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
echo '---------------------- FILTER OVERNIGHT GAPPER ----------------------'
python3 filterOvernightGap.py
echo '---------------------- DONE ----------------------'

read -p "Press [Enter] key to start pushing symbol data..."
echo ''
python3 toServer.py
echo '---------------------- LAUNCHING FLASK ----------------------'
echo ''

# export FLASK_APP=app; flask run

