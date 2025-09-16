from django.db import models
from people.models import Person

class WarrantList(models.Model):
    name = models.CharField(max_length=120)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.name

class Warrant(models.Model):
    number = models.CharField(max_length=80, db_index=True)
    court = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=40, default="ATIVO")

    def __str__(self):
        return f"{self.number} - {self.status}"

class WarrantMembership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    warrant = models.ForeignKey(Warrant, on_delete=models.CASCADE)
    list = models.ForeignKey(WarrantList, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
