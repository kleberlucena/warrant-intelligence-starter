import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .transform import transform
from people.models import Person
from warrants.models import Warrant, WarrantList, WarrantMembership

class ImportView(APIView):
    permission_classes = [permissions.AllowAny]  # adjust in real deployments

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "Upload a CSV file in 'file' field."},
                            status=status.HTTP_400_BAD_REQUEST)
        df = pd.read_csv(file)
        df = transform(df)

        wl = WarrantList.objects.create(name="upload")
        created_people = 0
        created_warrants = 0
        for _, row in df.iterrows():
            person, p_created = Person.objects.get_or_create(
                name=row.get("name",""),
                mother_name=row.get("mother_name",""),
                national_id=row.get("national_id",""),
                defaults={"sex": row.get("sex",""), "birth_date": row.get("birth_date")},
            )
            created_people += int(p_created)

            w, w_created = Warrant.objects.get_or_create(
                number=str(row.get("number","")), defaults={"court": row.get("court",""),
                                                            "status": row.get("status","ATIVO")}
            )
            created_warrants += int(w_created)

            if person.id and w.id:
                WarrantMembership.objects.get_or_create(person=person, warrant=w, list=wl)

        return Response({
            "people_created": created_people,
            "warrants_created": created_warrants,
            "list_id": wl.id,
            "rows_processed": len(df),
        }, status=200)
