echo '---------------------- STARTING ----------------------'
cd /home/young/Desktop/code/trading/candlestick-pattern-analyzer

if [ $1 == '--daily' ]; then
    echo '---------------------- CLEAR STAT ----------------------'
    rm ./data/stocks/*.csv
    cp ./data/symbols-empty.json ./data/symbols.json
fi

echo '---------------------- START APP ----------------------'
echo $1
python3 app/app.py $1
echo '----------------------  END APP  ----------------------'
