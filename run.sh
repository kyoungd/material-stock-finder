echo '---------------------- STARTING ----------------------'
cd /home/young/Desktop/code/trading/candlestick-pattern-analyzer

if [ $1 == '--daily' ]; then
    echo '---------------------- CLEAR STAT ----------------------'
    rm ./data/stocks/*.csv
    rm ./data/bak/*.csv
    rm ./data/bak/*.json
    cp ./data/symbols-empty.json ./data/symbols.json
fi

if [ $1 == '--run' ]; then
    echo '---------------------- CLEAR STAT ----------------------'
    rm ./data/stocks/*.csv
    rm ./data/bak/*.csv
    rm ./data/bak/*.json
    cp ./data/symbols-empty.json ./data/symbols.json
fi

echo '---------------------- START APP ----------------------'
echo $1
python3 app/app.py $1
echo '----------------------  END APP  ----------------------'
cp ./data/symbols.* ./data/bak/
echo '----------------------  ENDING  ----------------------'

