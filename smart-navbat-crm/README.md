# Smart Navbat CRM

Kichik xizmat ko'rsatish bizneslari (o'quv markazlari, shifokorlar, salonlar,
avtoyuvish) uchun Telegram va Web orqali ishlaydigan avtomatik
qabul/navbat (booking) tizimi va CRM. Bu papka "Eng Daromadli B2B
Web-Loyiha" deep-research hisobotidagi g'oyaning MVP (Minimal Viable
Product) ko'rinishidagi kodga aylantirilgan holati.

## Arxitektura

Hisobotdagi taqsimotga mos ravishda ikkita xizmatdan iborat:

- **`backend/` (Django + DRF)** — biznes egasi uchun CRM/boshqaruv paneli
  (hozircha Django admin orqali — har bir biznes egasi faqat o'z
  `Tenant`iga tegishli xizmatlar/xodimlar/mijozlar/navbatlarni ko'radi va
  boshqaradi) va mijozlar uchun ochiq (public) booking REST API.
- **`bot_service/` (FastAPI)** — Telegram webhook qabul qiluvchi xizmat.
  Mijoz bilan qisqa suhbat orqali (xizmat -> kun -> bo'sh vaqt -> ism)
  navbatga yozadi, buning uchun Django'ning public API'siga murojaat
  qiladi va tasdiqlash xabarini Telegram orqali yuboradi.
- **PostgreSQL** — asosiy ma'lumotlar bazasi (lokal ishlab chiqishda
  `POSTGRES_DB` o'rnatilmasa, Django avtomatik SQLite'ga tushadi).

Ma'lumotlar modeli hisobotdagi rejaga mos: `Tenant` (biznes), `Service`
(xizmat turi), `Employee` (xodim/usta), `Client` (mijoz) va `Appointment`
(navbat) — har bir `Appointment` qat'iy ravishda bitta `Tenant`ga va bitta
`Client`ga bog'langan (multi-tenancy shared-schema modeli, tenant_id bilan
ajratilgan — kichik SaaS uchun eng arzon va oddiy yondashuv).

## MVP funksiyalari (hisobotga mos)

1. Biznes egasi Django admin orqali o'z xizmatlari va xodimlarini kiritadi.
2. Mijozlar uchun yagona booking havolasi: `POST/GET /api/public/<slug>/...`
   — buni Instagram bio'ga qo'yiladigan oddiy web-sahifa yoki Telegram bot
   iste'mol qiladi.
3. Navbat yaratilganda mijoz va (agar biriktirilgan bo'lsa) xodimga
   avtomatik Telegram xabarnomasi yuboriladi (`bookings/services.py`).

Qoldirilgan (post-MVP): moliyaviy hisobotlar, xodimlar KPI, ombor nazorati,
Payme/Click integratsiyasi (`Tenant.plan` maydoni narxlash uchun tayyor,
lekin to'lov provayderi ulanmagan).

## Lokal ishga tushirish

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

```bash
cd bot_service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_API_BASE_URL=http://localhost:8000/api
uvicorn main:app --reload --port 8001
```

Yoki hammasini birga: `docker compose up --build` (avval `.env.example`ni
`.env`ga nusxalang).

Telegram bot webhookini ulash uchun (bot_service ochiq internetdan
yetish mumkin bo'lgandan so'ng):

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<domain>/webhook/<tenant-slug>
```

## Public API qisqacha

- `GET  /api/public/<slug>/services/` — faol xizmatlar ro'yxati
- `GET  /api/public/<slug>/availability/?service=<id>&date=YYYY-MM-DD` — bo'sh vaqtlar
- `POST /api/public/<slug>/book/` — navbat yaratish (`service`, `start_time`, `client: {full_name, telegram_user_id?}`)

## Ma'lum cheklovlar (MVP)

- Ish vaqti hozircha qat'iy 09:00–20:00 (`bookings/services.py`); tenant
  bo'yicha moslashuvchan jadval keyingi bosqich.
- Xodim biriktirilmagan (`employee=None`) navbatlar uchun qo'sh-band
  qilishdan himoya yo'q — production uchun har bir navbatga xodim
  biriktirish yoki tenant darajasida qo'shimcha unique-constraint tavsiya
  etiladi.
- Bot suhbat holati xotirada saqlanadi (`bot_service/state.py`) — ko'p
  nusxali (replica) joylashtirishda Redisga o'tkazish kerak.
