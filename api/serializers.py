from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.invite import Invite
from .models.profile import Profile
from .models.user import User

class InviteSerializer(serializers.ModelSerializer):
    user_host_id = serializers.StringRelatedField()
    user_friend_id = serializers.StringRelatedField()
    class Meta:
        model = Invite
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # this utilizes the custom related_name set on the model Profile
    # by running through the serializer, we have access to all the fields
    user_profiles = ProfileSerializer(many=True, read_only=True)
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
