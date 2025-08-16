# ============================
# Windows-first Makefile (pip-tools)
# pyproject.toml -> base.txt -> constraints.txt
# dev.in + -c constraints.txt -> dev.txt
# sync по двум файлам: base.txt + dev.txt
# Работает в VSCode PowerShell (GNU Make из Git for Windows / MSYS).
# ============================

# Путь к питону из venv (Windows). Форвард-слэши, чтобы шелл не блевал.
PY := .venv\Scripts\python.exe

# Корневые пути
BACKEND=backend
REQ=backend/requirements

.PHONY: venv deps compile-base constraints compile-dev sync mig run fmt lint test precommit env upgrade info check help

# 0) Создать venv и поставить базовые тулзы (pip-tools и прочее)
venv:
	py -3 -m venv .venv
	$(PY) -m pip install -U pip setuptools wheel
	$(PY) -m pip install pip-tools black isort ruff pytest pytest-django pre-commit

# 1) База из pyproject.toml -> base.txt (пины)
compile-base:
	$(PY) -m piptools compile $(REQ)/pyproject.toml -o $(REQ)/base.txt

# 2) constraints.txt = копия base.txt (тут потом руками фиксируешь спорные версии)
constraints:
	$(PY) -c "import shutil, pathlib; shutil.copy(pathlib.Path(r'$(REQ)/base.txt'), pathlib.Path(r'$(REQ)/constraints.txt'))"

# 3) dev.in под constraints -> dev.txt (пины для дев-инструментов)
compile-dev:
	$(PY) -m piptools compile -c $(REQ)/constraints.txt $(REQ)/dev.in -o $(REQ)/dev.txt --strip-extras

# 4) Приводим окружение ровно к двум пин-файлам (base + dev)
sync:
	$(PY) -m piptools sync $(REQ)/base.txt $(REQ)/dev.txt

# Один выстрел: создать/обновить всё и установить
deps: venv compile-base constraints compile-dev sync

# Django: миграции
mig:
	cd $(BACKEND) && $(PY) manage.py makemigrations && $(PY) manage.py migrate

# Django: сервер разработки
run:
	cd $(BACKEND) && $(PY) manage.py runserver 0.0.0.0:8000

# Скопировать .env.example -> .env кроссплатформенно (без Copy-Item/cp)
env:
	$(PY) -c "from pathlib import Path; import shutil, re, secrets, string; from secrets import token_urlsafe; \
	alphabet = string.ascii_letters + string.digits; \
	gen_pass = ''.join(secrets.choice(alphabet) for _ in range(20)); \
	s=Path('backend/.env.example'); d=Path('backend/.env'); \
	shutil.copy(s,d) if s.exists() else print('WARN: backend/.env.example not found'); \
	text = d.read_text(); \
	secret = token_urlsafe(50); \
	text = re.sub(r'^SECRET_KEY=.*$$', f'SECRET_KEY={secret}', text, flags=re.M); \
	text = re.sub(r'^POSTGRES_PASSWORD=.*$$', f'POSTGRES_PASSWORD={gen_pass}', text, flags=re.M); \
	d.write_text(text)"

# Форматирование
fmt:
	$(PY) -m black .
	$(PY) -m isort .

# Линты (без автофиксов)
lint:
	$(PY) -m black --check .
	$(PY) -m isort --check-only .

# Тесты
test:
	cd $(BACKEND) && $(PY) -m pytest -q

# pre-commit хуки
precommit:
	$(PY) -m pre_commit install

# Апгрейд пинов до свежих версий (и синк)
upgrade:
	$(PY) -m piptools compile -U $(REQ)/pyproject.toml -o $(REQ)/base.txt
	$(PY) -c "import shutil, pathlib; shutil.copy(pathlib.Path(r'$(REQ)/base.txt'), pathlib.Path(r'$(REQ)/constraints.txt'))"
	$(PY) -m piptools compile -U -c $(REQ)/constraints.txt $(REQ)/dev.in -o $(REQ)/dev.txt
	$(PY) -m piptools sync $(REQ)/base.txt $(REQ)/dev.txt

# Отладочная инфа
info:
	@echo Using venv python: $(PY)
	@echo Requirements dir:  $(REQ)

# Проверка версии питона и тулов (на всякий)
check:
	$(PY) -V
	$(PY) -m piptools --version

help:
	@echo === Make targets (quick reference) ===
	@echo venv             - Create .venv and install base tools (pip-tools/black/isort/ruff/pytest/pre-commit)
	@echo compile-base     - pyproject.toml to requirements/base.txt (pin production deps)
	@echo constraints      - Copy base.txt to constraints.txt (lock tricky versions)
	@echo compile-dev      - dev.in + -c constraints.txt to dev.txt (pin dev tools)
	@echo sync             - Sync environment exactly to base.txt + dev.txt
	@echo deps             - One shot: venv + compile-* + constraints + sync
	@echo mig              - Django: makemigrations + migrate
	@echo run              - Django: runserver 0.0.0.0:8000
	@echo env              - Copy backend/.env.example to backend/.env (if exists)
	@echo fmt              - Formatting: black + isort
	@echo lint             - Checks only: black --check + isort --check-only
	@echo test             - pytest (in backend directory)
	@echo precommit        - Install pre-commit hooks
	@echo upgrade          - Update pins (base/dev) to latest compatible versions and sync
	@echo info             - Show paths: interpreter and requirements directory
	@echo check            - Verify Python and pip-tools versions
	@echo d-build          - Docker Compose: build
	@echo d-up             - Docker Compose: up -d (fast start without build)
	@echo d-down           - Docker Compose: down (stop and remove containers)
	@echo d-logs           - Docker Compose: logs for web (tail=200, follow)
	@echo d-sh             - Enter web container (sh)
	@echo ---


.PHONY: d-build d-up d-down d-logs d-sh

d-build:
	docker compose -f docker-compose.dev.yml build

d-up:
	docker compose -f docker-compose.dev.yml up -d

d-down:
	docker compose -f docker-compose.dev.yml down

d-logs:
	docker compose -f docker-compose.dev.yml logs -f --tail=200 web

# залезть внутрь контейнера
d-sh:
	docker compose -f docker-compose.dev.yml exec web sh