cd /home/young/Desktop/code/trading/candlestick-pattern-analyzer
echo '---------------------- FILTER LastnightGapper ----------------------'
python3 study/filterLastnightGapper.py
echo '---------------------- SENDING DATA ----------------------'

# read -p "Press [Enter] key to start pushing symbol data..."
echo ''
python3 toServer.py
echo '---------------------- COMPLETE ----------------------'
echo ''
