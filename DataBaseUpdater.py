import time

from OrderTrackerBackend import OrderTrackerBackend


def countdownTimer(minutes):
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print('Time is up!')


minutes = 15
while True:
    print("starting timer")
    countdownTimer(minutes)
    # run email scanner
    print("starting email check")
    try:
        OrderTrackerBackend().main()
    except:
        print("ERROR")

