from people.models import Person

# Simple duplicate rule: treat as duplicate when we find an existing record
# and at least two of the following match: national_id, name, mother_name.
def is_duplicate(person_like: dict) -> bool:
    name = person_like.get("name")
    mother = person_like.get("mother_name")
    nid = person_like.get("national_id")

    qs = Person.objects.all()
    if name:
        qs = qs.filter(name=name)
    if mother:
        qs = qs.filter(mother_name=mother) | qs
    if nid:
        qs = qs.filter(national_id=nid) | qs
    return qs.exists()
