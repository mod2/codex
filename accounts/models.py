from __future__ import unicode_literals

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from model_utils import Choices


def _generate_password():
    return '1234567890'


def send_invite_email(user, password):
    subject = "[Codex] Invite to help transcribe"

    msg = """
    <p>You've been invited to use Codex.</p>

    <p>
    Email/username: <b>{email}</b><br/>
    Password: <b>{password}</b> (change this!)
    </p>

    <p><a href="localhost:8000/accounts/password/change/">Log in and change password</a></p>
    """.format(email=user.email, password=password)

    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [user.email]

    send_mail(subject, msg, from_email, to_emails, html_message=msg, fail_silently=False)


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_active, is_admin, **kwargs):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=is_active,
                          is_admin=is_admin,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, True, **kwargs)


class User(AbstractBaseUser):
    """
    Custom user class with email as the username and simplified a little.
    """
    LAYOUTS = Choices(('side_by_side', 'Side By Side'), ('stacked', 'Stacked'))
    THEMES = Choices(('light', 'Light'), ('dark', 'Dark'))
    email = models.EmailField('email address', unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True,
                                       default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    layout = models.CharField(max_length=12, default=LAYOUTS.side_by_side,
                              choices=LAYOUTS)
    theme = models.CharField(max_length=5, default=THEMES.light, choices=THEMES)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return "{0.name} ({0.email})".format(self) if self.name else self.email

    def get_short_name(self):
        return self.name if self.name else self.email

    def __unicode__(self):
        return self.name if self.name else self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @classmethod
    def create_new_user(cls, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            password = _generate_password()
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
            send_invite_email(user, password)
        return user

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def has_logged_in(self):
        return not (self.last_login - self.date_joined) < timedelta(seconds=2)
