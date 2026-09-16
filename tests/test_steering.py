from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Button
from pybricks.tools import wait, StopWatch

STEER_CENTER = 0.067
STEER_MIN, STEER_MAX = -110, 110
STEER_SPEED = 250
STEP = 10          # deg per press
LOOP_MS = 30
SHOW_MS = 150

hub = PrimeHub()
steer_motor = Motor(Port.B)
steer_motor.reset_angle(0)
steer_motor.run_target(STEER_SPEED, STEER_CENTER, wait=True)
wait(500)

target = STEER_CENTER
last_cmd = None
dbg = StopWatch()
show = StopWatch()


def steer_to(angle):
    global last_cmd
    angle = max(STEER_MIN, min(STEER_MAX, angle))
    if last_cmd is not None and abs(angle - last_cmd) < 1:
        return
    steer_motor.run_target(STEER_SPEED, angle, wait=False)
    last_cmd = angle


while True:
    pressed = hub.button.pressed()

    if Button.RIGHT in pressed:
        target += STEP
        steer_to(target)
        while Button.RIGHT in hub.button.pressed():
            wait(20)

    if Button.LEFT in pressed:
        target -= STEP
        steer_to(target)
        while Button.LEFT in hub.button.pressed():
            wait(20)

    if Button.CENTER in pressed:
        target = STEER_CENTER
        steer_to(target, )
        steer_motor.run_target(STEER_SPEED, STEER_CENTER, wait=True)
        while Button.CENTER in hub.button.pressed():
            wait(20)

    if show.time() >= SHOW_MS:
        hub.display.text(str(round(steer_motor.angle(), 1)))
        if dbg.time() >= 500:
            print("target=%.1f actual=%.1f" % (target, steer_motor.angle()))
            dbg.reset()
        show.reset()

    wait(LOOP_MS)
