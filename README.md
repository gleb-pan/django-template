# Django + Docker Cookiecutter Template

A pragmatic Django template with Docker-first development, split settings, and sensible defaults.  
Generate a production-ready baseline in minutes — then customize.

- The project is ready to run inside the docker exatcly after the cookiecutter generation.

- Database name is attached to project_slug.

- .env file is generated automatically based on .env.example.

- DJANGO_SECRET_KEY and POSTGRES_PASSWORD are generated automatically after the template generation (see hooks/post_gen_project.py).

- **Don't forget to change DB password if you're not OK with the generated one.**

---

## ✨ What this template gives you

- **Django 5.x** project scaffolded via Cookiecutter
- **Dockerized development** (Django + PostgreSQL) with persistent volumes
- **Clean settings layout**: `config/settings/{base,dev,prod}.py`
- **12-factor friendly**: environment variables via `.env`
- **Makefile helpers** for common tasks
- **CI/CD-ready** (GitHub Actions friendly layout)

> You work on code locally (hot-reload). DB lives in Docker. No local Postgres install required.

---

## 🔧 Prerequisites

- [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)
- [Python 3.12+](https://www.python.org/)
- [make (Windows)](https://community.chocolatey.org/packages/make) (optionally) - for running make commands (see MAKEFILE_COMMANDS.md)
- [make (Linux)]() - bash: 'sudo apt install make'

```bash
pip install cookiecutter
```

## 🚀 Examples


```bash
# locally
cookiecutter .

# or directly from github (USE HTTPS LINK)
cookiecutter https://github.com/<you>/<template-repo>.git

# test the docker setup
docker compose -f docker-compose.dev.yml up --build

# enter docker container via shell
make d-sh
#: python manage.py createsuperuser . . .

# continue working locally
cd project_name
make deps # creates venv with all listed packages
```