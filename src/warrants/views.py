from rest_framework import viewsets, filters
from .models import Warrant
from .serializers import WarrantSerializer

class WarrantViewSet(viewsets.ModelViewSet):
    queryset = Warrant.objects.all().order_by("-id")
    serializer_class = WarrantSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["number","court","status"]
    ordering_fields = ["id","number","status"]
