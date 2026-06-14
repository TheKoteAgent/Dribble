from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Паролі не співпадають.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

class UserProfileSerializer(serializers.ModelSerializer):
    shots_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'avatar', 'bio',
            'website', 'twitter', 'instagram', 'linkedin',
            'shots_count', 'followers_count', 'following_count'
        )
        read_only_fields = ('id', 'email', 'shots_count', 'followers_count', 'following_count')

    def get_shots_count(self, obj):
        return getattr(obj, 'shots_count_cached', 0)

    def get_followers_count(self, obj):
        return getattr(obj, 'followers_count_cached', 0)

    def get_following_count(self, obj):
        return getattr(obj, 'following_count_cached', 0)