from django.urls import path, include
from rest_framework.routers import DefaultRouter
from people.views import PersonViewSet
from warrants.views import WarrantViewSet
from etl.views import ImportView

router = DefaultRouter()
router.register(r"people", PersonViewSet, basename="people")
router.register(r"warrants", WarrantViewSet, basename="warrants")

urlpatterns = [
    path("", include(router.urls)),
    path("etl/import/", ImportView.as_view(), name="etl-import"),
]
