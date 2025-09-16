from django.db import models

class Person(models.Model):
    SEX_CHOICES = (("M", "Male"), ("F", "Female"))
    name = models.CharField(max_length=160)
    mother_name = models.CharField(max_length=160, blank=True)
    national_id = models.CharField(max_length=32, blank=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["national_id", "name", "mother_name"])]

    def __str__(self) -> str:
        return self.name
