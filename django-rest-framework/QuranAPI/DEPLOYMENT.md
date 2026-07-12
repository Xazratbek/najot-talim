# Deployment (Gunicorn + Nginx + Supervisor)

## Currently running: local deployment

This is a local study project with no remote VPS/cloud credentials attached, so the
Gunicorn + Nginx + Supervisor stack described below is actually running **on this
machine** as the "server", using the exact same three tools a real VPS deploy would use:

```bash
deploy/local/start.sh   # supervisord -> gunicorn (unix socket) -> nginx :8088
deploy/local/stop.sh
```

- Swagger UI: http://127.0.0.1:8088/api/
- API root:   http://127.0.0.1:8088/api/v1/surah/
- Process manager: `supervisorctl -c deploy/local/supervisord.conf status`
- Nginx config: `deploy/local/nginx.local.conf` (proxies :8088 -> gunicorn unix socket, serves `/static/`)
- Gunicorn config: `deploy/local/gunicorn.local.conf.py` (unix socket in `/tmp/quranapi-run/`, short path to stay under macOS's AF_UNIX 104-byte limit)

The sections below are the generic recipe for pointing the same configs at a real
remote server once one is available.

---

Target: any Ubuntu/Debian VPS with Python 3.11+, PostgreSQL and Nginx installed.

## 1. Get the code onto the server

```bash
sudo mkdir -p /var/www/quranapi
sudo chown $USER:$USER /var/www/quranapi
git clone <your-repo-url> /var/www/quranapi
cd /var/www/quranapi
```

## 2. Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Environment variables

Copy `.env.example` to `.env` and fill in real values (never commit `.env`):

```bash
cp .env.example .env
```

```
DEBUG=False
SECRET_KEY=<generate a new one>
ALLOWED_HOSTS=your-domain.example.com
DATABASE_URL=postgres://user:password@host:5432/dbname
```

## 4. Database

```bash
python manage.py migrate
python manage.py import_quran        # loads 178 editions + 114 surahs + 6236 ayahs + 30 juz
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 5. Gunicorn + Supervisor

```bash
sudo mkdir -p /run/quranapi /var/log/quranapi
sudo chown www-data:www-data /run/quranapi /var/log/quranapi

sudo cp deploy/supervisor/quranapi.conf /etc/supervisor/conf.d/quranapi.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status quranapi
```

`gunicorn.conf.py` (project root) binds to `unix:/run/quranapi/gunicorn.sock` and is
picked up automatically by the supervisor command.

## 6. Nginx

```bash
sudo cp deploy/nginx/quranapi.conf /etc/nginx/sites-available/quranapi
sudo ln -s /etc/nginx/sites-available/quranapi /etc/nginx/sites-enabled/quranapi
sudo nginx -t && sudo systemctl reload nginx
```

Edit `server_name` in `deploy/nginx/quranapi.conf` to your real domain, and add TLS
with `certbot --nginx -d your-domain.example.com` once DNS points at the server.

## 7. Verify

- API root: `http://your-domain.example.com/api/v1/surah/`
- Swagger UI: `http://your-domain.example.com/api/`
- Admin: `http://your-domain.example.com/admin/`

## Redeploying after changes

```bash
cd /var/www/quranapi
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart quranapi
```
