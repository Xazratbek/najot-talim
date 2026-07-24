# Exode.biz imkoniyatlari va backend mantiqiy tahlili

Ushbu hujjat `exode.biz` saytida ko'rinadigan funksiyalarni backend nuqtai nazaridan tushuntiradi. Maqsad — FastAPI orqali clone backendini qurishda har bir imkoniyat ortidagi biznes mantiqni aniq ko'rish.

## 1. Platforma g'oyasi

Exode bitta platformada bir nechta turdagi mijozga xizmat qiladi: online maktab, korporativ ta'lim, prodyuser/ekspert, repetitor. Shuning uchun backend oddiy kurs sayti emas, balki ko'p tenantli SaaS bo'lishi kerak. Har bir maktab alohida brend, katalog, xodimlar, kurslar, o'quvchilar va to'lovlarga ega bo'ladi.

Mantiq:

1. Foydalanuvchi platformaga kiradi.
2. U bitta yoki bir nechta maktabga ulangan bo'lishi mumkin.
3. Tanlangan maktab kontekstida kurslar, chatlar, accesslar va rollar ishlaydi.
4. Backend har doim `school_id` orqali ma'lumotlarni filtrlaydi.

## 2. Onlayn maktab yaratish

Saytdagi "maktab yaratish va sozlash" funksiyasi backendda `School` obyektidan boshlanadi. Maktab egasi nom, slug, logo, ranglar, kontaktlar va domenni sozlaydi.

Logik oqim:

1. User ro'yxatdan o'tadi.
2. `POST /schools` orqali yangi maktab ochadi.
3. Userga shu maktabda `owner` roli beriladi.
4. Default sozlamalar, default katalog va default rollar yaratiladi.
5. Keyin owner xodimlarni taklif qiladi va kurslarni qo'shadi.

## 3. Kurs konstruktori

Kurs konstruktori video, matn, test va topshiriqlarni vizual tartibda yig'ishga imkon beradi. Backendda bu iyerarxiya ko'rinishida quriladi:

`Course -> Module -> Lesson -> LessonContent / Practice / Quiz`

Logik qoidalar:

- Kurs `draft` bo'lsa, o'quvchilar ko'rmaydi.
- `published` bo'lsa, katalogda chiqadi yoki access bo'lsa ochiladi.
- Modul va darslarda `position` maydoni bo'ladi.
- Darslar ketma-ket ochilishi yoki bir vaqtning o'zida ochilishi mumkin.
- Video faylning o'zi storage'da, DBda faqat URL va metadata saqlanadi.

## 4. Uy vazifalari va testlar

Saytda testlar, topshiriqlar va avto-tekshirish aytilgan. Bu ikkita mantiqni talab qiladi:

1. Avtomatik tekshiriladigan savollar: variant tanlash, moslashtirish, bo'sh joy to'ldirish, tartiblash.
2. Mentor tekshiradigan savollar: matnli javob, fayl yuklash, loyiha topshirish.

Logik oqim:

1. O'quvchi attempt yaratadi.
2. Backend javoblarni saqlaydi.
3. Agar savollar avto-tekshirilsa, ball darhol hisoblanadi.
4. Agar qo'lda tekshirish kerak bo'lsa, attempt `waiting_review` bo'ladi.
5. Mentor ball va izoh yozadi.
6. Natija lesson/course progressga ta'sir qiladi.

## 5. To'lovlarni qabul qilish

Exode Payme, Click, Uzum, Mastercard/Visa kabi providerlarni ko'rsatadi. Backendda providerlar umumiy `PaymentProvider` interfeysi ostida ishlashi kerak.

Logik oqim:

1. O'quvchi mahsulotni tanlaydi.
2. Backend `Invoice` yaratadi.
3. Frontend provider checkout sahifasiga o'tkazadi.
4. Provider webhook yuboradi.
5. Backend webhook imzosini tekshiradi.
6. Invoice `paid` bo'ladi.
7. `ProductAccess` avtomatik yaratiladi.
8. O'quvchiga notification yuboriladi.

Muhim qoida: webhook qayta-qayta kelishi mumkin, shuning uchun `provider_transaction_id` bo'yicha idempotency shart.

## 6. Bo'lib-bo'lib to'lash va obuna

Saytda auto-debit, bosqichma-bosqich kirish va takroriy to'lovlar bor. Bu oddiy invoice'dan murakkabroq model talab qiladi.

Logik variantlar:

- Obuna: har oy avtomatik yechim; to'lov bo'lmasa access to'xtaydi.
- Installment: kurs qismlari to'lov bosqichlariga qarab ochiladi.
- Club/community: obuna faol bo'lsa Telegram yoki platforma jamoasiga kirish saqlanadi.

Backendda `Subscription`, `InstallmentPlan`, `AccessPolicy` modellarini ajratish kerak.

## 7. Telegram jamoani monetizatsiya qilish

Saytda Telegram bot orqali yopiq kanal/chatga avtomatik ruxsat berish ko'rsatilgan.

Logik oqim:

1. Maktab Telegram bot tokenini ulaydi.
2. Product Telegram channel/chat bilan bog'lanadi.
3. To'lov muvaffaqiyatli bo'lganda access yaratiladi.
4. Background job Telegram API orqali userni kanalga qo'shadi yoki invite link beradi.
5. Obuna tugasa, user kanaldan chiqariladi yoki invite bekor qilinadi.

## 8. Analitika

Saytda progress, daromad, faollik, top kurslar, NPS va sotuv voronkasi ko'rinadi. Backend real vaqt va agregat ma'lumotlarni birlashtirishi kerak.

Asosiy metrikalar:

- O'quvchi progressi: user/course/group kesimida foiz.
- Daromad: paid invoice summasi, oy va kurs bo'yicha.
- Faollik: login, dars ko'rish, vazifa topshirish eventlari.
- Top kurslar: daromad yoki o'quvchi soni bo'yicha.
- Funnel: tashrif -> kurs ochildi -> savatcha/invoice -> to'lov.
- NPS: o'quvchi fikrlaridan hisoblanadi.

Mantiq: muhim harakatlar `events` yoki audit logga yozilsa, keyin dashboard uchun agregatsiya osonlashadi.

## 9. Korporativ ta'lim va HR

Saytda HR Academy, Sales School, Tech Onboarding, Compliance kabi korporativ holatlar bor. Bu B2B ta'lim uchun xodim modeli kerakligini bildiradi.

Logik oqim:

1. HR admin xodimlarni import qiladi yoki yaratadi.
2. Xodimlarga bo'lim, lavozim, daraja, rahbar belgilanadi.
3. Kurslar bo'lim yoki guruhga tayinlanadi.
4. Backend har xodim uchun progress yaratadi.
5. HR dashboardda boshlamagan, jarayonda, tugatgan xodimlarni ko'radi.
6. Attestatsiya natijalari sertifikat yoki compliance statusga ta'sir qiladi.

## 10. Messenger

Platforma ichidagi messenger o'quvchi va mentorlarni bog'laydi.

Mantiq:

- Chat maktab doirasida yaratiladi.
- Chat turi: individual, guruh, announcement.
- Xabar muallifi va o'qilgan status saqlanadi.
- Tizim xabarlari avtomatik yaratiladi: "kursga kirish ochildi", "uy vazifasi tekshirildi".
- Notification queue push/email/telegram jo'natishni alohida bajaradi.

## 11. Marketing va sotuv

Saytda pixel, UTM, mailing va tripwire eslatilgan. Backend marketing manbalarini buyurtma bilan bog'lashi kerak.

Mantiq:

1. User landingga UTM bilan keladi.
2. UTM cookie/local storage orqali checkoutgacha olib boriladi.
3. Invoice yaratilganda UTM maydonlari saqlanadi.
4. Dashboard qaysi reklama manbasi ko'proq sotuv qilganini chiqaradi.
5. Tripwire arzon mahsulot orqali leadni birinchi xaridga olib keladi.

## 12. API hujjatlar va integratsiyalar

Exode docs sahifasida API orqali foydalanuvchilar, guruhlar, kurslar, accesslar, formalar, exportlar va webhooklar boshqarilishi aytilgan. Clone backendda ham tashqi integratsiyalar uchun tokenli API kerak.

Mantiq:

- Servis token school yoki seller darajasida beriladi.
- Har token scope/permission bilan cheklanadi.
- API response formati yagona bo'ladi.
- Webhooklar tashqi CRM, bot yoki BI tizimlarga event yuboradi.
- Export joblar katta hisobotlarni backgroundda tayyorlaydi.

## 13. Mobil ilova imkoniyatlari

Google Play va App Store tavsifida mobil ilova orqali maktab tanlash, kurs o'qish, video/text/test/topshiriq, chat, gamifikatsiya va reyting ishlashi ko'rsatiladi.

Backend mantiqi:

- `GET /mobile/schools` user ulangan maktablarni beradi.
- `GET /mobile/me/courses` davom ettiriladigan kurslarni beradi.
- `GET /mobile/lessons/{id}` dars kontentini beradi.
- `POST /mobile/practices/{id}/attempts` vazifa yuboradi.
- `GET /mobile/rating` ball va reytingni beradi.

## 14. Qo'llab-quvvatlash va migratsiya

Saytda boshqa platformadan kontent ko'chirish, jamoani o'qitish va 24/7 support bor. Backendda support jarayonlari uchun minimal model bo'lishi mumkin.

Mantiq:

- Migration request: eski platforma, kontent hajmi, status.
- Support ticket: mavzu, prioritet, mas'ul manager.
- Onboarding checklist: domen, to'lov, kurs, xodim, katalog sozlandi yoki yo'q.

## 15. Clone loyihada ustuvorlik

Uyga vazifa uchun hamma narsani birdan kodlash shart emas. Tavsiya etilgan ketma-ketlik:

1. Auth + school + role.
2. Course/module/lesson CRUD.
3. Product + invoice + fake payment webhook.
4. ProductAccess + student course progress.
5. Practice/test minimal modeli.
6. Analytics dashboard minimal endpoint.
7. Messenger va notificationning sodda varianti.
8. Webhook/API token va export joblar.

Shu tartibda qurilsa, loyiha Exode'ning asosiy biznes qiymatini — kurs yaratish, sotish, o'qitish va natijani kuzatishni — backend darajasida takrorlay oladi.
