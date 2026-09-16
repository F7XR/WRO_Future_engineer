# 🤖 روبوت WRO مهندسي المستقبل | WRO Future Engineers Robot

> روبوت ذاتي القيادة لمسابقة **World Robot Olympiad — Future Engineers**
> A self-driving robot built for the **World Robot Olympiad — Future Engineers**

---

## 📌 نظرة عامة | Overview


روبوتنا يتحكم بنفسه تلقائيا في أرض التحدي مع الحفاظ على مسافة ثابتة بينه وبين الجدار،
واكتشاف الحواجز في طريقه، وقراءة الحواجز الخضراء والحمراء بكاميرا مبرمجة على اللوني الاخضر والاحمر.
بدلا من نظام القيادة العادي الشائع، صمّمنا **محور توجيه حقيقي بطريقة سيارات RC**
— مما منح الروبوت حركة تشبه السيارات، و دقيقة وقابلة للتكرار.


Our robot drives automatic around the challenge field while keeping a constant
distance from the walls, detecting obstacles ahead, and reading colored signs with
an AI camera. Instead of the common differential drive, we engineered a
**real steering axle inspired by RC cars** — giving the robot car-like,
predictable, repeatable motion.

|   Subsystem |   Our Choice |
|---|---|
| 🧠 العقل/ Brain | LEGO SPIKE Prime Hub + Pybricks(Programing APP) |
| 🎯 التوجيه / Steering |  محرك ليقو متوسط لنظام التوجيه   / Medium motor for steering system |
| ⚙️ الدفع / Drive | عجلتان خلفيتان / 2 × rear wheels |
| 📡 المسافات / Distance | 3 × Ultrasonic (أمام · يسار · يمين / front · left · right) |
| 👁 الرؤية / Vision | HuskyLens AI Camera |
| 🔌 الدمج / Integration | تلحيم مباشر — تغذية مباشرة من العقل / Soldered direct wiring |

---

## 🔧 التصميم الميكانيكي | Mechanical Design

### نظام التوجيه 🎯 | Steering System


قلب الروبوت هو **محور توجيه حقيقي بنفس نظام سيارات RC:**
- **محرك سيرفو مخصص** يحرّك العجلات الأمامية يميناً ويساراً.
- **نظام التوجيه** — كل عجلة أمامية تدور حول محورها الخاص، فيلتف الروبوت
  بسلاسة تامة **بدون سحب للإطارات ودون انزلاق جانبي**.

**🇬🇧 English:**
The heart of our robot is a **genuine steering axle, exactly like RC cars:**
- A dedicated **servo motor** turns the front wheels left and right.
- **Ackermann geometry** — each front wheel pivots on its own axis,
  so the robot corners smoothly with **zero tire drag and no side slipping**.

### منظومة الدفع ⚙️ | Drivetrain


- **عجلتان خلفيتان** تنقلان قوة الدفع.
- أثقل المكوّنات (العقل + البطارية) موضوعة **مباشرة فوق محرك الدفع الخلفي**،
  فتتحول قوة المحركات إلى أقصى تماس — بلا دوران للعجلات عند الانطلاق.
- **مركز ثقل منخفض** يثبّت الهيكل أثناء مناورات التفادي الحادة.


- **Two rear wheels** deliver the drive power.
- The heaviest parts (hub + battery) sit **directly above the rear drive motor**,
  converting motor torque into maximum traction — no wheel spin on launch.
- A **low center of gravity** keeps the chassis planted during sharp avoidance turns.

---

## 👁 الحساسات والرؤية | Sensors & Vision

### الحساسات الترا سونيك الثلاثة | 3 × Ultrasonic Sensors

| الحساس / Sensor | الوظيفة / Role |
|---|---|
| **الأمامي / Front** | كشف الحواجز حتى **100 سم** ← يفعّل التفادي ويتحكم بالسرعة / Detects obstacles up to **100 cm** → triggers avoidance & speed control |
| **اليمين / Right** | يثبّت مسافة **20 سم** عن الجدار (حساس التتبع الأساسي) / Keeps a constant **20 cm** from the wall (main following sensor) |
| **اليسار / Left** | قراءة مرآة — احتياطي للتتبع وإدراك حدود الأرضية / Mirror reading — backup for following & field-edge awareness |

### كاميرا HuskyLens 📷 | HuskyLens AI Camera

مركّبة على واجهة الروبوت الأمامية، تتعرّف على **اللافتات الملوّنة** أثناء الجولة:
- 🟢 **إشارة خضراء ← انعطاف يسارا**
- 🔴 **إشارة حمراء ← انعطاف يمينا**


Mounted on the robot's front face, it recognizes **colored signs** during the run:
- 🟢 **Green signal → turn left**
- 🔴 **Red signal → turn right**

### دمج Pybricks  | Pybricks Integration


نبرمج عقل SPIKE Prime ببيئة **Pybricks**، وهي التي جعلت هذه المعمارية ممكنة:
- تحكم كامل بلغة **Python** على المحركات والحساسات.
- دعم **الاتصال المباشر بكاميرا HuskyLens** من خلال العقل.
- تنفيذ منخفض الكمون لقرارات التوجيه اللحظية.

>  **تفصيل هندسي أساسي:** قمنا **بتلحيم أسلاك منفذ SPIKE Prime مباشرة
> على كاميرا HuskyLens**، لتتصل بالكاميرا في منفذ العقل وتعمل **بشكل مباشر** —
> بلا لوحات محوّلات، وبلا بطارية منفصلة. هذا جعل منظومة الرؤية
> **موثوقة 100%** في جولات المسابقة، دون أي انقطاع في الاتصال.

We program the SPIKE Prime Hub with **Pybricks**, which is what makes this
architecture possible:
- Full **Python** control over motors and sensors.
- **Native connection support for the HuskyLens** through the hub.
- Low-latency execution for real-time steering decisions.

>  **Key engineering detail:** we **soldered the SPIKE Prime connector wires
> directly onto the HuskyLens**, so the camera plugs into a hub port and runs
> **directly** — no adapter boards, no converters, no separate battery. This made
> the vision system **100% reliable** in competition runs with zero connection drops.

---

## 💻 البرمجيات | Software

**يحتوي المستودع على برنامجين كاملين للروبوت:**
**The repository ships with two complete programs:**

### 1️⃣ `Free Lab` — تشغيل **بدون وجود الحواجز** | run **without obstacles**

- تتبّع مستقر للجدار على مسافة 20 سم.
- منعطفات قرار بناءً على الرؤية.
- مضبوط لأسرع لفة نظيفة.

- Steady wall-following at 20 cm.
- Vision-based decision turns.
- Tuned for the **fastest clean lap**.

### 2️⃣ `Obstacle Run` — وضع التحدي الكامل **مع وجود الحواجز** | full challenge mode

- **الحساس الأمامي يرى حاجزاً على أقل من 100 سم ←** ينفّذ مناورة
  انحراف يميناً ديناميكية.
- يعيد الالتصاق بالجدار ويكمل اللفة.

- **Front sensor sees an obstacle < 100 cm →** executes a dynamic
  right-side avoidance maneuver.
- Re-locks onto the wall and continues the lap.

### الآلة المشتركة | Shared Core

البرنامجان يشتركان في نواة واحدة: **آلة حالات محدودة**

`تهيئة ومعايرة ← تتبع الجدار ← تفادي الحاجز / منعطف القرار ← تتبع الجدار …`

مع منطق أمان: إذا قفزت قراءة حساس بشكل شاذ، يثبّت الروبوت اتجاهه
بالحساسات المتبقية بدلاً من التوقف.

Both programs share one core: a **Finite State Machine**

`INIT (calibrate) → WALL FOLLOW  → OBSTACLE AVOID / DECISION TURN → WALL FOLLOW …`

with fail-safe logic: if a sensor reading jumps abnormally, the robot holds its
heading using the remaining sensors instead of stopping.

---

## 🚀 البدء السريع | Quick Start

1. جمّع الهيكل (محور التوجيه بنمط RC + الدفع الخلفي).
2. وصّل **الحساسات الترا سونيك الثلاثة** و**كاميرا HuskyLens** بمنافذ العقل.
3. ثبّت firmware الخاص بـ **Pybricks** على عقل SPIKE Prime.
4. ارفع البرنامج المطلوب — `Free Lab` أو `Obstacle Run`.
5. ضع الروبوت على الأرضية واضغط تشغيل 🏁

1. Assemble the chassis (RC-style steering axle + rear drive).
2. Connect the **3 ultrasonic sensors** and the **HuskyLens** to the hub ports.
3. Flash the **Pybricks** firmware to the SPIKE Prime Hub.
4. Upload the program you need — `Free Lab` or `Obstacle Run`.
5. Place the robot on the field and hit run 🏁

---

## 👥 أعضاء الفريق | Team Members

| العضو / Member | الدور / Role |
|---|---|
| **بدر بخاري — Badr Bukhari** | التصميم الميكانيكي ونظام التوجيه بنمط RC / Mechanical design & RC steering system |
| **ماهر الحربي — Maher Al-Harbi** | البرمجيات — Pybricks، آلة الحالات، ومنطق تتبع الجدار / Software — Pybricks, FSM & wall-following logic |

🧑‍🏫 **المدرب — Coach:** **أسامة محروس — Osama Mahrous**

---

## 📄 الرخصة | License




MIT License

Copyright (c) 2026 AQSA ROBO FORCE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
