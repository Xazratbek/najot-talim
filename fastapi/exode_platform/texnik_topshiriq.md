# Exode.biz clone backendi uchun texnik topshiriq (FastAPI)

## 1. Loyiha maqsadi

`exode.biz` — onlayn maktablar, ekspertlar, prodyuserlar, repetitorlar va korporativ ta'lim jamoalari uchun EdTech SaaS platformasi. Backend vazifasi: maktab yaratish, kurslarni sotish, o'quv jarayonini yuritish, to'lovlardan keyin avtomatik kirish berish, amaliyotlarni tekshirish, chat, analitika, sertifikat va integratsiyalarni bitta tizimda boshqarish.

## 2. Asosiy foydalanuvchi rollari

| Rol | Maqsadi | Asosiy huquqlar |
| --- | --- | --- |
| Super admin | Butun platformani boshqaradi | barcha maktablar, tariflar, billing, moderatsiya |
| Maktab egasi | O'z online maktabini boshqaradi | brending, domen, kurs, xodim, to'lov, analitika |
| Admin/manager | Operatsion boshqaruv | o'quvchi, guruh, buyurtma, xabar, hisobot |
| Mentor/kurator | O'quv jarayonini kuzatadi | uy vazifasini tekshirish, fikr bildirish, chat |
| O'qituvchi | Kurs kontentini yaratadi | modul, dars, test, topshiriq, material |
| O'quvchi | Kursni sotib olib o'qiydi | dars ko'rish, test yechish, vazifa topshirish, chat |
| Korporativ HR | Xodimlarni o'qitadi | xodim, bo'lim, lavozim, kurs tayinlash, attestatsiya |
| API servis foydalanuvchisi | Tashqi tizim integratsiyasi | token orqali user, group, course, access, webhook ishlatish |

## 3. MVP chegarasi

MVP FastAPI backend quyidagilarni qamrab oladi:

1. Ko'p maktabli SaaS arxitekturasi (`school_id` orqali tenant ajratish).
2. JWT autentifikatsiya va RBAC ruxsatlar.
3. Maktab profili, brending va sozlamalar.
4. Kurs katalogi, mahsulot va narxlar.
5. Kurs konstruktori: modul, dars, video/text/test/topshiriq.
6. O'quvchi ro'yxatdan o'tishi va kurs sotib olishi.
7. To'lov invoice modeli va payment provider webhooklari uchun endpointlar.
8. To'lovdan keyin mahsulot/kursga avtomatik access berish.
9. Uy vazifasi va test natijalari.
10. Guruhlar va korporativ xodimlarni kursga biriktirish.
11. Ichki messengerning minimal varianti.
12. Analitika uchun agregat endpointlar.
13. Sertifikat generatsiyasi uchun ma'lumot modeli.
14. REST API dokumentatsiyasi va webhook eventlari.

## 4. Funksional talablar

### 4.1 Autentifikatsiya va foydalanuvchilar

- Email/telefon + parol orqali ro'yxatdan o'tish.
- Login, refresh token, logout.
- Parolni tiklash uchun token modeli.
- Profil: ism, familiya, avatar, telefon, email, tug'ilgan sana, til.
- Bitta foydalanuvchi bir nechta maktabga ulanadi.
- Har maktab ichida alohida rol va status saqlanadi.
- API servis tokenlari alohida jadvalda saqlanadi.

### 4.2 Maktab va kastomizatsiya

- Maktab nomi, slug, logo, favicon, ranglar, kontaktlar.
- Custom domen maydoni va domen verifikatsiya statusi.
- Til, valuta, vaqt zonasi, huquqiy matnlar.
- Landing/katalog ko'rinishi uchun sozlamalar.
- Xodimlarni taklif qilish va ruxsatlar berish.

### 4.3 Kurs konstruktori

- Kurs: nom, tavsif, cover, daraja, davomiylik, status (`draft`, `published`, `archived`).
- Modul: tartib raqami, nom, unlock sharti.
- Dars: video, longread/text, fayl, test, amaliy topshiriq turlari.
- Dars ochilish qoidalari: ketma-ket, sana bo'yicha, to'lov bosqichi bo'yicha.
- Preview darslar va yopiq darslar.
- Kursni ko'paytirish, draft/publish jarayoni.

### 4.4 Testlar va uy vazifalari

- Savol turlari: single choice, multiple choice, text answer, matching, fill gaps, ordering.
- Avto-tekshirish: variantli savollarni avtomatik baholash.
- Qo'lda tekshirish: mentor izohi, ball, qayta topshirishga ruxsat.
- Deadline, maksimal urinishlar, minimal o'tish bali.
- Attempt tarixi va progressga ta'siri.

### 4.5 Mahsulot, sotuv va to'lov

- Product modeli: bitta yoki bir nechta kursni sotiladigan paketga bog'lash.
- Narxlar: bir martalik, obuna, bo'lib-bo'lib to'lash.
- Promokod/chegirma va UTM manbalar.
- Invoice yaratish, statuslar: `pending`, `paid`, `failed`, `cancelled`, `refunded`.
- Providerlar: Payme, Click, Uzum, Visa/Mastercard uchun abstrakt adapter.
- Webhook qabul qilish, imzoni tekshirish, idempotency.
- To'lov muvaffaqiyatli bo'lsa, access avtomatik beriladi.
- Obuna uchun keyingi yechib olish sanasi va auto-debit statusi saqlanadi.

### 4.6 Access va o'qish progressi

- ProductAccess: user, product, course, start/end date, status.
- Dars ko'rildi, test topshirildi, vazifa topshirildi holatlari.
- Kurs progress foizi.
- Sertifikat olish sharti: progress 100% va minimal ball.
- Kirish muddati tugasa darslar yopiladi.

### 4.7 Guruhlar va korporativ ta'lim

- Guruh yaratish, o'quvchilarni qo'shish/o'chirish.
- HR uchun xodim profili: bo'lim, lavozim, daraja, rahbar.
- Kursni guruhga yoki bo'limga tayinlash.
- Onboarding, attestatsiya va compliance kurslari.
- Xodim statuslari: boshlamagan, jarayonda, tugatgan.

### 4.8 Messenger va bildirishnomalar

- Maktab ichida chat: user-mentor, guruh chati, announcement.
- Xabar turlari: text, file, system notification.
- O'qildi/o'qilmadi statuslari.
- Email/Telegram/push bildirishnomalar uchun notification queue.
- To'lov, access, vazifa tekshirildi, deadline eslatmalari.

### 4.9 Marketing va sotuv vositalari

- UTM parametrlarini buyurtma va ro'yxatdan o'tishda saqlash.
- Pixel/integration config: Meta Pixel, Google Analytics, Yandex Metrica kabi kalitlar.
- Tripwire/lead magnet mahsulot turi.
- Mailing segmentlari: kurs, progress, xarid statusi bo'yicha.
- Sales funnel: tashrif, kurs ochish, savatcha, to'lov metrikalari.

### 4.10 Analitika va hisobot

- Dashboard metrikalari: o'quvchilar soni, faol userlar, tugatganlar, sertifikatlar.
- Daromad: oylar bo'yicha, kurslar bo'yicha, provider bo'yicha.
- Progress: kurs/guruh/user kesimida.
- NPS va fikrlar modeli.
- Export: CSV/XLSX/JSON uchun asinxron job.
- API endpointlar paginatsiya, filter va sort bilan ishlaydi.

### 4.11 Mobil ilova uchun API

- Maktab tanlash va maktablar ro'yxati.
- O'quvchining kurslari, davom ettirish bloki.
- Dars kontenti, test, vazifa yuborish.
- Chat va notificationlar.
- Gamifikatsiya: ball, reyting, badge.

### 4.12 Tashqi API va webhooklar

- Base prefix: `/api/v1`.
- Har so'rovda tenant konteksti: `X-School-Id` yoki token orqali.
- Webhook eventlari: `user.created`, `invoice.paid`, `access.granted`, `course.completed`, `practice.checked`.
- API javob formati yagona bo'ladi: `{ "success": true, "code": "OK", "payload": ... }`.
- Rate limit va audit log qo'shiladi.

## 5. Ma'lumotlar bazasi modeli

Asosiy jadvallar:

- `users`, `profiles`, `sessions`, `password_reset_tokens`
- `schools`, `school_memberships`, `roles`, `permissions`
- `staff_invites`, `api_tokens`, `audit_logs`
- `courses`, `course_modules`, `course_lessons`, `lesson_contents`
- `questions`, `question_options`, `practice_tasks`, `practice_attempts`
- `products`, `product_courses`, `product_prices`, `discounts`
- `invoices`, `payments`, `subscriptions`, `installment_plans`
- `product_accesses`, `lesson_progresses`, `course_progresses`, `certificates`
- `groups`, `group_members`, `employees`, `departments`, `positions`
- `chats`, `chat_members`, `messages`, `notifications`
- `utm_events`, `pixel_configs`, `mailing_campaigns`
- `webhook_endpoints`, `webhook_deliveries`, `export_jobs`

## 6. Tavsiya etilgan FastAPI arxitekturasi

```text
exode_platform/
  app/
    main.py
    core/          # config, security, dependencies
    db/            # session, base, migrations
    modules/
      auth/
      users/
      schools/
      courses/
      learning/
      sales/
      payments/
      access/
      groups/
      messenger/
      analytics/
      integrations/
    common/        # pagination, response schema, exceptions
  tests/
  alembic/
  pyproject.toml
  README.md
```

Texnologiyalar:

- FastAPI, Pydantic v2.
- PostgreSQL, SQLAlchemy 2.0 async, Alembic.
- Redis + Celery/RQ yoki FastAPI background tasks.
- S3-compatible storage uchun video/fayl metadata.
- JWT access/refresh token.
- Pytest + HTTPX.

## 7. Muhim endpointlar namunasi

| Method | URL | Vazifa |
| --- | --- | --- |
| POST | `/api/v1/auth/register` | user yaratish |
| POST | `/api/v1/auth/login` | token olish |
| GET | `/api/v1/schools/me` | user ulangan maktablar |
| POST | `/api/v1/schools` | maktab yaratish |
| POST | `/api/v1/courses` | kurs yaratish |
| POST | `/api/v1/courses/{id}/modules` | modul qo'shish |
| POST | `/api/v1/modules/{id}/lessons` | dars qo'shish |
| POST | `/api/v1/products` | sotiladigan paket yaratish |
| POST | `/api/v1/invoices` | to'lov invoice yaratish |
| POST | `/api/v1/payments/{provider}/webhook` | provider webhooki |
| GET | `/api/v1/me/courses` | o'quvchi kurslari |
| POST | `/api/v1/lessons/{id}/complete` | darsni tugatish |
| POST | `/api/v1/practices/{id}/attempts` | uy vazifa yuborish |
| PUT | `/api/v1/practice-attempts/{id}/check` | mentor tekshirishi |
| GET | `/api/v1/analytics/dashboard` | dashboard statistikasi |
| POST | `/api/v1/webhooks` | tashqi webhook sozlash |

## 8. Nofunksional talablar

- Har tenant ma'lumotlari qat'iy ajratiladi.
- Payment webhooklar idempotent ishlashi shart.
- Barcha muhim harakatlar audit logga yoziladi.
- Paginatsiya default 20, max 100.
- Video/fayllar DBda emas, storage havolasi sifatida saqlanadi.
- Soft delete muhim biznes obyektlarda qo'llanadi.
- API OpenAPI orqali hujjatlanadi.
- Test coverage MVP uchun kamida 60%.

## 9. Qabul qilish mezonlari

- Maktab egasi kurs yaratib publish qila oladi.
- O'quvchi mahsulot uchun invoice yaratib, webhook simulyatsiyasidan keyin kursga kira oladi.
- O'quvchi darsni tugatib, test yoki uy vazifasini yubora oladi.
- Mentor uy vazifasini baholaydi va progress yangilanadi.
- Admin dashboardda daromad, progress va faol userlarni ko'radi.
- API swagger hujjatida barcha endpointlar ko'rinadi.
