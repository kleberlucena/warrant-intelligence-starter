# dashboard/urls.py
from django.urls import path
from .views import HomeView, HealthcheckView, MapView, PeopleListView, ImportDataView

app_name = "dashboard"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("health/", HealthcheckView.as_view(), name="health"),
    path("mapa/", MapView.as_view(), name="mapa"),
    path("people/", PeopleListView.as_view(), name="people-list"),
    path("importar/", ImportDataView.as_view(), name="importar"),
]

