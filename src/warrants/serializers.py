from rest_framework import serializers
from .models import Warrant, WarrantList, WarrantMembership

class WarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrant
        fields = ["id","number","court","status"]

class WarrantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantList
        fields = ["id","name","uploaded_at","file_name"]

class WarrantMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantMembership
        fields = ["id","person","warrant","list","created_at"]
