import os
from datetime import datetime
from typing import Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import pandas as pd

from people.models import Person
from warrants.models import Warrant


DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d")  # tente alguns formatos comuns


def parse_date(val: Optional[str]):
    if val in (None, "", "nan", "NaT"):
        return None
    s = str(val).strip()
    # se vier como '2024-07-31 00:00:00' pega só a parte da data
    s = s.split(" ")[0]
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def parse_float(val: Optional[str]):
    if val in (None, "", "nan", "NaN"):
        return None
    try:
        return float(val)
    except Exception:
        try:
            return float(str(val).replace(",", "."))
        except Exception:
            return None


class Command(BaseCommand):
    help = (
        "Importa CSV com pessoas e mandados.\n"
        "Colunas esperadas (case-insensitive):\n"
        "  national_id,name,mother_name,birth_date,number,status,issued_at,court,lat,lon\n"
    )

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Caminho do arquivo CSV")
        parser.add_argument(
            "--sep", default=",", help="Separador do CSV (padrão: ,). Ex: ;"
        )
        parser.add_argument(
            "--encoding", default="utf-8", help="Encoding (padrão: utf-8)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Não grava no banco; só mostra o que faria",
        )

    def handle(self, *args, **opts):
        path = opts["csv_path"]
        sep = opts["sep"]
        encoding = opts["encoding"]
        dry_run = opts["dry_run"]

        if not os.path.exists(path):
            raise CommandError(f"Arquivo não encontrado: {path}")

        # lê CSV
        try:
            df = pd.read_csv(path, sep=sep, encoding=encoding)
        except Exception as e:
            raise CommandError(f"Erro lendo CSV: {e}")

        # normaliza nomes de colunas (lower)
        df.columns = [c.strip().lower() for c in df.columns]

        # colunas que vamos tentar usar (todas opcionais menos name/number para o mandado)
        cols = {
            "national_id": "national_id",
            "name": "name",
            "mother_name": "mother_name",
            "birth_date": "birth_date",
            "number": "number",
            "status": "status",
            "issued_at": "issued_at",
            "court": "court",
            "lat": "lat",
            "lon": "lon",
        }
        for key in list(cols.keys()):
            if key not in df.columns:
                # mantém a chave, mas o valor virá None nas linhas
                df[key] = None

        created_people = 0
        updated_people = 0
        created_warrants = 0
        updated_warrants = 0
        total = len(df)

        self.stdout.write(self.style.NOTICE(f"Linhas no CSV: {total}"))

        # transação (se não for dry-run)
        ctx = transaction.atomic() if not dry_run else _NullContext()

        with ctx:
            for _, row in df.iterrows():
                name = (row["name"] or "").strip() if row["name"] is not None else ""
                if not name:
                    # sem nome, pula (pode logar)
                    continue

                national_id = (str(row["national_id"]).strip()
                               if row["national_id"] not in (None, "", "nan", "NaN")
                               else None)
                mother_name = (str(row["mother_name"]).strip()
                               if row["mother_name"] not in (None, "", "nan", "NaN")
                               else None)
                birth_date = parse_date(row["birth_date"])

                # dedupe pela trinca (national_id, name, mother_name)
                person, p_created = Person.objects.get_or_create(
                    national_id=national_id,
                    name=name,
                    mother_name=mother_name,
                    defaults={"birth_date": birth_date},
                )
                if p_created:
                    created_people += 1
                else:
                    # se vier birth_date e estiver vazio, atualiza
                    if birth_date and not person.birth_date:
                        person.birth_date = birth_date
                        person.save(update_fields=["birth_date"])
                        updated_people += 1

                # mandado
                number = (str(row["number"]).strip()
                          if row["number"] not in (None, "", "nan", "NaN")
                          else None)
                if not number:
                    # sem número não cadastra mandado
                    continue

                status = (str(row["status"]).strip()
                          if row["status"] not in (None, "", "nan", "NaN")
                          else "ATIVO")
                issued_at = parse_date(row["issued_at"])
                court = (str(row["court"]).strip()
                         if row["court"] not in (None, "", "nan", "NaN")
                         else None)
                lat = parse_float(row["lat"])
                lon = parse_float(row["lon"])

                warrant, w_created = Warrant.objects.update_or_create(
                    person=person,
                    number=number,
                    defaults={
                        "status": status or "ATIVO",
                        "issued_at": issued_at,
                        "court": court,
                        "lat": lat,
                        "lon": lon,
                    },
                )
                if w_created:
                    created_warrants += 1
                else:
                    updated_warrants += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"OK — Pessoas: +{created_people} criadas, {updated_people} atualizadas | "
                f"Mandados: +{created_warrants} criados, {updated_warrants} atualizados"
            )
        )


class _NullContext:
    """context manager no-op para dry-run."""
    def __enter__(self): return self
    def __exit__(self, *exc): return False
