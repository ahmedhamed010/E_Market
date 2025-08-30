from rest_framework import serializers
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password' , 'email']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }

    def create(self, validated_data):
        username = validated_data['email'].split('@')[0]  
        user = User(
            username=username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    def update(self , instance , validated_data):
        password = validated_data.pop('password' , None)
        for attr , value in validated_data.items():
            setattr(instance , attr , value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

