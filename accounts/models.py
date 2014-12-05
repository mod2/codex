from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
    email = models.EmailField('email address', unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        else:
            return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
