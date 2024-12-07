from rest_framework import serializers
from .models import NewUser

class regSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password':{'write_only':True}}

        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['user_name', 'first_name', 'last_name', 'email', 'bio', 'pen_name', 'start_date']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['bio', 'pen_name'] 
