from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port, Direction, Stop
from pybricks.tools import wait, StopWatch
from math import atan2, degrees, sin, tan, radians

# =====================================================
#  الإعدادات
# =====================================================
DEBUG = True           # يطبع الحالة كل نصف ثانية
TURN_DIR = -1          # -1 = عكس عقارب الساعة (يسار) | +1 = مع عقارب الساعة
LAPS = 3
GEAR_RATIO = 3         # تروس الموتر الخلفي 1 : 3 (العجلة تلف 3 لفات لكل لفة موتر)
WHEEL_CIRC_MM = 175.9 * GEAR_RATIO   # المسافة المقطوعة لكل لفة موتر = محيط العجلة (176 مم) × 3
SPEED_CM_S = 20        # السرعة المطلوبة بالسم/ث (ارفعها 3-5 فقط في كل مرة بعد ما يثبت)
DRIVE_SPEED = SPEED_CM_S * 10 / WHEEL_CIRC_MM * 360   # deg/s للموتر D (تُحسب تلقائياً)

STEER_LEFT = 87        # زاوية الموتر B لأقصى يسار
STEER_RIGHT = -72      # زاوية الموتر B لأقصى يمين

# --- تحكم الاتجاه (الجايرو) ---
KP_HEAD = 0.03
KD_HEAD = 0.004
CENTER_STEER_LIMIT = 0.5   # أقصى توجيه وقت المشي العادي
PILLAR_STEER_LIMIT = 1   # أقصى توجيه وقت تفادي مكعب
MAX_OFFSET = 26            # أقصى انحراف عن المرجع بسبب المكعب (درجة)
MAX_OFFSET_CLOSE = 38      # لو المكعب قريب (أقل من 60 سم) نسمح بانحراف أكبر

# --- الزوايا ---
CORNER_DIST_MM = 830
EMERGENCY_MM = 250
MIN_TURN_GAP_MS = 1500
FINISH_MM = 400

# --- المكعبات (5x5 سم، ارتفاع 10 سم) ---
MIN_BLOCK_H = 8
PILLAR_H_CM = 10
FOCAL_PX = 295
CAM_CX = 150               # من معايرة 70 و100 سم
REACT_DIST_CM = 110
CLEAR_CM = 18
CAM_GAIN = 1.6             # قوة الانحراف عن المكعب (تعديل ميداني: الأخضر المواجه كان يُصدم؛ كان 1.2 ثم 1.0)
LANE_LAT_MAX_CM = 30       # مكعب أبعد جانبياً من هذا = ليس في ممرنا (نتجاهله)
Y_LIMIT_CM = 40           # أقصى بعد جانبي عن وسط الممر (رفعناه من 25 حتى لا يخنق الانحراف عن المكعب؛ الساحة 3م والحساسات الجانبية تحرس)
SAME_PILLAR_MM = 250       # قراءة ضمن هذا الفرق من موقع المكعب المتتبَّع = نفس المكعب
MIN_UPDATE_DEPTH_CM = 40   # أقرب من هذا لا نحدّث الانحراف (الكاميرا غير دقيقة عند الحافة)
REAR_CLEAR_MM = 100        # مسافة بعد موقع المكعب قبل اعتباره متجاوزًا (طلب ميداني: 100 بدل 300، الروبوت موازٍ أصلًا بعد بلوغ الموقع)
GREEN_ID, RED_ID = 1, 2

# --- الأصفر: إشارة إسكات الحساس الأمامي فقط (طلب ميداني: شفنا الأصفر = الحساس الأمامي يسكت وبس) ---
YELLOW_ID = 3               # هوية الأصفر عند الكاميرا
YELLOW_MIN_H = 8            # أقل ارتفاع بالبكسل نعتبره أصفر حقيقي (لو الأصفر عندك صغير أو بعيد: نزّل الرقم)
FRONT_MUTE_MM = 9999        # المسافة الوهمية وقت الإسكات (تشوفها في شاشة التنقيح: F 9999)

# --- العودة لوسط الممر بالحساب (بدون حساسات جانبية) ---
USE_ODOM_CENTER = True
KY = 0.25                  # درجة لكل سم انحراف عن الوسط
MAX_CENTER_OFFSET = 8      # أقصى تصحيح (درجة)

# --- توقف وفحص (Stop & Look) ---
# G1 = True  => أخضر => نمر من اليسار
# G1 = False => أحمر => نمر من اليمين
SCAN_STEP_MM = 1200        # الفحص الواقف صار احتياطيًا نادرًا (كان 400): الكشف الأساسي صار أثناء الحركة
SCAN_SETTLE_MS = 150       # ننتظر حتى تهدأ السيارة قبل القراءة
SCAN_FRAMES = 3            # عدد القراءات الواقفة (نأخذ اللون الأكثر تكراراً)
NOW_DEPTH_CM = 105         # مدى الكشف أثناء الحركة (كان 90): مكعب داخل هذا المدى يُصوَّت عليه بلا توقف
DRIVE_VOTES = 2            # إطارات جديدة بنفس اللون قبل التصرف أثناء الحركة (1 = إطار واحد مثل القديم)
EMERGENCY_DEPTH_CM = 55    # مكعب أقرب من هذا أثناء الحركة: نتصرف من إطار واحد بلا تصويت

# --- تفادي أقوى (تعديل ميداني: الأخضر المواجه كان يُصدم) ---
PILLAR_KP_HEAD = 0.06      # جين الجايرو أثناء تتبع مكعب (ضعف KP_HEAD): الميل يُبنى أسرع
PILLAR_KD_HEAD = 0.008     # مقابل KD_HEAD بنفس النسبة
PILLAR_SPEED_FRAC = 0.7    # السرعة أثناء تتبع مكعب: نمهل التوجيه يبني الميل قبل بلوغ المكعب
DEAD_AHEAD_CM = 12         # مكعب على محورنا مباشرة: إطار واحد يكفي للتفعيل (المسافة لا تسمح بالتصويت)

# =====================================================
#  مكعب الزاوية القادمة: يظهر في طرف الكاميرا (الثلث الأيسر لو اللفة يسار) قبل اللفة
#   أحمر => نمر من يمينه: طلب ميداني ثالث بعد ارتطام الجدار: أقصى توجيه وأبدر لفة،
#           كان التوقيت 950 مم والخروج نحو 730 مم من الجدار الخارجي
#   طلب ميداني رابع (هذي النسخة): تصغير المسافة اللي يلف منها لما يشوف أحمر عند الزوايا:
#           التوقيت صار 750 مم والخروج نحو 530 مم (اللفة نفسها على أقصى توجيه من الطلب الثالث)
#   أخضر => نصغّر اللفة (أقصى توجيه) ونلف بدري  (نمر من يساره = قرب الجدار الداخلي)
# =====================================================
IMG_W = 320
CORNER_ZONE_PX = IMG_W / 3        # عرض الثلث الخارجي من الصورة
CORNER_CUBE_MAX_CM = 220          # أبعد مسافة نعتمد فيها قراءة مكعب الزاوية
CORNER_VOTES = 2                  # عدد الإطارات المتفقة على اللون قبل اعتماده
WHEELBASE_MM = 185                # المسافة بين مركزي العجلتين
MAX_STEER_DEG = 40                # أقصى زاوية التفاف
STEER_FRAC_NONE = 1.0             # بدون مكعب (نفس سلوك الكود الحالي)
STEER_FRAC_TIGHT = 1.0            # أقصى توجيه = أصغر لفة (أخضر لو اللفة يسار)
STEER_FRAC_RELAXED = 1.0          # الأحمر: طلب ميداني ثالث "شدّد اللفة" بعد ارتطام الجدار (المسار: 0.75 ثم 0.9 ثم أقصى توجيه؛ نصف القطر 220.5 مم مثل الأخضر ويبقى التفريق بالتوقيت وجهة الخروج)
EXIT_OUT_NONE = 500               # بُعد الخروج من الزاوية عن الجدار الخارجي (مم): الوسط
EXIT_OUT_INNER = 700              # أخضر: نخرج بعيد عن الخارجي (قرب الداخلي) لنمر من يسار المكعب
EXIT_OUT_OUTER = 600              # أحمر: طلب ميداني رابع: نصغّر مسافة بدء اللفة (المسار: 300 ثم 500 ثم 650 ثم 450): التوقيت 750 مم والخروج نحو 530 مم من الجدار | للرجوع للقديم: 650
WIDE_MEMORY_MM = 1200             # بعد عائق أحمر والمكعب التالي محجوب: نعتبره أحمر

# --- كسر اللفة (Sharper turn) بالـ YAW ---
SHARP_DEPTH_CM = 45        # مكعب على جهة اللفة أقرب من هذا أثناء اللفة => نكسر اللفة
SHARP_EXTRA_DEG = 15       # نزيد هدف الـ YAW بهذا المقدار
SHARP_HOLD_MM = 200        # نحافظ على الانحراف هذه المسافة (لو السبب جدار)
TURN_WALL_MM = 120         # جدار أمامي أقرب من هذا أثناء اللفة => نكسر اللفة

# --- الألتراسونيك قرأ شيء قريب: الكاميرا تتأكد (مكعب أم جدار؟) قبل ما ندور ---
WALL_CONFIRM = 1           # قراءتان متتاليتان للألتراسونيك قبل ما نسأل الكاميرا
CONFIRM_FRAMES = 2         # عدد الإطارات الجديدة من الكاميرا للتأكد
FRONT_LAT_CM = 20          # مكعب بهذا العرض عن محور السيارة = ممكن يكون ما قرأه الألتراسونيك
FRONT_TOL_MM = 250         # فرق مسموح بين بُعد المكعب (كاميرا) وقراءة الألتراسونيك
CHECK_GAP_MS = 400         # أقل فاصل بين فحصين متتاليين

# --- أمان الجدران بالحساسين الجانبيين (حماية فقط، ليس للتمركز) ---
USE_SIDE_SAFETY = True
SAFE_SIDE_MM = 110         # أقل مسافة آمنة جانبياً
SAFE_GAIN = 0.15           # درجة ميل لكل مم اقتراب
SAFE_MAX_DEG = 12

# =====================================================
#  الأجهزة
# =====================================================
hub = PrimeHub()
steer = Motor(Port.B)
drive = Motor(Port.D, Direction.COUNTERCLOCKWISE)   # معكوس بسبب التروس (احذف Direction لو يمشي عكس)
ultra = UltrasonicSensor(Port.A)      # أمامي
ultra_r = UltrasonicSensor(Port.F)    # يمين
ultra_l = UltrasonicSensor(Port.E)    # يسار
uart = UARTDevice(Port.C, 9600, timeout=50)

REQ_BLOCKS = bytes([0x55, 0xAA, 0x11, 0x00, 0x21, 0x31])


def set_steer(s):
    s = max(-1, min(1, s))
    if s >= 0:
        steer.track_target(s * STEER_LEFT)
    else:
        steer.track_target(-s * STEER_RIGHT)


def parse_blocks(data):
    blocks = []
    i = 0
    n = len(data)
    while i + 6 <= n:
        if data[i] == 0x55 and data[i + 1] == 0xAA and data[i + 2] == 0x11:
            length = data[i + 3]
            cmd = data[i + 4]
            p = i + 5
            if p + length + 1 > n:
                break
            if cmd == 0x2A and length == 10:
                x = data[p] | (data[p + 1] << 8)
                y = data[p + 2] | (data[p + 3] << 8)
                w = data[p + 4] | (data[p + 5] << 8)
                h = data[p + 6] | (data[p + 7] << 8)
                bid = data[p + 8] | (data[p + 9] << 8)
                blocks.append((x, y, w, h, bid))
            i = p + length + 1
        else:
            i += 1
    return blocks


# قراءة الكاميرا بدون انتظار
rx = b""
waiting = False
req_timer = StopWatch()
last_blocks = []
frame_no = 0                   # يزيد مع كل إطار جديد من الكاميرا


def husky_poll():
    global rx, waiting, last_blocks, frame_no
    if not waiting:
        uart.clear()
        rx = b""
        uart.write(REQ_BLOCKS)
        waiting = True
        req_timer.reset()
        return last_blocks
    data = uart.read_all()
    if data:
        rx += data
    if len(rx) >= 16 and rx[4] == 0x29:
        n = rx[5] | (rx[6] << 8)
        if len(rx) >= 16 + 16 * n:
            last_blocks = parse_blocks(rx)
            frame_no += 1
            waiting = False
    if waiting and req_timer.time() > 250:
        waiting = False
    return last_blocks


def husky_reset():
    global rx, waiting, last_blocks
    rx = b""
    waiting = False
    last_blocks = []
    uart.clear()


def closest_block(blocks):
    best = None
    for b in blocks:
        if b[4] in (GREEN_ID, RED_ID) and b[3] >= MIN_BLOCK_H:
            if best is None or b[3] > best[3]:
                best = b
    return best


def classify(blocks, d, y):
    """يرجع (مكعب ممرنا, لون مكعب الزاوية القادمة)
       مكعب ممرنا = (G1, عمق سم, جانبي سم) أو None | لون الزاوية: True أخضر / False أحمر / None"""
    lane = None
    lane_h = 0
    corner = None
    corner_h = 0
    for b in blocks:
        if b[4] not in (GREEN_ID, RED_ID) or b[3] < MIN_BLOCK_H:
            continue
        g1 = b[4] == GREEN_ID
        depth_cm = FOCAL_PX * PILLAR_H_CM / b[3]            # البعد من الكاميرا
        lat_cm = (b[0] - CAM_CX) * depth_cm / FOCAL_PX      # موجب = يمين محور السيارة
        out_of_lane = abs(lat_cm + y) > LANE_LAT_MAX_CM     # موقعه المطلق خارج ممرنا
        if (not out_of_lane) and depth_cm <= REACT_DIST_CM and depth_cm * 10 <= d + 150:
            if b[3] > lane_h:                               # الأقرب (الأكبر) في ممرنا
                lane_h = b[3]
                lane = (g1, depth_cm, lat_cm)
        elif out_of_lane and depth_cm <= CORNER_CUBE_MAX_CM:
            if TURN_DIR < 0:
                in_zone = b[0] < CORNER_ZONE_PX             # الثلث الأيسر
            else:
                in_zone = b[0] > IMG_W - CORNER_ZONE_PX     # الثلث الأيمن
            if in_zone and b[3] > corner_h:
                corner_h = b[3]
                corner = g1
    return lane, corner


def yellow_seen(blocks):
    """هل ظهر الأصفر (ID 3) في آخر إطار؟ أي ظهور يكفي: مهمته إسكات الحساس الأمامي فقط، لا يوجد أي تفاعل آخر معه"""
    for b in blocks:
        if b[4] == YELLOW_ID and b[3] >= YELLOW_MIN_H:
            return True
    return False


def turn_plan(g1):
    """يرجع (نسبة التوجيه, مسافة بدء اللفة من الجدار الأمامي) حسب لون مكعب الزاوية القادمة.
       الخروج = المسافة بعد اللفة عن الجدار الأمامي القديم: يتغير مع بدء اللفة ومع نصف قطرها."""
    if g1 is None:
        frac, exit_out = STEER_FRAC_NONE, EXIT_OUT_NONE
    elif (g1 and TURN_DIR < 0) or ((not g1) and TURN_DIR > 0):
        frac, exit_out = STEER_FRAC_TIGHT, EXIT_OUT_INNER       # نمر من جهة الداخل: لفة أصغر وبدري
    else:
        frac, exit_out = STEER_FRAC_RELAXED, EXIT_OUT_OUTER     # نمر من جهة الخارج: لفة أكبر ومتأخر
    radius = WHEELBASE_MM / tan(radians(MAX_STEER_DEG * frac))
    radius0 = WHEELBASE_MM / tan(radians(MAX_STEER_DEG * STEER_FRAC_NONE))
    trigger = CORNER_DIST_MM + (exit_out - EXIT_OUT_NONE) + (radius - radius0)
    return frac, max(EMERGENCY_MM + 100, trigger)


def plan_offset(g1, depth_cm, lat_cm, y):
    """انحراف الـ YAW المطلوب: أخضر (True) نمر يساره | أحمر (False) نمر يمينه"""
    target_lat = CLEAR_CM if g1 else -CLEAR_CM
    err_cm = target_lat - lat_cm
    err_cm = max(y - Y_LIMIT_CM, min(y + Y_LIMIT_CM, err_cm))
    off = -CAM_GAIN * degrees(atan2(err_cm, max(depth_cm, 30)))
    limit = MAX_OFFSET_CLOSE if depth_cm < 60 else MAX_OFFSET
    return max(-limit, min(limit, off))


def husky_read_blocking(max_ms=400, fresh=True):
    """قراءة كاملة من الكاميرا. fresh=False يكمل على إطار ناقص بدل رميه (لسقف زمني أقصر أثناء الحركة)"""
    if fresh:
        husky_reset()
    husky_poll()
    t = StopWatch()
    while t.time() < max_ms:
        wait(10)
        blocks = husky_poll()
        if not waiting:
            return blocks
    return []


def scan_pillar(d, y):
    """نتوقف ونقرأ عدة مرات. يرجع ((G1, عمق, جانبي) أو None, لون مكعب الزاوية أو None)"""
    drive.brake()
    wait(SCAN_SETTLE_MS)
    results = []
    cg = 0
    cr = 0
    for _ in range(SCAN_FRAMES):
        lane, corner = classify(husky_read_blocking(), d, y)
        if lane is not None:
            results.append(lane)
        if corner is True:
            cg += 1
        elif corner is False:
            cr += 1
    corner_g1 = None
    if cg != cr:
        corner_g1 = cg > cr
    if len(results) == 0:
        return None, corner_g1
    greens = 0
    for r in results:
        if r[0]:
            greens += 1
    if greens * 2 == len(results):
        g1 = results[len(results) - 1][0]               # تعادل: آخر قراءة
    else:
        g1 = greens * 2 > len(results)
    best = None
    for r in results:
        if r[0] == g1:
            best = r
    return best, corner_g1


def cube_ahead(d):
    """الألتراسونيك قرأ شيء على مسافة d: الكاميرا تفحص إطارات جديدة.
       يرجع (G1, عمق, جانبي) لو في مكعب أمامنا على نفس بُعد القراءة (= قرأ المكعب وليس جدار)، وإلا None"""
    best = None
    best_h = 0
    for i in range(CONFIRM_FRAMES):
        # سقف زمني للفحص أثناء الحركة: كاميرا بطيئة كانت تأكل حتى 240 مم من مسافة بدء اللفة
        blocks = husky_read_blocking(200 if i == 0 else 150, fresh=(i == 0))
        for b in blocks:
            if b[4] not in (GREEN_ID, RED_ID) or b[3] < MIN_BLOCK_H:
                continue
            depth_cm = FOCAL_PX * PILLAR_H_CM / b[3]
            lat_cm = (b[0] - CAM_CX) * depth_cm / FOCAL_PX
            if abs(lat_cm) <= FRONT_LAT_CM and abs(depth_cm * 10 - d) <= FRONT_TOL_MM and b[3] > best_h:
                best_h = b[3]
                best = (b[4] == GREEN_ID, depth_cm, lat_cm)
    return best


# =====================================================
#  البداية: تصفير التوجيه + نقطة إثبات الـ YAW
# =====================================================
try:
    steer.reset_angle(None)    # الزاوية المطلقة للموتر (نفس الأرقام التي قستها: يسار 87 / يمين -72)
except Exception:
    pass                       # لو غير مدعوم نكمل بالزاوية الحالية
steer.run_target(300, 0)       # الموتر B يتحرك إلى الزاوية 0 (العجلتان مستقيمتان)
while not hub.imu.ready():
    wait(50)
wait(500)
hub.imu.reset_heading(0)       # هذا هو المرجع الثابت: كل الدورانات تُحسب منه
drive.reset_angle(0)
print("YAW مرجع = 0 | جاهز")

turns = 0
total_turns = LAPS * 4
base_heading = 0               # = turns * 90 * TURN_DIR دائماً
offset = 0
ob_active = False              # هل نتتبع مكعباً الآن؟
ob_pos_mm = 0                  # موقع المكعب المتتبَّع على مسار السيارة (بالمسافة المقطوعة)
G1 = None                      # لون المكعب المتتبَّع: True أخضر | False أحمر | None لا يوجد
prev_g1 = None                 # لون آخر عائق تجاوزناه
last_ob_end_mm = -100000       # متى تجاوزنا آخر عائق
last_scan_mm = -100000         # آخر نقطة توقف وفحص (-100000 = افحص فوراً)
y_cm = 0.0                     # الانحراف الجانبي المقدّر عن وسط الممر (موجب = يمين)
last_turn = StopWatch()
dbg = StopWatch()
clock = StopWatch()
last_turn_mm = 0
finishing = False
wall_hits = 0                  # عدد قراءات الألتراسونيك المتتالية القريبة
check_timer = StopWatch()      # فاصل بين فحوص الكاميرا
last_check_cube = False        # نتيجة آخر فحص: كان مكعب؟
corner_g = 0                   # أصوات: مكعب الزاوية القادمة أخضر
corner_r = 0                   # أصوات: مكعب الزاوية القادمة أحمر
corner_lock = None              # أول لون يكتمل تصويته للزاوية يُقفل أساسًا ولا ينقلبه تصويت لاحق (أولوية أول قراءة)
last_frame_no = 0
drive_votes = 0                # تصويت الكشف أثناء الحركة
vote_g1 = None                 # لون آخر إطار شارك في التصويت
vote_pos_mm = 0.0              # موقع آخر مكعب صوّتنا له
last_lane_frame = 0            # آخر إطار شارك في تصويت الحركة
cur_speed = DRIVE_SPEED        # السرعة الحالية المطبقة (نغيرها فقط عند انتقال حالة التتبع)

set_steer(0)
wait(300)
drive.run(DRIVE_SPEED)

prev_t = clock.time()
prev_h = hub.imu.heading()
prev_ang = drive.angle()
travelled = 0.0                # المسافة الكلية بالمم
rate = 0

while True:
    now = clock.time()
    heading = hub.imu.heading()
    dt = now - prev_t
    if dt > 0:
        r = (heading - prev_h) * 1000 / dt
        rate = 0.6 * rate + 0.4 * r
    prev_t = now
    prev_h = heading

    # المسافة المقطوعة + تقدير الانحراف الجانبي
    ang = drive.angle()
    ds = (ang - prev_ang) / 360 * WHEEL_CIRC_MM
    prev_ang = ang
    travelled += ds
    y_cm += ds * sin(radians(heading - base_heading)) / 10

    blocks = husky_poll()
    d = ultra.distance()
    if yellow_seen(blocks):
        d = FRONT_MUTE_MM           # شفنا الأصفر: الحساس الأمامي اسكت (لا لفة جدران ولا طوارئ)؛ الكاميرا والفحص الواقف والحساسات الجانبية يكملون
    lane_cube, corner_cube = classify(blocks, d, y_cm)

    # ---------- 1) تفادي المكعبات (G1: أخضر = True يسار | أحمر = False يمين) ----------
    # المكعب الجديد يُكتشف عند التوقف والفحص (القسم 1ب). أثناء المشي نكتفي بتحديث موقع
    # المكعب المتتبَّع. حتى لو اختفى من الكاميرا نكمل مناورته حتى تتجاوزه السيارة كلها.
    pillar_in_front = False
    close_pillar = False
    seen_pillar = False
    if ob_active and travelled > ob_pos_mm + REAR_CLEAR_MM:
        ob_active = False                               # تجاوزناه بالكامل
        if G1 is not None:
            prev_g1 = G1                                # نتذكر لون العائق السابق
        last_ob_end_mm = travelled
        last_scan_mm = -100000                          # نفحص المكعب التالي فوراً
        G1 = None
        drive_votes = 0
        vote_g1 = None
    if lane_cube is not None:
        seen_pillar = True
        g1_now, depth_cm, lat_cm = lane_cube
        pillar_in_front = abs(depth_cm * 10 - d) < 150 and abs(lat_cm) < 12
        pos = travelled + depth_cm * 10
        if ob_active:
            # أولوية أول لون قُرئ (طلب ميداني): نكمل مناورة نفس المكعب ما دام مرئيًا أمامنا
            same = abs(pos - ob_pos_mm) < SAME_PILLAR_MM and travelled < ob_pos_mm + REAR_CLEAR_MM
            if same and G1 is not None and depth_cm > MIN_UPDATE_DEPTH_CM:
                ob_pos_mm = max(ob_pos_mm, pos)         # نفس المكعب: موقعه للأمام فقط
                close_pillar = depth_cm < 60
                if pos > travelled:                     # ما دام قدامنا: نواصل الدفع جانبيًا
                    offset = plan_offset(G1, depth_cm, lat_cm, y_cm)
        elif depth_cm < NOW_DEPTH_CM and frame_no != last_lane_frame:
            # كشف أثناء الحركة: تصويت سريع على الإطارات الجديدة بدل التوقف
            last_lane_frame = frame_no
            if depth_cm < EMERGENCY_DEPTH_CM or abs(lat_cm) < DEAD_AHEAD_CM:
                drive_votes = DRIVE_VOTES               # قريب جدًا أو على محورنا مباشرة: إطار واحد يكفي
            elif vote_g1 == g1_now and abs(pos - vote_pos_mm) < SAME_PILLAR_MM:
                drive_votes += 1                        # نفس اللون ونفس الموقع تقريبًا
            else:
                drive_votes = 1                         # تغيّر اللون أو المكعب: نصفر
            vote_g1 = g1_now
            vote_pos_mm = pos
            if drive_votes >= DRIVE_VOTES:
                ob_active = True
                G1 = g1_now
                ob_pos_mm = pos
                close_pillar = depth_cm < 60
                offset = plan_offset(G1, depth_cm, lat_cm, y_cm)
                drive_votes = 0
                vote_g1 = None
    if ob_active and travelled >= ob_pos_mm and lane_cube is None:
        offset = 0                                      # بلغنا موقع المكعب واختفى عن الكاميرا: نستقيم (لو ما زال مرئيًا نكمل الشغل حتى يختفي)
    pillar_active = ob_active
    if not ob_active:
        offset = 0
    target_speed = int(DRIVE_SPEED * PILLAR_SPEED_FRAC) if pillar_active else DRIVE_SPEED
    if target_speed != cur_speed:
        drive.run(target_speed)                         # إبطاء أثناء التتبع واستئناف السرعة الكاملة بعده
        cur_speed = target_speed

    # مكعب الزاوية القادمة: يظهر في طرف الكاميرا وخارج ممرنا (ID 1 أخضر | ID 2 أحمر)
    if frame_no != last_frame_no:
        last_frame_no = frame_no
        if corner_cube is True:
            corner_g += 1
        elif corner_cube is False:
            corner_r += 1
    next_g1 = None
    if corner_g >= CORNER_VOTES or corner_r >= CORNER_VOTES:
        next_g1 = corner_g > corner_r
        if corner_lock is None:
            corner_lock = next_g1               # أول لون يكتمل: يبقى الأساس حتى الزاوية

    # ---------- 1ب) توقف وفحص (Stop & Look) ----------
    if (not ob_active and not finishing and d > EMERGENCY_MM + 100
            and travelled - last_scan_mm >= SCAN_STEP_MM):
        res, cg = scan_pillar(d, y_cm)
        if cg is not None:                              # قراءة وهي ثابتة: صوت قوي لمكعب الزاوية
            if cg:
                corner_g += CORNER_VOTES
            else:
                corner_r += CORNER_VOTES
        ang = drive.angle()                             # المسافة أثناء الفرملة
        travelled += (ang - prev_ang) / 360 * WHEEL_CIRC_MM
        last_scan_mm = travelled
        if res is not None:
            G1, depth_cm, lat_cm = res
            ob_active = True
            ob_pos_mm = travelled + depth_cm * 10
            offset = plan_offset(G1, depth_cm, lat_cm, y_cm)
            if DEBUG:
                print("فحص: G1 =", G1, "عمق", int(depth_cm), "جانبي", int(lat_cm), "offset", int(offset))
        elif DEBUG:
            print("فحص: لا يوجد مكعب")
        drive.run(DRIVE_SPEED)
        prev_t = clock.time()
        prev_h = hub.imu.heading()
        prev_ang = drive.angle()
        rate = 0
        continue

    # ---------- 2) الزوايا (YAW + كاميرا + ألتراسونيك) ----------
    can_turn = last_turn.time() > MIN_TURN_GAP_MS and not finishing
    # شكل اللفة حسب مكعب الزاوية: أحمر => أكبر ومتأخرة | أخضر => أصغر وبدري
    plan_g1 = next_g1
    if plan_g1 is None and prev_g1 is False and travelled - last_ob_end_mm < WIDE_MEMORY_MM:
        plan_g1 = False                                 # بعد عائق أحمر والمكعب التالي محجوب: نعتبره أحمر
    frac, trigger_d = turn_plan(plan_g1)
    wall_now = d < trigger_d and not pillar_in_front and not ob_active
    wall_hits = wall_hits + 1 if wall_now else 0
    turn_now = False
    if can_turn and (wall_hits >= WALL_CONFIRM or d < EMERGENCY_MM):
        # الألتراسونيك قرأ شيء قريب: نسأل الكاميرا (مكعب أم جدار؟) قبل ما ندور
        if check_timer.time() > CHECK_GAP_MS:
            cube = cube_ahead(d)
            ang = drive.angle()
            travelled += (ang - prev_ang) / 360 * WHEEL_CIRC_MM     # المسافة أثناء الفحص
            prev_ang = ang
            check_timer.reset()
            last_check_cube = cube is not None
            if cube is not None:
                # الكاميرا شافت مكعب على نفس المسافة: القراءة مكعب وليست جدار => نتفاداه ولا ندور
                if DEBUG:
                    print("الألتراسونيك قرأ مكعب وليس جدار | قراءة", d, "| G1 =", cube[0], "عمق", int(cube[1]))
                if not ob_active:
                    G1, depth_cm, lat_cm = cube
                    ob_active = True
                    ob_pos_mm = travelled + depth_cm * 10
                    offset = plan_offset(G1, depth_cm, lat_cm, y_cm)
                wall_hits = 0
                prev_t = clock.time()
                prev_h = hub.imu.heading()
                rate = 0
                continue
            turn_now = True                                         # الكاميرا ما شافت مكعب = جدار فعلاً
            if DEBUG:
                print("الكاميرا أكدت: جدار | قراءة", d)
        else:
            turn_now = not last_check_cube                          # نستخدم نتيجة الفحص الأخير
    if turn_now:
        target = (turns + 1) * 90 * TURN_DIR            # دائماً 90 × رقم الزاوية
        set_steer(-TURN_DIR * frac)
        if DEBUG:
            print("دوران | مكعب الزاوية:", plan_g1, "| توجيه", frac, "| بدأ عند", d, "مم")
        extra = 0                                       # كسر اللفة الإضافي بالـ YAW (درجات)
        sharp_g1 = None
        sharp_mm = SHARP_HOLD_MM
        while (target + TURN_DIR * extra - hub.imu.heading()) * TURN_DIR > 8:
            if extra == 0:
                # أثناء اللفة: مكعب قريب على جهة اللفة أو جدار قريب => نكسر اللفة أكثر
                bl = closest_block(husky_poll())
                hit = ultra.distance() < TURN_WALL_MM
                if bl is not None:
                    depth = FOCAL_PX * PILLAR_H_CM / bl[3]
                    on_turn_side = (bl[4] == GREEN_ID) == (TURN_DIR < 0)
                    if depth <= SHARP_DEPTH_CM and on_turn_side and abs(bl[0] - CAM_CX) < 120:
                        hit = True
                        sharp_g1 = (bl[4] == GREEN_ID)
                        sharp_mm = depth * 10
                if hit:
                    extra = SHARP_EXTRA_DEG
                    set_steer(-TURN_DIR)                # أقصى توجيه
            wait(10)
        travelled += (drive.angle() - prev_ang) / 360 * WHEEL_CIRC_MM
        turns += 1
        base_heading = target
        if ob_active and G1 is not None:
            prev_g1 = G1
            last_ob_end_mm = travelled
        offset = 0
        ob_active = False
        G1 = None
        y_cm = 0.0
        drive_votes = 0
        vote_g1 = None
        husky_reset()                                   # نمسح قراءات الممر القديم
        last_turn.reset()
        last_turn_mm = travelled
        last_scan_mm = -100000                          # نفحص فوراً بعد الزاوية
        wall_hits = 0
        last_check_cube = False
        corner_g = 0
        corner_r = 0
        corner_lock = None
        if extra > 0:
            # كسر اللفة: نحافظ على انحراف YAW إضافي حتى نتجاوز المكعب/الجدار
            ob_active = True
            G1 = sharp_g1
            ob_pos_mm = travelled + max(sharp_mm - 100, 150)
            offset = TURN_DIR * extra
        if turns >= total_turns:
            finishing = True
        prev_t = clock.time()
        prev_h = hub.imu.heading()
        prev_ang = drive.angle()
        rate = 0
        continue

    # ---------- 3) الحفاظ على الاتجاه ----------
    center_off = 0
    if USE_ODOM_CENTER and not pillar_active:
        center_off = -KY * y_cm
        center_off = max(-MAX_CENTER_OFFSET, min(MAX_CENTER_OFFSET, center_off))

    safe_off = 0
    if USE_SIDE_SAFETY:
        dr = ultra_r.distance()
        dl = ultra_l.distance()
        if dr < SAFE_SIDE_MM:                           # قريب من الجدار/المكعب يميناً: نميل يساراً
            safe_off -= min(SAFE_MAX_DEG, SAFE_GAIN * (SAFE_SIDE_MM - dr))
        if dl < SAFE_SIDE_MM:                           # قريب يساراً: نميل يميناً
            safe_off += min(SAFE_MAX_DEG, SAFE_GAIN * (SAFE_SIDE_MM - dl))

    ref = base_heading + offset + center_off + safe_off
    if pillar_active:
        s = PILLAR_KP_HEAD * (heading - ref) + PILLAR_KD_HEAD * rate
    else:
        s = KP_HEAD * (heading - ref) + KD_HEAD * rate
    if close_pillar:
        lim = 1.0
    elif pillar_active:
        lim = PILLAR_STEER_LIMIT
    else:
        lim = CENTER_STEER_LIMIT
    s = max(-lim, min(lim, s))
    set_steer(s)

    if DEBUG and dbg.time() > 500:
        print("F", d, "next", next_g1, "trig", int(trigger_d), "G1", G1, "votes", drive_votes, "off", int(offset), "safe", int(safe_off), "y", int(y_cm),
              "head", int(heading), "turns", turns,
              "v_cms", int(abs(drive.speed()) * WHEEL_CIRC_MM / 3600))
        dbg.reset()

    # ---------- 4) النهاية ----------
    if finishing:
        if travelled - last_turn_mm >= FINISH_MM:
            drive.stop()
            set_steer(0)
            break

    wait(5)
