# Exode Platform backendini qurish va o'rganish yo'l xaritasi

Bu fayl Exode.biz clone loyihasini FastAPI bilan qurish jarayonida nimalarni o'rganish, qaysi texnologiyalarni qanday ulash va uyga vazifa uchun qanday dokumentatsiya tayyorlash kerakligini bosqichma-bosqich tushuntiradi.

## 1. Asosiy maqsad

Loyihani shunchaki ko'chirib yozish emas, balki qurish jarayonida quyidagi ko'nikmalarni egallash kerak:

- FastAPI'da katta backendni modullarga bo'lib qurish.
- JWT authentication va role-based authorization qilish.
- Docker orqali loyihani bir xil muhitda ishga tushirish.
- Redis va Celery orqali background tasklar yozish.
- To'lovdan keyin kursga avtomatik access berish.
- Kurs ichida guruh chat va online videochat funksiyasini loyihalash.
- Video darslarni tashqi bepul storage/CDN servisga yuklash.
- Swagger va Postman dokumentatsiya tayyorlash.

## 2. O'rganish strategiyasi

Har bir katta modul uchun quyidagi 4 bosqichli usuldan foydalan:

1. **Mini nazariya** — modul nima uchun kerakligini 20-40 daqiqa o'rgan.
2. **Kichik tajriba** — alohida kichik faylda yoki demo endpointda sinab ko'r.
3. **Asosiy loyihaga ulash** — ishlagan yechimni `app/modules/...` ichiga ko'chir.
4. **Dokumentatsiya va test** — Swagger, Postman, README va pytest bilan tekshir.

Misol: JWT o'rganishda avval token nima ekanini tushun, keyin demo login yoz, keyin loyihadagi `auth` moduliga ulab, Swagger orqali login qilib ko'r.

## 3. Tavsiya etilgan ketma-ketlik

| Bosqich | Nima quriladi | Nima o'rganiladi | Natija |
| --- | --- | --- | --- |
| 1 | Project skeleton | FastAPI structure, settings | server ishga tushadi |
| 2 | Docker setup | Dockerfile, compose, volumes | backend/db/redis containerda ishlaydi |
| 3 | Auth | `python-jose`, JWT, password hash | register/login/token ishlaydi |
| 4 | Roles & schools | RBAC, tenant filter | owner/admin/student ajraladi |
| 5 | Courses | CRUD, relationships | course/module/lesson yaratiladi |
| 6 | Video storage | file upload, external URL | video metadata saqlanadi |
| 7 | Products & payments | invoice, fake webhook | to'lovdan keyin access ochiladi |
| 8 | Learning progress | progress calculation | dars tugashi hisoblanadi |
| 9 | Group chat | WebSocket, messages | kurs o'quvchilari suhbatlashadi |
| 10 | Online videochat | room, schedule, join link | kurs egasi live dars qiladi |
| 11 | Redis/Celery | background jobs | notification, export, cleanup ishlaydi |
| 12 | Docs | Swagger, Postman | topshiriq dokumentatsiyasi tayyor bo'ladi |

## 4. FastAPI project structure

```text
fastapi/exode_platform/
  app/
    main.py
    core/
      config.py
      security.py
      permissions.py
    db/
      base.py
      session.py
    modules/
      auth/
      users/
      schools/
      courses/
      lessons/
      products/
      payments/
      access/
      chat/
      videochat/
      notifications/
      storage/
    workers/
      celery_app.py
      tasks.py
  tests/
  docker-compose.yml
  Dockerfile
  .env.example
  postman/
    exode_platform.postman_collection.json
  README.md
```

## 5. JWT authentication: `python-jose`

Uyga vazifada JWT uchun `python-jose` ishlatish kerak. Kerakli kutubxonalar:

```bash
pip install "python-jose[cryptography]" passlib[bcrypt] python-multipart
```

O'rganiladigan mavzular:

- Access token va refresh token farqi.
- JWT payload ichida `sub`, `exp`, `type`, `school_id`, `role` saqlash.
- `OAuth2PasswordBearer` orqali protected endpoint qilish.
- Parolni hech qachon plain text saqlamaslik, `bcrypt` hash ishlatish.

Minimal mantiq:

1. `POST /api/v1/auth/register` user yaratadi.
2. `POST /api/v1/auth/login` email/parolni tekshiradi.
3. Backend `python-jose` bilan access va refresh token yaratadi.
4. Protected endpoint `Authorization: Bearer <token>` kutadi.
5. Token ichidagi `sub` orqali user DBdan topiladi.
6. Role tekshirilib, ruxsat beriladi yoki `403` qaytariladi.

## 6. Docker bilan ishlash

Docker loyiha har kimda bir xil ishga tushishi uchun kerak. Minimal compose servislar:

- `api` — FastAPI app.
- `postgres` — asosiy database.
- `redis` — cache, broker, rate limit.
- `worker` — Celery background worker.

O'rganish rejasi:

1. Dockerfile nima ekanini tushun.
2. `docker-compose.yml` ichida servislar, portlar, environment va volumes yozishni o'rgan.
3. Avval faqat FastAPI + Postgres ishga tushir.
4. Keyin Redis qo'sh.
5. Oxirida Celery worker qo'sh.

Uyga vazifa uchun kerakli komandalar READMEda bo'lishi kerak:

```bash
docker compose up --build
alembic upgrade head
pytest
```

## 7. Redis nima uchun kerak bo'ladi

Redis quyidagi ishlar uchun ishlatiladi:

- Celery broker sifatida.
- Login rate limit: bir IP ko'p noto'g'ri login qilsa vaqtincha bloklash.
- Online foydalanuvchilar va WebSocket connection holatini saqlash.
- Tez-tez so'raladigan analitika cache.
- OTP yoki password reset tokenni qisqa muddatga saqlash.

Boshlanish uchun Redisni Celery broker sifatida ishlatish yetarli:

```text
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

## 8. Celery bilan background tasklar

Celery asosiy requestni sekinlashtirmasdan og'ir ishlarni orqada bajaradi.

Bu loyihada Celery tasklar:

- To'lovdan keyin email/Telegram notification yuborish.
- Video upload qilingandan keyin metadata tekshirish yoki thumbnail yaratish.
- Sertifikat PDF generatsiya qilish.
- Analitika report/export tayyorlash.
- Subscription muddati tugagan userlarni accessdan chiqarish.
- Webhooklarni tashqi CRMga qayta yuborish.

O'rganish tartibi:

1. Oddiy `send_test_email.delay(user_id)` task yoz.
2. Worker logida task ishlaganini ko'r.
3. Keyin payment webhookdan keyin notification task chaqir.
4. Keyin periodic task uchun Celery Beat yoki cron qo'sh.

## 9. Kurs uchun Telegramga o'xshash guruh chat

Talab: har bir kurs uchun platformaning o'zida alohida suhbat guruhi bo'lishi kerak. Bu Telegram groupga o'xshaydi, lekin platforma ichida ishlaydi.

Backend modeli:

- `course_groups`: `id`, `school_id`, `course_id`, `title`, `created_by`.
- `course_group_members`: `group_id`, `user_id`, `role`, `joined_at`, `muted_until`.
- `group_messages`: `group_id`, `sender_id`, `text`, `file_url`, `created_at`, `edited_at`, `deleted_at`.
- `message_reads`: `message_id`, `user_id`, `read_at`.

Mantiq:

1. Kurs publish bo'lganda yoki birinchi o'quvchi sotib olganda `course_group` yaratiladi.
2. O'quvchi kursni sotib olsa, shu kurs groupiga avtomatik qo'shiladi.
3. Kurs egasi, mentor va admin group moderatorlari bo'ladi.
4. Faqat accessi bor o'quvchi groupga kira oladi.
5. Access tugasa user groupdan chiqariladi yoki read-only bo'ladi.
6. Real-time xabar uchun FastAPI WebSocket ishlatiladi.
7. Redis WebSocket session va pub/sub uchun ishlatilishi mumkin.

Endpointlar:

| Method | URL | Vazifa |
| --- | --- | --- |
| GET | `/api/v1/courses/{course_id}/group` | kurs groupini olish |
| GET | `/api/v1/groups/{group_id}/messages` | xabarlar tarixi |
| POST | `/api/v1/groups/{group_id}/messages` | xabar yuborish |
| WS | `/ws/groups/{group_id}` | real-time chat |

## 10. Kurs egasi belgilangan vaqtda online videochat qilishi

Talab: kurs egasi kursni sotib olgan o'quvchilar bilan belgilangan vaqtda online videochat o'tkazadi.

Bu funksiya 2 xil yo'l bilan qilinadi:

### 10.1 Oddiy va tez variant: tashqi video room link

MVP uchun eng oson yo'l:

- Google Meet, Zoom, Jitsi yoki Daily.co room linki saqlanadi.
- Backend faqat schedule, qatnashchilar va accessni boshqaradi.
- O'quvchi vaqti kelganda `join_url` oladi.

Afzalligi: tez, WebRTC murakkabligini kamaytiradi.

### 10.2 Platforma ichida WebRTC/Jitsi embed

Keyingi bosqichda Jitsi Meet embed yoki self-hosted Jitsi ishlatish mumkin. Backend room yaratish, JWT room token va qatnashchilarni boshqaradi.

Backend modeli:

- `live_sessions`: `id`, `school_id`, `course_id`, `host_id`, `title`, `starts_at`, `ends_at`, `provider`, `room_url`, `status`.
- `live_session_participants`: `session_id`, `user_id`, `role`, `joined_at`, `left_at`.
- `live_session_records`: `session_id`, `recording_url`, `duration`.

Mantiq:

1. Kurs egasi `live_session` yaratadi va vaqt belgilaydi.
2. Backend faqat shu kursni sotib olganlarga notification yuboradi.
3. Dars vaqtidan 10-15 daqiqa oldin join tugmasi ochiladi.
4. `GET /live-sessions/{id}/join` user accessini tekshiradi.
5. Access bor bo'lsa room URL yoki token qaytariladi.
6. Sessiya tugagach recording URL dars materialiga qo'shilishi mumkin.

Endpointlar:

| Method | URL | Vazifa |
| --- | --- | --- |
| POST | `/api/v1/courses/{course_id}/live-sessions` | live dars yaratish |
| GET | `/api/v1/courses/{course_id}/live-sessions` | kurs live darslari |
| GET | `/api/v1/live-sessions/{id}/join` | videochatga kirish linki/tokeni |
| POST | `/api/v1/live-sessions/{id}/finish` | sessiyani yakunlash |

## 11. Video darslarni saqlash uchun bepul servis tanlash

Talab: videolarni aynan video saqlashga mo'ljallangan, ko'p joy/resurs beradigan va bepul servisda saqlash.

Haqiqat: katta video hosting odatda pullik bo'ladi. Shuning uchun homework/MVP uchun bepul planli servisdan boshlash, productionda pullik storagega o'tish kerak.

Tavsiya etilgan variantlar:

| Servis | Nima uchun | Cheklov |
| --- | --- | --- |
| YouTube Unlisted | juda katta bepul video hosting, embed oson | maxfiylik to'liq emas, branding YouTube |
| Vimeo free/basic | video uchun mo'ljallangan | free limit kam bo'lishi mumkin |
| Cloudinary free | video upload API bor, transform mumkin | free quota cheklangan |
| Firebase Storage/Supabase Storage free | file storage oson | video streaming optimizatsiyasi cheklangan |
| Jitsi recording + external storage | live dars recording uchun | storage alohida kerak |

Uyga vazifa uchun eng amaliy yechim:

1. Video darslar uchun **YouTube Unlisted** ishlat.
2. DBda `video_provider='youtube'`, `video_url`, `embed_url`, `duration`, `thumbnail_url` saqla.
3. Agar upload API shart bo'lsa, **Cloudinary free** bilan demo upload qil.
4. Storage servisini abstraksiya qil: keyin YouTube/Cloudinary/S3 almashtirish oson bo'lsin.

Backendda `VideoAsset` modeli bo'ladi:

```text
VideoAsset(id, school_id, lesson_id, provider, original_url, embed_url, duration_seconds, thumbnail_url, status)
```

Muhim xavfsizlik qoidasi: faqat kurs accessi bor o'quvchiga embed URL ko'rsat. Lekin YouTube Unlisted link tarqalib ketishi mumkinligini READMEda yozib qo'y.

## 12. Swagger dokumentatsiya

FastAPI avtomatik Swagger beradi:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

Uyga vazifa uchun quyidagilarni qilish kerak:

- Har endpointga `summary`, `description`, `response_model`, `tags` yoz.
- Pydantic schema'larda `Field(..., examples=[...])` ishlat.
- Auth endpointlarda Bearer token ishlashini Swaggerda ko'rsat.
- READMEda `/docs` va `/openapi.json` linklarini yoz.
- OpenAPI JSONni export qilib saqlash mumkin:

```bash
curl http://localhost:8000/openapi.json -o docs/openapi.json
```

## 13. Postman dokumentatsiya

Postman uchun collection va environment tayyorlash kerak.

Folderlar:

```text
postman/
  exode_platform.postman_collection.json
  exode_platform.local.postman_environment.json
```

Collection ichida bo'ladigan bo'limlar:

1. Auth: register, login, refresh.
2. Schools: create school, my schools.
3. Courses: CRUD, modules, lessons.
4. Products & Payments: product, invoice, fake webhook.
5. Learning: my courses, complete lesson, submit practice.
6. Chat: group messages, websocket eslatma.
7. Live sessions: create schedule, join link.
8. Analytics: dashboard.

Postmanda login requestdan keyin access tokenni avtomatik environmentga yozish uchun `Tests` script qo'shiladi:

```javascript
const json = pm.response.json();
pm.environment.set("access_token", json.payload.access_token);
```

Keyingi requestlarda header:

```text
Authorization: Bearer {{access_token}}
```

## 14. Uyga vazifa uchun minimal demo flow

Topshiriqni ko'rsatishda quyidagi ketma-ketlikni ishlat:

1. `docker compose up --build` bilan loyihani ishga tushir.
2. Swagger `/docs` ochilganini ko'rsat.
3. Owner register/login qiladi.
4. Owner school yaratadi.
5. Owner course, module, lesson yaratadi.
6. Owner YouTube unlisted video URLni lesson video sifatida qo'shadi.
7. Owner product yaratadi va course bilan bog'laydi.
8. Student register/login qiladi.
9. Student invoice yaratadi.
10. Fake payment webhook invoice'ni `paid` qiladi.
11. Student kursga access oladi.
12. Student course group chatga avtomatik qo'shiladi.
13. Owner live session schedule qiladi.
14. Student join link oladi.
15. Student darsni tugatadi va progress yangilanadi.
16. Postman collectionda shu flow ishlayotganini ko'rsat.

## 15. Har hafta uchun o'quv rejasi

### 1-hafta: FastAPI, Docker, DB

- FastAPI router, dependency, schema, response model.
- Dockerfile va docker-compose.
- Postgres va Alembic migration.
- Natija: authsiz school/course CRUD.

### 2-hafta: Auth va role

- `python-jose` JWT.
- Password hashing.
- RBAC va `school_id` tenant filter.
- Natija: owner/admin/student rollari bilan protected endpointlar.

### 3-hafta: Course, lesson, video storage

- Course/module/lesson relational model.
- YouTube/Cloudinary video asset modeli.
- Lesson progress.
- Natija: student accessi bo'lsa video darsni ko'radi.

### 4-hafta: Payment va access

- Product, invoice, payment webhook.
- Fake payment provider.
- Idempotency.
- Natija: to'lovdan keyin kurs ochiladi.

### 5-hafta: Chat, live session, Redis

- WebSocket chat.
- Course group membership.
- Live session scheduling.
- Redis pub/sub yoki connection state.
- Natija: kurs ichida suhbat va videochat link.

### 6-hafta: Celery, analytics, docs

- Celery notification/export tasklari.
- Dashboard statistikasi.
- Swagger descriptions.
- Postman collection.
- Natija: loyiha topshirishga tayyor.

## 16. Qaysi narsani chuqur, qaysini MVP qilish kerak

Chuqur o'rgan:

- FastAPI dependency injection.
- SQLAlchemy relationship va migration.
- JWT security.
- Docker compose.
- Payment webhook idempotency.

MVP darajasida qil:

- Real payment o'rniga fake provider.
- Videochat uchun Jitsi/Google Meet link.
- Video storage uchun YouTube Unlisted URL.
- Celeryda 2-3 ta real task.
- Chatda oddiy text message.

Keyin rivojlantirish:

- Real Payme/Click integration.
- Cloudinary/S3 upload.
- Jitsi JWT yoki Daily.co API.
- Redis pub/sub bilan multi-instance chat.
- Celery Beat bilan periodic billing.
