#!/usr/bin/env python
import os, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent      # /home/projetos/WIS
SRC_DIR = BASE_DIR / "src"                      # /home/projetos/WIS/src
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from dotenv import load_dotenv
from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")  # carrega variáveis do arquivo .env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.management import execute_from_command_line
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
