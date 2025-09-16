from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id","name","mother_name","national_id","birth_date","sex","created_at"]
