from .models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class EmailAuthBackend(object):
    """
    Custom authentication backend for logging in with an email address as the
    username.
    """
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None


class EmailAuthAPIBackend(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password):
        """Authenticate the userid and password against email and password."""
        backend = EmailAuthBackend()
        user = backend.authenticate(email=userid, password=password)
        if user is None or not user.is_active:
            raise AuthenticationFailed('Invalid email/password')
        return (user, None)
