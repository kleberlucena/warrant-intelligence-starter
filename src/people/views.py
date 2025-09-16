from rest_framework import viewsets, filters
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by("-created_at")
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name","mother_name","national_id"]
    ordering_fields = ["created_at","name"]
