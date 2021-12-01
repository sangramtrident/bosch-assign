from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, Group)
from django.core.validators import RegexValidator



PHONE_REGEX = '^[6-9][0-9]{9}$'

name_REGEX = '^[a-zA-Z ]*$'

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)
class UserManager(BaseUserManager):

    def create_superuser(self, name, phone, email, password=None):
        if not name:
            raise ValueError('Users must have a username')
        if not phone:
            raise ValueError('Users must have a phone')
        if not password:
            raise ValueError('Users must set the password')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            phone=phone,
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, name, phone, email, password=None):
        if not name:
            raise ValueError('Users must have a username')
        if not phone:
            raise ValueError('Users must have a phone')
        if not password:
            raise ValueError('Users must set the password')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            phone=phone,
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=30, blank=False, validators=[RegexValidator(
        regex=name_REGEX,
        message='name must be Alphabetic only',
        code='invalid_first_name'
    )])
    email = models.EmailField(max_length=255, blank=False, unique=True)
    phone = models.CharField(max_length=10, blank=False, unique=True, validators=[RegexValidator(
        regex=PHONE_REGEX,
        message='invalid number',
        code='invalid_phone',
    )])
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)
    password = models.CharField(max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        full_name = self.name
        if full_name.strip() == "":
            return self.email + " - " + self.phone
        else:
            return full_name + " - " + self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
