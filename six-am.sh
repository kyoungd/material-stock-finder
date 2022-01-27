echo '---------------------- FILTER LastnightGapper ----------------------'
python3 study/filterLastnightGapper.py
echo '---------------------- DONE ----------------------'

# read -p "Press [Enter] key to start pushing symbol data..."
echo ''
python3 toServer.py
echo '---------------------- LAUNCHING FLASK ----------------------'
echo ''
