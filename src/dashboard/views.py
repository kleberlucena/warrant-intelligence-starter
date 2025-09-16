from django.shortcuts import render
from people.models import Person
from warrants.models import Warrant

def home(request):
    stats = {
        "people": Person.objects.count(),
        "warrants": Warrant.objects.count(),
    }
    return render(request, "dashboard/home.html", {"stats": stats})
