#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path
import secrets
import string

ROOT = Path.cwd()
BACKEND = ROOT / "backend"
ENV_EXAMPLE = BACKEND / ".env.example"
ENV_FILE = BACKEND / ".env"

# Генератор строки без знака '$' (и вообще без пробельных сюрпризов)
def gen_safe_string(length=50, extra: str = "") -> str:
    # Разрешённые символы: буквы, цифры, часть пунктуации без $
    allowed_punct = "!@#%^&*()-_=+[]{}|;:,.?/"  # никаких $
    alphabet = string.ascii_letters + string.digits + allowed_punct + extra
    return "".join(secrets.choice(alphabet) for _ in range(length))

def replace_line(contents: str, key: str, value: str) -> str:
    pattern = rf"(?m)^{re.escape(key)}=.*$"
    replacement = f"{key}={value}"
    if re.search(pattern, contents):
        return re.sub(pattern, replacement, contents)
    # если ключа не было — добавим в конец
    return contents.rstrip() + "\n" + replacement + "\n"

def main():
    try:
        if not ENV_EXAMPLE.exists():
            print(f"WARN: {ENV_EXAMPLE} not found; skip .env generation")
            return

        # 1) Скопировали .env.example → .env (перетираем, чтобы всегда актуально)
        shutil.copyfile(ENV_EXAMPLE, ENV_FILE)

        # 2) Сгенерили значения без '$'
        secret_key = gen_safe_string(64)

        pg_password = gen_safe_string(24)

        # 3) Подставили
        contents = ENV_FILE.read_text(encoding="utf-8")
        contents = replace_line(contents, "SECRET_KEY", secret_key)
        contents = replace_line(contents, "POSTGRES_PASSWORD", pg_password)

        print(f"\nDjango secret key: {secret_key}")
        print(f"PostgreSQL password: {pg_password}\n")
        print(f"YOU CAN CHANGE AUTOMATICALLY GENERATED CREDENTIALS IN 'project_name/backend/.env'\n")

        # На всякий случай: если DEBUG пустой — выставим 1 (dev-значение)
        if re.search(r"(?m)^DEBUG\s*=\s*$", contents):
            contents = replace_line(contents, "DEBUG", "1")
            print('DEBUG has been set to TRUE')

        ENV_FILE.write_text(contents, encoding="utf-8")

        # Git hygiene: убедимся, что .env в .gitignore
        gi = ROOT / ".gitignore"
        try:
            if gi.exists():
                gi_text = gi.read_text(encoding="utf-8")
                if "backend/.env" not in gi_text:
                    gi.write_text((gi_text.rstrip() + "\nbackend/.env\n"), encoding="utf-8")
            else:
                gi.write_text("backend/.env\n", encoding="utf-8")
        except Exception as e:
            print(f"WARN: couldn't update .gitignore: {e}")

    except Exception as e:
        # Не падаем молча — пусть видно причину
        print(f"ERROR generating .env: {e}")

if __name__ == "__main__":
    main()
