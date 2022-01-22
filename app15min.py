import time

# parameter parsing
print('starting.  please stand by.  It might take a minute or two to start')
obj_now = datetime.now()
secWait = 60 - obj_now.second
time.sleep(secWait)

SetInterval(900, lambda: MinInterval(symbol, period))
