from pybricks.hubs import PrimeHub
from pybricks.pupdevices import UltrasonicSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch

LOOP_MS = 50
SHOW_MS = 150
PRINT_MS = 500
NEAR_MM = 200      # قريب = خطر
MID_MM = 700       # متوسط

hub = PrimeHub()
front_sensor = UltrasonicSensor(Port.A)

dbg = StopWatch()
show = StopWatch()
reading = None

while True:
    try:
        d = front_sensor.distance()
        reading = d if d and d > 0 else None
    except Exception:
        reading = None

    if reading is not None:
        if reading < NEAR_MM:
            hub.light.on(Color.RED)
        elif reading < MID_MM:
            hub.light.on(Color.ORANGE)
        else:
            hub.light.on(Color.GREEN)
    else:
        hub.light.on(Color.BLUE)

    if show.time() >= SHOW_MS:
        hub.display.text(str(reading) if reading else "---")
        show.reset()

    if dbg.time() >= PRINT_MS:
        print("F=%s" % reading)
        dbg.reset()

    wait(LOOP_MS)
