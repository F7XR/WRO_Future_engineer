# 🤖 روبوت WRO للمهندسين المستقبليين | WRO Future Engineers Robot

> روبوت ذاتي القيادة لمسابقة **World Robot Olympiad — Future Engineers**
> A self-driving robot built for the **World Robot Olympiad — Future Engineers**

---

## 📌 نظرة عامة | Overview

**🇸🇦 عربي:**
روبوتنا يقود نفسه تلقائياً في أرض التحدي مع الحفاظ على مسافة ثابتة عن الجدار،
وإكتشاف الحواجز أمامه، وقراءة اللافتات الملوّنة بكاميرا ذكاء اصطناعي.
بدلاً من نظام القيادة التفاضلي الشائع، صمّمنا **محور توجيه حقيقي بنفس طريقة سيارات RC**
— مما يمنح الروبوت حركة تشبه السيارات، دقيقة وقابلة للتكرار.

**🇬🇧 English:**
Our robot drives autonomously around the challenge field while keeping a constant
distance from the walls, detecting obstacles ahead, and reading colored signs with
an AI camera. Instead of the common differential drive, we engineered a
**real steering axle inspired by RC cars** — giving the robot car-like,
predictable, repeatable motion.

| النظام / Subsystem | اختيارنا / Our Choice |
|---|---|
| 🧠 العقل / Brain | LEGO SPIKE Prime Hub + Pybricks |
| 🎯 التوجيه / Steering | سيرفو بنظام سيارات RC — هندسة آكرمان / RC-style servo — Ackermann |
| ⚙️ الدفع / Drive | عجلتان خلفيتان / 2 × rear wheels |
| 📡 المسافات / Distance | 3 × Ultrasonic (أمام · يسار · يمين / front · left · right) |
| 👁 الرؤية / Vision | HuskyLens AI Camera |
| 🔌 الدمج / Integration | تلحيم مباشر — تغذية مباشرة من العقل / Soldered direct wiring |

---

## 🔧 التصميم الميكانيكي | Mechanical Design

### نظام التوجيه 🎯 | Steering System

**🇸🇦 عربي:**
قلب الروبوت هو **محور توجيه حقيقي بنفس نظام سيارات RC:**
- **محرك سيرفو مخصص** يحرّك العجلات الأمامية يميناً ويساراً.
- **هندسة آكرمان** — كل عجلة أمامية تدور حول محورها الخاص، فيلتف الروبوت
  بسلاسة تامة **بدون سحب للإطارات ودون انزلاق جانبي**.
- الإنكودر المدمج في السيرفو يقرأ **زاوية التوجيه الفعلية لحظياً**،
  ما يتيح مناورات دقيقة ومتكررة حول العوائق.
- **روتين معايرة تلقائي** يعيد تصفير التوجيه عند كل تشغيل.

**🇬🇧 English:**
The heart of our robot is a **genuine steering axle, exactly like RC cars:**
- A dedicated **servo motor** turns the front wheels left and right.
- **Ackermann geometry** — each front wheel pivots on its own axis,
  so the robot corners smoothly with **zero tire drag and no side slipping**.
- The servo's built-in encoder reports the **exact steering angle in real time**,
  enabling precise, repeatable maneuvers around obstacles.
- A **home-alignment routine** re-centers the steering on every boot.

### منظومة الدفع ⚙️ | Drivetrain

**🇸🇦 عربي:**
- **عجلتان خلفيتان** تنقلان قوة الدفع.
- أثقل المكوّنات (العقل + البطارية) موضوعة **مباشرة فوق محور الدفع الخلفي**،
  فتتحول قوة المحركات إلى أقصى تماس — بلا دوران للعجلات عند الانطلاق.
- **مركز ثقل منخفض** يثبّت الهيكل أثناء مناورات التفادي الحادة.

**🇬🇧 English:**
- **Two rear wheels** deliver the drive power.
- The heaviest parts (hub + battery) sit **directly above the rear drive axle**,
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

**🇸🇦 عربي:**
مركّبة على واجهة الروبوت الأمامية، تتعرّف على **اللافتات الملوّنة** أثناء الجولة:
- 🟢 **إشارة خضراء ← انعطاف يميناً**
- 🔴 **إشارة حمراء ← انعطاف يساراً**

**🇬🇧 English:**
Mounted on the robot's front face, it recognizes **colored signs** during the run:
- 🟢 **Green signal → turn right**
- 🔴 **Red signal → turn left**

### دمج Pybricks ⚡ | Pybricks Integration

**🇸🇦 عربي:**
نبرمج عقل SPIKE Prime ببيئة **Pybricks**، وهي التي جعلت هذه المعمارية ممكنة:
- تحكم كامل بلغة **Python** على المحركات والحساسات.
- دعم **الاتصال المباشر بكاميرا HuskyLens** من خلال العقل.
- تنفيذ منخفض الكمون لقرارات التوجيه اللحظية.

> 🔥 **تفصيل هندسي أساسي:** قمنا **بتلحيم أسلاك منفذ SPIKE Prime مباشرة
> على كاميرا HuskyLens**، لتتصل بالكاميرا في منفذ العقل وتعمل **بشكل مباشر** —
> بلا لوحات محوّلات، وبلا بطارية منفصلة. هذا جعل منظومة الرؤية
> **موثوقة 100%** في جولات المسابقة، دون أي انقطاع في الاتصال.

**🇬🇧 English:**
We program the SPIKE Prime Hub with **Pybricks**, which is what makes this
architecture possible:
- Full **Python** control over motors and sensors.
- **Native connection support for the HuskyLens** through the hub.
- Low-latency execution for real-time steering decisions.

> 🔥 **Key engineering detail:** we **soldered the SPIKE Prime connector wires
> directly onto the HuskyLens**, so the camera plugs into a hub port and runs
> **directly** — no adapter boards, no converters, no separate battery. This made
> the vision system **100% reliable** in competition runs with zero connection drops.

---

## 💻 البرمجيات | Software

**يحتوي المستودع على برنامجين كاملين للروبوت:**
**The repository ships with two complete programs:**

### 1️⃣ `Free Lab` — تشغيل **بدون وجود الحواجز** | run **without obstacles**

**🇸🇦 عربي:**
- تتبّع مستقر للجدار على مسافة 20 سم.
- منعطفات قرار بناءً على الرؤية.
- مضبوط لأسرع لفة نظيفة.

**🇬🇧 English:**
- Steady wall-following at 20 cm.
- Vision-based decision turns.
- Tuned for the **fastest clean lap**.

### 2️⃣ `Obstacle Run` — وضع التحدي الكامل **مع وجود الحواجز** | full challenge mode

**🇸🇦 عربي:**
- تتبّع الجدار بتحكم PID.
- **الحساس الأمامي يرى حاجزاً على أقل من 100 سم ←** ينفّذ مناورة
  انحراف يميناً ديناميكية.
- يعيد الالتصاق بالجدار ويكمل اللفة.

**🇬🇧 English:**
- Wall-following with PID control.
- **Front sensor sees an obstacle < 100 cm →** executes a dynamic
  right-side avoidance maneuver.
- Re-locks onto the wall and continues the lap.

### الآلة المشتركة | Shared Core

**🇸🇦 عربي:**
البرنامجان يشتركان في نواة واحدة: **آلة حالات محدودة**

`تهيئة ومعايرة ← تتبع الجدار (PID) ← تفادي الحاجز / منعطف القرار ← تتبع الجدار …`

مع منطق أمان: إذا قفزت قراءة حساس بشكل شاذ، يثبّت الروبوت اتجاهه
بالحساسات المتبقية بدلاً من التوقف.

**🇬🇧 English:**
Both programs share one core: a **Finite State Machine**

`INIT (calibrate) → WALL FOLLOW (PID) → OBSTACLE AVOID / DECISION TURN → WALL FOLLOW …`

with fail-safe logic: if a sensor reading jumps abnormally, the robot holds its
heading using the remaining sensors instead of stopping.

---

## 🚀 البدء السريع | Quick Start

**🇸🇦 عربي:**
1. جمّع الهيكل (محور التوجيه بنمط RC + الدفع الخلفي).
2. وصّل **الحساسات الترا سونيك الثلاثة** و**كاميرا HuskyLens** بمنافذ العقل.
3. ثبّت firmware الخاص بـ **Pybricks** على عقل SPIKE Prime.
4. ارفع البرنامج المطلوب — `Free Lab` أو `Obstacle Run`.
5. ضع الروبوت على الأرضية واضغط تشغيل 🏁

**🇬🇧 English:**
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

**🇸🇦 عربي:** صدر هذا العمل تحت رخصة **MIT** — استخدموه، تعلّموا منه،
وابنوا شيئاً أفضل. حظاً موفقاً في الملعب! 🏆

**🇬🇧 English:** Released under the **MIT License** — reuse it, learn from it,
and build something even better. Good luck on the field! 🏆
