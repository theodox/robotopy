from motors import forward, turn_right, halt
from rangefinder import get_range
import time


rf = get_range()
rf.next()
result = 100
for n in range(100):
    nextv = rf.send(result < 20)
    if nextv:
       result = nextv
    time.sleep(0.1)
    print "range:", result
#    rf.send(result > 50)

print "DONE"

#forward(.125)
#time.sleep(1)
#halt()
#time.sleep(.5)
#turn_right()
#time.sleep(1)
#forward(.5)
#time.sleep(1)
