from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    resume = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_type', 'resume')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_user_type(self, value):
        if value not in ['recruiter', 'job_seeker']:
            raise serializers.ValidationError("User type must be 'recruiter' or 'job_seeker'")
        return value

    def create(self, validated_data):
        resume = validated_data.pop('resume', None)
        user = User.objects.create_user(**validated_data)
        if resume:
            user.resume = resume
            user.save()
        return user
