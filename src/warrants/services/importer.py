# warrants/services/importer.py
from datetime import datetime
from typing import Optional, Tuple, Dict

from django.db import transaction
from people.models import Person
from warrants.models import Warrant

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d")

def _parse_date(val: Optional[str]):
    if val in (None, "", "nan", "NaT"):
        return None
    s = str(val).strip().split(" ")[0]
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None

def _parse_float(val: Optional[str]):
    if val in (None, "", "nan", "NaN"):
        return None
    try:
        return float(val)
    except Exception:
        try:
            return float(str(val).replace(",", "."))
        except Exception:
            return None

def import_from_dataframe(df, *, dry_run: bool = False) -> Dict[str, int]:
    """
    Espera colunas (case-insensitive):
      national_id,name,mother_name,birth_date,number,status,issued_at,court,lat,lon
    Retorna um resumo com contagens.
    """
    # normaliza nomes de colunas para lower
    df.columns = [c.strip().lower() for c in df.columns]

    # garante que todas as colunas existam
    for col in ["national_id","name","mother_name","birth_date","number","status","issued_at","court","lat","lon"]:
        if col not in df.columns:
            df[col] = None

    created_people = 0
    updated_people = 0
    created_warrants = 0
    updated_warrants = 0

    ctx = transaction.atomic() if not dry_run else _NullContext()
    with ctx:
        for _, row in df.iterrows():
            name = (row["name"] or "").strip() if row["name"] is not None else ""
            if not name:
                continue

            national_id = (str(row["national_id"]).strip()
                           if row["national_id"] not in (None, "", "nan", "NaN") else None)
            mother_name = (str(row["mother_name"]).strip()
                           if row["mother_name"] not in (None, "", "nan", "NaN") else None)
            birth_date = _parse_date(row["birth_date"])

            person, p_created = Person.objects.get_or_create(
                national_id=national_id,
                name=name,
                mother_name=mother_name,
                defaults={"birth_date": birth_date},
            )
            if p_created:
                created_people += 1
            else:
                if birth_date and not person.birth_date:
                    person.birth_date = birth_date
                    person.save(update_fields=["birth_date"])
                    updated_people += 1

            number = (str(row["number"]).strip()
                      if row["number"] not in (None, "", "nan", "NaN") else None)
            if not number:
                continue

            status = (str(row["status"]).strip()
                      if row["status"] not in (None, "", "nan", "NaN") else "ATIVO")
            issued_at = _parse_date(row["issued_at"])
            court = (str(row["court"]).strip()
                     if row["court"] not in (None, "", "nan", "NaN") else None)
            lat = _parse_float(row["lat"])
            lon = _parse_float(row["lon"])

            _, w_created = Warrant.objects.update_or_create(
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

    return {
        "rows": len(df),
        "people_created": created_people,
        "people_updated": updated_people,
        "warrants_created": created_warrants,
        "warrants_updated": updated_warrants,
        "dry_run": int(dry_run),
    }

class _NullContext:
    def __enter__(self): return self
    def __exit__(self, *exc): return False
