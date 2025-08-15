# ============================
# Windows-first Makefile (pip-tools)
# pyproject.toml -> base.txt -> constraints.txt
# dev.in + -c constraints.txt -> dev.txt
# sync по двум файлам: base.txt + dev.txt
# Работает в VSCode PowerShell (GNU Make из Git for Windows / MSYS).
# ============================

# Путь к питону из venv (Windows). Форвард-слэши, чтобы шелл не блевал.
PY=./.venv/Scripts/python.exe

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
	$(PY) -c "from pathlib import Path; import shutil, secrets, string; from django.core.management.utils import get_random_secret_key as gk; \
	alphabet = string.ascii_letters + string.digits; \
	gen_pass = ''.join(secrets.choice(alphabet) for _ in range(20)); \
	s=Path('backend/.env.example'); d=Path('backend/.env'); \
	shutil.copy(s,d) if s.exists() else print('WARN: backend/.env.example not found'); \
	text = d.read_text(); \
	text = text.replace('SECRET_KEY=', f'SECRET_KEY={gk()}'); \
	text = text.replace('POSTGRES_PASSWORD=', f'POSTGRES_PASSWORD={gen_pass}'); \
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
	@echo "=== Make targets (кратко) ==="
	@printf "  %-18s %s\n" "venv"           "Создать .venv и поставить базовые тулзы (pip-tools/black/isort/ruff/pytest/pre-commit)"
	@printf "  %-18s %s\n" "compile-base"   "pyproject.toml -> requirements/base.txt (пины прод-зависимостей)"
	@printf "  %-18s %s\n" "constraints"    "Скопировать base.txt -> constraints.txt (фиксируешь спорные версии)"
	@printf "  %-18s %s\n" "compile-dev"    "dev.in + -c constraints.txt -> dev.txt (пины дев-тулов)"
	@printf "  %-18s %s\n" "sync"           "Привести окружение ровно к base.txt + dev.txt"
	@printf "  %-18s %s\n" "deps"           "Один выстрел: venv + compile-* + constraints + sync"
	@printf "  %-18s %s\n" "mig"            "Django: makemigrations + migrate"
	@printf "  %-18s %s\n" "run"            "Django: runserver 0.0.0.0:8000"
	@printf "  %-18s %s\n" "env"            "Скопировать backend/.env.example -> backend/.env (если есть)"
	@printf "  %-18s %s\n" "fmt"            "Форматирование: black + isort"
	@printf "  %-18s %s\n" "lint"           "Проверки без автофиксов: black --check + isort --check-only"
	@printf "  %-18s %s\n" "test"           "pytest (в каталоге backend)"
	@printf "  %-18s %s\n" "precommit"      "Установить pre-commit хуки"
	@printf "  %-18s %s\n" "upgrade"        "Апдейт пинов (base/dev) до свежих версий и sync"
	@printf "  %-18s %s\n" "info"           "Показать пути: интерпретатор и директорию requirements"
	@printf "  %-18s %s\n" "check"          "Проверить версии Python и pip-tools"
	@printf "  %-18s %s\n" "d-build"        "Docker Compose: build"
	@printf "  %-18s %s\n" "d-up"           "Docker Compose: up -d (быстрый старт без билда)"
	@printf "  %-18s %s\n" "d-down"         "Docker Compose: down (остановить и убрать контейнеры)"
	@printf "  %-18s %s\n" "d-logs"         "Docker Compose: логи web (tail=200, follow)"
	@printf "  %-18s %s\n" "d-sh"           "Войти в контейнер web (sh)"
	@echo "— Подсказка: код менял — 'd-up', Dockerfile/зависимости менял — 'd-build' или 'd-up --build'."

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