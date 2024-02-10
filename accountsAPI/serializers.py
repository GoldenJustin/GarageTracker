from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from uuid import uuid4

class ownerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Owner.objects.all())]
    )
    owner_code = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Owner.objects.all())]
    )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = Owner
        fields = ('owner_code', 'email', 'password', 'first_name', 'middle_name', 'last_name', 'gender', 'expdate', 'programme', 'signature', 'avatar')

class technicianSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=technician.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=technician.objects.all())]
    )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = technician
        fields = ('username', 'email', 'password')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        if not username and not password:
            raise ValidationError("Details not entered.")
        owner = owner.objects.filter(
            owner_code=username,
            password=password
        ).first()
        technician = technician.objects.filter(
            username=username,
            password=password
        ).first()
        if not owner and not technician:
            raise ValidationError("User credentials are not correct.")
        if owner and owner.ifLogged:
            raise ValidationError("User already logged in.")
        if technician and technician.ifLogged:
            raise ValidationError("User already logged in.")
        if owner:
            data['token'] = str(uuid4())
            data['role'] = 'owner'  
            owner.ifLogged = True
            owner.token = data['token']
            owner.save()
        else:
            data['token'] = str(uuid4())
            data['role'] = 'technician'  
            technician.ifLogged = True
            technician.token = data['token']
            technician.save()
        return data


class UserLogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        owner = owner.objects.filter(token=token).first()
        technician = technician.objects.filter(token=token).first()
        if not owner and not technician:
            raise ValidationError("User is not logged in.")
        if owner:
            owner.ifLogged = False
            owner.token = ""
            owner.save()
        else:
            technician.ifLogged = False
            technician.token = ""
            technician.save()
        data['status'] = "User is logged out."
        return data


class NumberSerializer(serializers.Serializer):
    number = serializers.IntegerField()