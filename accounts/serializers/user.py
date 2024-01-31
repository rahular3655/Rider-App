from django.utils.translation import gettext_lazy
from accounts.models import User
from rest_framework import exceptions
from defender import utils as defender_utils
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    re_enter_password = serializers.CharField(write_only=True)

    def validate_username(self, username):
        """
        Custom validation method to check if the username already exists
        """
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail=gettext_lazy("Username already exists.")
            )

        return username

    def validate_email(self, email):
        """
        Custom validation method to check if the email already exists
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail=gettext_lazy("Email already exists.")
            )

        return email

    def validate(self, data):
        """
        the password is strong enough.
        """
        password = data.get('password')
        re_enter_password = data.get('re_enter_password')

        if password != re_enter_password:
            errors = {'password': gettext_lazy('Passwords do not match.')}
            raise exceptions.ValidationError(errors)

        return data

    def create(self, validated_data):
        """
        Create and return a new User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    """Validating user with username/email and password"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if defender_utils.is_already_locked(request=self.context.get('request'), username=username):
            raise exceptions.PermissionDenied(detail=gettext_lazy(
                "Your account is blocked due to too many failed login attempts. Please try again later."),
                code='account_blocked')

        user = authenticate(username=username, password=password)

        if not user:
            """
            Checking the user is already block or not.And if there is too many
            attempts the user will be blocked using django defender
            """
            defender_utils.add_login_attempt_to_db(self.context.get('request'), login_valid=False, username=username)
            ip_address = defender_utils.get_ip(self.context.get('request'))
            defender_utils.record_failed_attempt(ip_address, username)

            raise exceptions.AuthenticationFailed(detail=gettext_lazy('Invalid Credentials'))

        if user.is_deleted:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Invalid Credentials."))

        if not user.is_active:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Your account is not activated."), code='account_inactive')

        attrs['user'] = user
        return attrs