from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import PasswordResetSerializer

User = get_user_model()


def password_reset_url_generator(request, user, temp_key):
    """Посилання веде на фронтенд: /forgot-password/confirm?uid=...&token=..."""
    return f"{settings.FRONTEND_URL}/forgot-password/confirm?uid={user_pk_to_url_str(user)}&token={temp_key}"


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {'url_generator': password_reset_url_generator}

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
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'avatar', 'bio',
            'website', 'twitter', 'instagram', 'linkedin',
            'shots_count', 'followers_count', 'following_count', 'is_following'
        )
        read_only_fields = ('id', 'email', 'shots_count', 'followers_count', 'following_count', 'is_following')

    def get_shots_count(self, obj):
        return obj.shots.count()

    def get_followers_count(self, obj):
        return obj.followers_set.count()

    def get_following_count(self, obj):
        return obj.following_set.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers_set.filter(follower=request.user).exists()
        return False


class FollowUserSerializer(serializers.ModelSerializer):
    """Мінімальний профіль для списків followers/following."""
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'bio')
