# Zo‘r — endi tushundim. Quyida OOP mavzularini **basic → advanced** tartibida olasan: har bir mavzu uchun **bitta amaliy vazifa (TZ)**, vazifa bosqichlari va talablarining batafsil tushuntirishi, qaysi OOP/texnik konseptlar ishlatilgani va agar sen bilmasang — o‘sha ishlatilgan narsaning qisqacha tushuntirishini beraman. Kodni **sen yozasan** — men konsept, arxitektura va sinf/mas’uliyat rejasini beraman. Men senga shunchaki “mukammal” emas, balki “ruthless mentor” uslubida to‘g‘ridan-to‘g‘ri va amaliy maslahatlar beraman — zerikarli fluff yo‘q.

# ---

# # Qanday o‘qish kerak (tez ko‘rsatma)

# 1. Har bir TZni oldindan o‘qib chiqing, keyin kod yozing.
# 2. Avval oddiy, toza, sinfga asoslangan in-memory yechim yozing — file yoki pickle bilan persistence kerak bo‘lsa, so‘rang.
# 3. Har bir vazifa uchun unit-test yoz. Test yozmasang — sening koding “ishlaydi” deb o‘ylash xato bo‘ladi.
# 4. Keyingi mavzuga o‘tganda oldingi vazifani kengaytiring (refactor), yangi patternni integratsiya qiling.
# 5. So‘nggi mini-project — hamma narsani birlashtirish, boshlash uchun in-memory, so‘ngra DB/Redis/Celery kabi komponentlarga ko‘chirish.

# ---

# # 1 — Sinflar & Instanslar (Class & Instance) — Boshlang‘ich

# **TZ:** `UserProfile` sinfi (in-memory). Maydonlar: `username`, `email`, `balance`. Metodlar: `deposit(amount)`, `withdraw(amount)`. `withdraw` balans yetmasa `InsufficientFundsError` tashlashi kerak.

# **Detallar / qadamlar:**

# * Konstruktorda validatsiya: username/email format (eng oddiy regex yoki `contains('@')` yetadi).
# * `deposit` — musbat son tekshiruvi, return yangi balans.
# * `withdraw` — atomic bo‘lmasa ham unit testda ketma-ket chaqirish to‘g‘ri ishlashini tekshir.
# * Qoida: hech qachon `balance` ni to‘g‘ridan-to‘g‘ri tashqaridan o‘zgartirishga ruxsat bermaymiz — private atribut (convention: `_balance` yoki `__balance`).

# **OOP konseptlar:** sinflar, instanslar, enkapsulyatsiya, istisnolar.

# **Agar bunday narsalar noma’lum bo‘lsa (izoh):**

# * *Enkapsulyatsiya* — sinf ichidagi holatni (state) bevosita tashqaridan o‘zgartirishni cheklash.
# * *Exception class* — `class InsufficientFundsError(Exception): ...` yozish — bundan keyin test va caller `try/except` bilan tutadi.

# **Mentor note:** oddiy, lekin hamma narsa shu yerda boshlanadi. Agar bu vazifada testsiz boshlasang, keyingilari qiyin bo‘ladi.

# ---

# # 2 — Atributlar & Properties (Getter/Setter)

# **TZ:** `Product` sinfi. `price` private bo‘ladi. Tashqaridan `price` ga set qilishda `property` va `@price.setter` dan foydalan — price musbat son bo‘lishi kerak. Ayrıca read-only sifatida `id` beriladi (uuid).

# **Detallar:**

# * `__init__` ichida `id = uuid4()` generatsiya qiling.
# * `@property price` qaytaradi; `@price.setter` validatsiya qiladi.
# * `__repr__` foydali matn qaytarsin (debug uchun).

# **OOP konseptlar:** enkapsulyatsiya, properties, immutability qayerda kerakligi.

# **Tushuntirish:** `property` — tashqaridan attribute kabi ko‘rinadi, ammo ichida getter/setter logikasi bor. Bu muhim: keyinroq DB modelga yoki serialization’ga o‘tganingda bu joyni o‘zgartirmasdan foydalanaverasan.

# ---

# # 3 — Kompozitsiya (Composition)

# **TZ:** `Order` sinfi: har bir `Order` `List[OrderLine]` dan tashkil topgan bo‘lsin. `OrderLine` — `product: Product`, `quantity`. `Order`da `total()` metodi bo‘lsin.

# **Detallar:**

# * `Order` sum/totalni hisoblaydi iteratsiya orqali.
# * `OrderLine` ichida `line_total()` bo‘lsin (`product.price * quantity`).
# * `Order`ga `add_line(product, qty)` va `remove_line(product_id)` metodlari bo‘lsin.

# **OOP konseptlar:** composition (has-a), delegation (order.total delegatsiya qiladi orderline.line_total ga).

# **Nima uchun muhim:** composition inheritancega nisbatan moslashuvchan — sinflarni qayta ishlatish oson.

# ---

# # 4 — Inheritance & Abstract Base Classes

# **TZ:** `PaymentMethod` — abstrakt sinf (`process(amount)` abstrakt). Keyin `CreditCardPayment` va `BankTransferPayment` yozib, har birining `process`i turlicha “simulyatsiya qilingan” logika bilan bo‘lsin (in-memory).

# **Detallar:**

# * Use `abc.ABC` va `@abc.abstractmethod`.
# * `PaymentMethod`da umumiy sanab olingan validatsiyalar bo‘lishi mumkin (e.g., minimal amount).
# * Test yoz: `issubclass` va `isinstance` testlari.

# **OOP konseptlar:** inheritance, Liskov Substitution (subclass base sinf o‘rnini to‘liq egallashi kerak), polymorphism (kod caller `PaymentMethod` tipiga ishonadi).

# **Tushuntirish:** abstract base class — umumiy API talab qiladi; turli implementatsiyalarni almashtirish oson bo‘ladi.

# ---

# # 5 — Polimorfizm va Strategy pattern

# **TZ:** `DiscountStrategy` interface yoz — `apply(order)` metod. `NoDiscount`, `PercentageDiscount`, `BuyXGetYFree` implementatsiyalari bo‘lsin. `Order`ga `discount_strategy` inject qilinsa, `order.final_total()` shu strategiaga asoslanib qaytaradi.

# **Detallar:**

# * Strategy pattern — behaviorni runtime’da almashtirish.
# * `PercentageDiscount(percent)` — oddiy formula.
# * `BuyXGetYFree(product_id, x, y)` — order linesni tahrirlaydi va hisoblaydi.

# **OOP konseptlar:** polymorphism, composition, single responsibility (discount logikasi alohida sinfda).

# **Agar bilmaydigan bo‘lsa:** Strategy pattern — algoritmlarni obyektda saqlash va ularni oson almashtirish uchun.

# ---

# # 6 — Dunder methods & Rich objects

# **TZ:** `Money` klassi: `__add__`, `__sub__`, `__eq__`, `__repr__`, `__lt__`. Currency mismatchda `CurrencyMismatchError`.

# **Detallar:**

# * `Money(amount, currency)`, `amount` — `Decimal` bilan ishlansin (floats yomon).
# * Operator overloading orqali `a + b` ishlashi kerak.
# * Immutability: `Money` obyektlari o‘zgarmas bo‘lsin (yangi obyektda natija qaytsin).

# **OOP konseptlar:** operator overloading, immutability, value objects.

# **Nima uchun:** biznes logikasida pulni float bilan qilmaslik — presizion muhim.

# ---

# # 7 — SOLID printsiplari (amaliy mashq)

# **TZ:** Kichik “ReportGenerator” pipeline: `ReportGenerator` faqat reportni hosil qilsin; *writing/saving* funksiyasi alohida `ReportStorage` sinfida bo‘lsin. Yangi format qo‘shish uchun `ReportFormatter` abstrakt sinf bo‘lsin.

# **Detallar:**

# * SRP: har bir sinf faqat bitta sabab bilan o‘zgaradi.
# * OCP: yangi formatter qo‘shilganda eski kodga tegmasdan qo‘shilsin.
# * DIP: generator `ReportStorage`-ga emas, balki interface/abstractionga bog‘lansin (constructor injection).

# **Nima uchun:** bu printsiplar keyingi murakkab vertekslarni tushunishga yordam beradi.

# ---

# # 8 — Exception handling & Validation patterns

# **TZ:** Kiruvchi data (dict) oladigan `UserFactory` yoz — noto‘g‘ri data bo‘lsa `ValidationError` qaytaradi va xatoliklar ro‘yxatini (field -> message) saqlaydi.

# **Detallar:**

# * Fail-fast validation; collect errors vs first-error approach — ikkalasini sinab ko‘r.
# * Unit tests: malformed data, missing fields, invalid types.

# **Nima uchun:** real-world code’da noto‘g‘ri inputni boshqarish — debuggability va UX uchun muhim.

# ---

# # 9 — Decorators & Context managers — Advanced syntactic tools

# **TZ:** `timing` decorator yoz — funksiyani ishga tushirish vaqtini log qiladi. Shuningdek `transactional` kontekst menedjer (in-memory persistence simulyatsiyasi) yoz.

# **Detallar:**

# * `@timing` — wrapper pattern, `functools.wraps`.
# * `with transactional():` — kontekstni boshlaydi va xatolik bo‘lsa rollback qiladi (in-memory: saqlangan state’ni restore qilish).

# **OOP konseptlar:** higher-order behavior, separation of concerns.

# **Nima uchun:** dekoratorlar cross-cutting concerns (logging, timing, auth)ni toza usulda qo‘shadi.

# ---

# # 10 — Descriptors & Metaclasses (deep advanced)

# **TZ:** Oddiy `TypeChecked` descriptor yoz — attribute set qilinganda type tekshiradi (e.g., `name = TypeChecked(str)`). Keyin bitta sinfga metaclass yordamida avtomatik `__repr__` va `__eq__` qo‘shing.

# **Detallar:**

# * Descriptor — `__get__`, `__set__`, `__delete__`.
# * Metaclass — klass yaratishda o‘zgarish kiritadi (klassga xususiyat qo‘shish).
# * Test: descriptor type errorni ko‘rsatishi va metaclass tomonidan `__repr__` ishlashi.

# **Nima uchun:** bu sizga Python’da DSL yaratish, ORM-lar qanday ishlashini tushunish imkonini beradi.

# **Mentor note:** descriptor/metaclass — kuchli, ammo o‘qilishi qiyin. Faqat zarurat bo‘lsa ishlat.

# ---

# # 11 — Concurrency: threading, asyncio, and thread-safety

# **TZ:** `Counter` sinfi — `increment()` multithreaded muhitda ham to‘g‘ri ishlashi kerak; keyin `AsyncRateLimiter` asyncio bilan yoz.

# **Detallar:**

# * `Counter` uchun `threading.Lock()` ishlat va unit-test bilan 1000 thread/loop simulyatsiya qil (aralash uv—ishlash).
# * `AsyncRateLimiter` uchun `asyncio.Semaphore` yoki moving-window algorithm bilan ishlashini test qil.
# * Explaining pitfalls: GIL, race conditions, deadlocks.

# **Nima uchun:** backendda ko‘p request parallel ishlaydi — state mutate qilishda ehtiyot bo‘l.

# ---

# # 12 — Testing, TDD & Packaging — Amaliy yakun

# **TZ:** Har bir oldingi vazifa uchun unit tests yoz. Keyin `setup.py/pyproject.toml` bilan kichik library paketlash va `tox`/`pytest` workflow tuzish.

# **Detallar:**

# * Unit test: edge cases, fixtures.
# * Mocking: external API simulyatsiya qilish uchun `unittest.mock`.
# * CI: GitHub Actions uchun oddiy workflow yaml yozish (test run).

# **Nima uchun:** haqiqiy ish shunday — testsiz kod “ishlaydi” emas, “xato berishi mumkin”.

# ---

# # Final mini-project (hamma mavzular bir yoqda ishlaydi) — Advanced (API)

# **Nomi:** **Matchmaker & Turn-Based Game Session Manager (MTGSM)** — oddiy online turn-based o‘yin uchun lobby, matchmaking va game session manager API. *Eslatma:* bu todo/task emas va backend-oriented.

# **Nega yaxshi:** bu loyiha OOP, concurrency, events, strategy (matchmaking), composition (session contains players), abstractions (storage), decorators/context managers (transactional/state), dunder methods (GameState), testing va packaging hamma birlashtiradi. Bosqichma-bosqich soddadan murakkabgacha kengaytiriladi.

# ## Minimal scope (boshlanish uchun — **DB/Caching/Queues ishlatmaymiz**)

# * **Core sinflar (in-memory):**

#   * `Player` (UserProfile’dan foydalanish mumkin)
#   * `Lobby` (rooms, join/leave)
#   * `Matchmaker` (strategy pattern — e.g., `RandomMatch`, `RankedMatch`)
#   * `GameSession` (manages turns, `GameState` value object, `__repr__`, `__eq__`)
#   * `EventBus` (observer pattern — in-process pub/sub for subscribers like `Logger`, `Notification`)
#   * `Storage(ABC)` + `InMemoryStorage` (abstraction for persisting sessions/players)
# * **API layer:** minimal FastAPI (yoki Flask) endpoints:

#   * `POST /join_lobby` — player joins
#   * `POST /start_match` — invoke matchmaker
#   * `POST /session/{id}/move` — submit move
#   * `GET /session/{id}` — get state
# * **Concurrency:** `GameSession` runs asynchronously (asyncio task) to manage turn timeouts; protect shared state with locks or rely on single-threaded asyncio model.
# * **Testing:** unit tests for matchmaker strategies, game flow, concurrency tests for simultaneous joins.
# * **Packaging:** `pyproject.toml`, local test runner.

# ## Advanced extensions (learn and add later)

# * **Persistence:** switch `InMemoryStorage` → `SQLStorage` (Postgres).

#   * *Why DB?* durability, crash recovery, sharing across processes.
# * **Caching / fast state:** introduce Redis for lobby/session hot state (fast updates).

#   * *Why cache?* low latency, atomic ops (sorted sets for leaderboards, etc.).
# * **Message queue / background workers:** Celery/RabbitMQ for long running tasks (matchmaking, replay processing).

#   * *Why?* offload heavy jobs, reliability, retry.
# * **Scaling:** multiple API workers (uvicorn workers) + shared Redis storage + persistent DB.
# * **Observability:** metrics (Prometheus), traces (OpenTelemetry), logs.

# ## Nima ishlatish kerak hozir (soddalashtirilgan stack)

# * Python 3.11+, FastAPI (ASGI), uvicorn, pytest, pydantic (data validation), asyncio library features.
# * Hech qanday DB/Redis/Celery zarur emas boshlash uchun. InMemoryStorage va file-based snapshot bilan boshlang.

# ## Nima o‘rganasan bu orqali

# * OOP patterns: composition, strategy (matchmaking), observer (EventBus), value objects (GameState), dunder (GameState eq/rep), concurrency (asyncio tasks/locks), testing, packaging.
# * So‘ngra izchil tarzda DB/Redis/Celery ni birma-bir qo‘shib o‘rganish oson bo‘ladi — chunki kod abstraktsiyalangan bo‘ladi (`Storage(ABC)` orqali).

# ---

# # Agar sen bularni bilmasang — qisqacha tushuntirishlar va o‘rganish tartibi

# Agar DB/caching/queue-lar hozir noma’lum bo‘lsa, mana minimal yo‘l:

# 1. **SQL (Postgres)** — asosiy; o‘rganish 1–2 hafta: CREATE TABLE, indexes, transactions. (Why: persistent data)
# 2. **ORM (SQLAlchemy / Django ORM)** — 1 hafta: model mapping, sessions, migrations (alembic).
# 3. **Redis (cache)** — 3–5 kun: get/set, TTL, atomic ops (INCR, ZADD). (Why: speed, atomicity)
# 4. **Message queue (RabbitMQ / Redis streams / Kafka)** — 1–2 hafta: publish/subscribe, worker model. (Why: decouple, retries, heavy jobs)
# 5. **Celery / RQ** — background worker frameworks; 1 hafta.
#    Har birini amaliy loyihada bosqichma-bosqich qo‘sh: avval interface’ni (`Storage(ABC)`) ta’minla, so‘ngra haqiqiy backendni swap qil.

# ---

# # Qisqacha ish rejasi (sen uchun — 4 haftalik roadmap)

# * Hafta 1: 1–6 TZlarni yozish + unit tests (classes → composition → inheritance → strategy).
# * Hafta 2: 7–10 TZlar (SOLID, exceptions, decorators, context managers) + tests.
# * Hafta 3: 11–12 TZlar (concurrency + testing + packaging). Boshlang‘ich Matchmaker core sinflari yoz.
# * Hafta 4: FastAPI wrapper + tests + local run, refactor storage to `Storage(ABC)`. Keyin DB/Redis qo‘shishni boshlay olasan.

# ---

# Agar hoziroq boshlamoqchi bo‘lsang, ayt: qaysi mavzudan boshlamoqchisiz yoki qaysi bir TZni birinchi yig‘ib kodga o‘tkazamiz — men sen uchun **file tree**, **class diagram**, **DB schema (agar kerak bo‘lsa keyinroq)** va **unit test cases**ni kodsiz yozib beraman, keyin sen kodini yozasan va men uni tekshirib, “ruthless review” qilaman. Qaysi vazifani birinchi qilib olamiz?
