from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import UARTDevice
from huskylens import HuskyLens

STEER_CENTER = 0.067
STEER_MIN, STEER_MAX = -110, 110
STEER_SPEED = 250
STEER_CHANGE_THRESHOLD = 3
DRIVE_SPEED = 1000
STEER_DRIVE_SPEED = 600
TURN_DRIVE_SPEED = 600
BACKUP_SPEED = 500
TURN_TARGET_DEG = 84.935
HEAD_SIGN = -1

TURN_MM = 1000
COLOR_MM = 700
BOOST_MM = 300
BACKUP_MM = 200
TURN_ESCALATE_MM = 200

AVOID_STEER = 30
AVOID_BOOST_STEER = 60
TURN_STEER = 60
TURN_STEER_MAX = 90
RETURN_STEER = 25
RETURN_MS = 600
BACKUP_TIME_MS = 500

AVOID_MAX_MS = 2500
AVOID_MAX_DEV_DEG = 30
CAMERA_CLEAR_MS = 400
CAM_LOCKOUT_MS = 1500
TURN_TIMEOUT_MS = 3000

CAM_RIGHT_IDS = (1,)
CAM_LEFT_IDS = (2,)
CAM_MIN_CONF = 70
CAM_MIN_AREA = 150
CAM_MAX_WIDTH_PX = 90
CAM_X_MIN, CAM_X_MAX = 80, 240
CAM_POLL_MS = 150

TARGET_YAW = 90
YAW_KP = 2.0
YAW_MAX = 45
YAW_DEADBAND = 1.5

RECENTER_APPROACH = -20
LOOP_MS = 30
DEBUG = True

hub = PrimeHub()
steer_motor = Motor(Port.B)
steer_motor.reset_angle(0)
steer_motor.run_target(STEER_SPEED, STEER_CENTER, wait=True)
wait(1000)

drive_motor = Motor(Port.D)
front_sensor = UltrasonicSensor(Port.A)

cam = None
try:
    hl_uart = UARTDevice(Port.C, 9600)
    candidate = HuskyLens(hl_uart)
    if candidate.connected:
        candidate.mode_color_recognition()
        cam = candidate
        print("Camera ready")
except Exception as e:
    print("Camera init failed:", e)
if cam is None:
    hub.display.text("NoCam")

for _ in range(30):
    try:
        if hub.imu.ready():
            break
    except AttributeError:
        break
    wait(100)
hub.imu.reset_heading(TARGET_YAW)

last_cmd = None
_avoid_watch = StopWatch()
_clear_watch = StopWatch()


def ang_diff(a, b):
    return abs((a - b + 180) % 360 - 180)


def read_front():
    try:
        d = front_sensor.distance()
        return d if d and d > 0 else None
    except Exception:
        return None


def steer_to(angle, force=False):
    global last_cmd
    angle = max(STEER_MIN, min(STEER_MAX, angle))
    if not force and last_cmd is not None and abs(angle - last_cmd) < STEER_CHANGE_THRESHOLD:
        return
    steer_motor.run_target(STEER_SPEED, angle, wait=False)
    last_cmd = angle


def recenter():
    global last_cmd
    steer_motor.run_target(STEER_SPEED, RECENTER_APPROACH, wait=True)
    wait(150)
    for _ in range(3):
        steer_motor.run_target(STEER_SPEED, STEER_CENTER, wait=True)
        if abs(steer_motor.angle() - STEER_CENTER) <= 2:
            break
        wait(100)
    wait(100)
    last_cmd = STEER_CENTER


def hold_steer():
    err = (TARGET_YAW - hub.imu.heading()) * HEAD_SIGN
    if abs(err) <= YAW_DEADBAND:
        return STEER_CENTER
    c = YAW_KP * err
    return STEER_CENTER + max(-YAW_MAX, min(YAW_MAX, c))


def camera_dir():
    if cam is None:
        return 0
    try:
        blocks = cam.get_blocks()
    except Exception:
        return 0
    best_l = best_r = 0
    for b in blocks:
        if b.ID <= 0:
            continue
        if b.confidence and b.confidence < CAM_MIN_CONF:
            continue
        if not (CAM_X_MIN <= b.x <= CAM_X_MAX):
            continue
        if b.width > CAM_MAX_WIDTH_PX:
            if DEBUG:
                print("CAM reject-wide: ID%d w%d" % (b.ID, b.width))
            continue
        if b.width * b.height < CAM_MIN_AREA:
            continue
        if DEBUG:
            print("CAM accept: ID%d x%d w%d h%d" % (b.ID, b.x, b.width, b.height))
        if b.ID in CAM_LEFT_IDS and b.width * b.height > best_l:
            best_l = b.width * b.height
        elif b.ID in CAM_RIGHT_IDS and b.width * b.height > best_r:
            best_r = b.width * b.height
    if best_l and best_l >= best_r:
        return 1
    if best_r:
        return -1
    return 0


def do_backup():
    hub.light.on(Color.RED)
    print("BACKUP")
    drive_motor.stop()
    steer_to(STEER_CENTER, force=True)
    wait(150)
    drive_motor.run(-BACKUP_SPEED)
    wait(BACKUP_TIME_MS)
    drive_motor.stop()
    wait(80)


def turn_left_90():
    hub.light.on(Color.ORANGE)
    start = hub.imu.heading()
    steer_to(TURN_STEER, force=True)
    drive_motor.run(TURN_DRIVE_SPEED)
    watch = StopWatch()
    escalated = False
    while watch.time() < TURN_TIMEOUT_MS:
        if ang_diff(hub.imu.heading(), start) >= TURN_TARGET_DEG:
            break
        if not escalated:
            f = read_front()
            if f is not None and f < TURN_ESCALATE_MM:
                steer_to(TURN_STEER_MAX, force=True)
                escalated = True
        wait(10)
    drive_motor.stop()
    recenter()
    hub.imu.reset_heading(TARGET_YAW)


drive_motor.run(DRIVE_SPEED)
cam_timer = StopWatch()
lockout = StopWatch()
dbg = StopWatch()

cam_dir = 0
cam_locked = False
in_avoid = False
last_avoid_dir = 0
return_dir = 0
return_ms_left = 0
err_streak = 0

while True:
    try:
        front = read_front()

        cam_dir = 0
        if cam is not None:
            if cam_locked and lockout.time() >= CAM_LOCKOUT_MS:
                cam_locked = False
            if not cam_locked and cam_timer.time() >= CAM_POLL_MS:
                cam_dir = camera_dir()
                cam_timer.reset()

        mode = "HOLD"
        cmd = STEER_CENTER

        if front is not None and front < BACKUP_MM:
            mode = "BACKUP"
            do_backup()
            cam_locked = True
            lockout.reset()
            in_avoid = False
            return_ms_left = 0

        elif cam_dir != 0 and front is not None and front < COLOR_MM:
            if not in_avoid:
                in_avoid = True
                _avoid_watch.reset()
                _clear_watch.reset()
                print("AVOID start dir=%+d" % cam_dir)
            _clear_watch.reset()
            last_avoid_dir = cam_dir
            mode = "AVOID"
            cmd = (AVOID_BOOST_STEER if front < BOOST_MM else AVOID_STEER) * cam_dir
            steer_to(cmd)

            if _avoid_watch.time() > AVOID_MAX_MS or \
                    ang_diff(hub.imu.heading(), TARGET_YAW) > AVOID_MAX_DEV_DEG:
                in_avoid = False
                return_dir = -last_avoid_dir
                return_ms_left = RETURN_MS
                cam_locked = True
                lockout.reset()
                print("AVOID bounded -> return %+d" % return_dir)

        elif in_avoid:
            if _clear_watch.time() < CAMERA_CLEAR_MS:
                mode = "AVOID*"
                cmd = AVOID_STEER * last_avoid_dir
                steer_to(cmd)
            else:
                in_avoid = False
                return_dir = -last_avoid_dir
                return_ms_left = RETURN_MS
                cam_locked = True
                lockout.reset()
                print("Box passed -> return %+d" % return_dir)

        elif front is not None and front < TURN_MM:
            if cam_dir != 0:
                mode = "WAIT"
                cmd = hold_steer()
                steer_to(cmd)
            else:
                mode = "TURN"
                turn_left_90()
                cam_locked = True
                lockout.reset()
                in_avoid = False
                return_ms_left = 0

        else:
            if return_ms_left > 0:
                return_ms_left -= LOOP_MS
                mode = "RETURN"
                cmd = RETURN_STEER * return_dir
                steer_to(cmd)
            else:
                cmd = hold_steer()
                steer_to(cmd)
                hub.light.on(Color.GREEN)

        if mode == "BACKUP":
            pass
        elif mode == "WAIT":
            drive_motor.run(STEER_DRIVE_SPEED)
        elif abs(cmd - STEER_CENTER) > 8:
            drive_motor.run(STEER_DRIVE_SPEED)
        else:
            drive_motor.run(DRIVE_SPEED)

        err_streak = 0

        if DEBUG and dbg.time() >= 250:
            print("F=%s H=%.1f S=%.1f CAM=%+d %s ret=%d"
                  % (front, hub.imu.heading(), steer_motor.angle(),
                     cam_dir, mode, return_ms_left))
            dbg.reset()

    except Exception as e:
        err_streak += 1
        drive_motor.stop()
        hub.light.on(Color.RED)
        hub.display.text("ERR")
        print("LOOP ERROR %d: %s: %s" % (err_streak, type(e).__name__, e))
        if err_streak >= 5:
            raise SystemExit("stopping")
        wait(1500)

    wait(LOOP_MS)
