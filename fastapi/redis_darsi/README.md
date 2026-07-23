# Redis darsi

Bu darsda FastAPI va DRF blog APIlarida Redis cache ishlatish ko'rsatilgan:

- postlarni ko'rish
- post bo'yicha oxirgi 10 ta commentni ko'rish
- post like soni va comment sonini ko'rish

Redis kalitlari yozuv o'zgarganda tozalanadi. FastAPI namunasi SQLAlchemy async bilan, DRF namunasi Django cache framework bilan ishlaydi.


## DRF da Celery + Redis

DRF loyihasida Redis va RabbitMQ ishlatiladi:

- `django-redis` orqali API response cache saqlash
- RabbitMQ Celery broker sifatida background tasklarni navbatga qo'yish
- Redis Celery result backend sifatida task natijalarini saqlash

Comment qo'shilganda yoki like bosilganda API cache kalitlarini tozalaydi va `refresh_post_cache` Celery taskini RabbitMQ broker orqali workerga yuboradi. Worker oxirgi 10 ta comment va post stats cachelarini qayta tayyorlab qo'yadi.

Ishga tushirish:

```bash
cd fastapi/redis_darsi
docker compose up -d redis rabbitmq
python drf_app/manage.py migrate
celery -A drf_app worker -l info
python drf_app/manage.py runserver
```


Agar Celery broker sifatida RabbitMQ o'rniga Redis ishlatmoqchi bo'lsang:

```bash
export CELERY_BROKER_URL=redis://127.0.0.1:6379/2
export CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
```
