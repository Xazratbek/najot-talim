# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Django REST Framework API mirroring the shape of https://alquran.cloud/api (the alquran.cloud
public Quran API), backed by a local Postgres database. This is a local study project (not a
strict clone — only the parts of that API's data model that matter here were ported over).

## Commands

```bash
# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations qurancloud
python manage.py migrate

# Populate the database from alquran.cloud (idempotent — safe to re-run)
python manage.py import_quran
python manage.py import_quran --edition en.sahih        # import a different edition's ayah text
python manage.py import_quran --skip-editions            # skip the 178-edition catalogue
python manage.py import_quran --skip-juz                 # skip building Juz groupings
python manage.py import_quran --editions-file editions.json --quran-file quran.json
                                                           # import from local JSON instead of
                                                           # hitting the network (alquran.cloud's
                                                           # gateway rate-limits some cloud/VPS IPs)

# Tests
python manage.py test                 # Django's own test runner
pytest                                 # equivalent, via pytest-django (config in pytest.ini)
pytest qurancloud/tests/test_views.py::SurahAPITests::test_retrieve_surah_by_number_returns_all_editions_ayahs
                                        # run a single test

# Coverage (config in .coveragerc, source = qurancloud only)
coverage run -m pytest
coverage report -m
coverage html                          # writes htmlcov/index.html
```

Env vars are loaded from a `.env` file at the project root via `django-environ`
(`DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) — see `.env.example`. There is no
in-repo default database password; `settings.py` falls back to a local Postgres DSN only if
`.env` is absent.

## Architecture

**Single Django app**: all domain code lives in `qurancloud/` (models, serializers, views, urls,
the `import_quran` management command, tests). `utils/` holds only `BaseModel`, an abstract base
with `created_at`/`updated_at` that every model inherits. `config/` is the Django project
(settings/urls/wsgi/asgi) — nothing else lives there.

**Data model** (`qurancloud/models.py`): `Edition` (a Quran text/translation/tafsir source, keyed
by `identifier`, unique) → `Surah` (114 chapters, keyed by `number`, unique) → `Ayah` (verses;
FKs to both `Surah` and `Edition`, unique together on `(surah, edition, number_in_surah)` — the
same surah exists once per edition it's been imported for). `Juz` is a derived grouping
(`ManyToManyField` to both `Ayah` and `Surah`, unique per `(number, edition)`), built by grouping
already-imported ayahs by their `juz` field rather than fetched separately from the API.

`Ayah.sajda` is a plain bool; `sajda_obligatory`/`sajda_recommended` capture the detail that
alquran.cloud embeds as an object (`{id, recommended, obligatory}`) instead of `false` on verses
requiring prostration — the import command derives all three from that single field.

**Import pipeline** (`qurancloud/management/commands/import_quran.py`): pulls the *entire* Quran
in one request (`GET /v1/quran/{edition}`, not 114 per-surah calls) plus the edition catalogue
(`GET /v1/edition`), then does exactly one `bulk_create` per model (`ignore_conflicts=True`),
making re-runs idempotent without extra round-trips. `--editions-file`/`--quran-file` let it read
the same JSON shape from disk — needed because alquran.cloud's Kong gateway rate-limits/blocks
some datacenter IP ranges (this bit DigitalOcean specifically; fetch from a non-blocked host and
copy the JSON over).

**API surface** (`qurancloud/views.py` + `urls.py`): DRF generic views only (`ListAPIView`/
`RetrieveAPIView`), no viewsets. Detail routes mirror alquran.cloud's URL shape:
`surah/<number>/`, `surah/<number>/<edition>/` (ayahs filtered to one edition via `Prefetch`),
`edition/<identifier>/`, `juz/<number>/`. Schema/docs are served by `drf-spectacular`
(`/api/schema/` raw OpenAPI, `/api/` Swagger UI) — **not** `drf-yasg`/`rest_framework_swagger`,
which are incompatible with the DRF/Django versions this project pins (crashes with
`AssertionError: duplicate Parameters found` on schema generation).

**Tests** (`qurancloud/tests/`): `test_models.py` (constraints/defaults), `test_views.py`
(`APITestCase`, hits real endpoints through DRF's test client), `test_import_quran.py` (mocks
`requests.get` at the command's import path — never hits the network). `factories.py` has plain
functions (no factory_boy), each accepting `**overrides` over sane defaults.

## Deployment

Not a generic cloud target — configs exist for two concrete scenarios, both Gunicorn +
Nginx + Supervisor:

- `deploy/local/` — runs the full stack on the dev machine itself (`start.sh`/`stop.sh`), using
  short-path unix sockets under `/tmp/quranapi-run/` (macOS's `AF_UNIX` path limit is 104 bytes,
  which a project-relative socket path exceeds).
- `deploy/nginx/quranapi.conf`, `deploy/supervisor/quranapi.conf`, `gunicorn.conf.py` — the real
  recipe for a remote VPS, documented step-by-step in `DEPLOYMENT.md` (includes the currently-live
  droplet's setup: free `sslip.io` DNS + Let's Encrypt, since bare IPs can't get a TLS cert).
