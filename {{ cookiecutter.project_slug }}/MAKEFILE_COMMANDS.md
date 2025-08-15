# Makefile Guide (Windows-first, pip-tools)

## Quick Start (первый запуск)

```bash
make venv          # создать .venv и базовые тулзы
make deps          # собрать/зафиксировать зависимости и установить (base+dev)
make env           # скопировать backend/.env.example -> backend/.env (потом отредактируй)
make mig           # миграции
make run           # сервер разработки http://0.0.0.0:8000
```

## Ежедневный цикл (после `git pull`)

```bash
make sync   # привести окружение строго к base.txt+dev.txt
make mig    # применить миграции (если есть новые)
make run    # запустить сервер разработки (или см. Docker ниже)
```

## Если менялись зависимости

### Прод-зависимости (`backend/requirements/pyproject.toml`)
```bash
make compile-base   # пересобрать пины прод-зависимостей -> base.txt
make constraints    # обновить constraints.txt из base.txt (при необходимости подправить)
make sync           # привести окружение к base.txt+dev.txt
make test           # проверить, что всё ок
```

## Dev-зависимости (`backend/requirements/dev.in`)

```bash
make compile-dev    # пересобрать пины дев-тулзов -> dev.txt (под constraints.txt)
make sync           # привести окружение к base.txt+dev.txt
make test           # проверить, что всё ок после обновлений
```