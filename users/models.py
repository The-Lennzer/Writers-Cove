from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(('email address'), unique=True)
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    bio = models.TextField(('about'), max_length=350, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # refresh_token = models.TextField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self) -> str:
        return f"{self.user_name}"


    # username = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=100)
    # middle_name = models.CharField(max_length=100, blank=True, null=True)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # pen_name = models.CharField(max_length=100, blank=True, null=True)
    # dob = models.DateField(default=date.today)
    # password = models.CharField(max_length=100)
    # age = models.PositiveIntegerField(blank=True, null=True)

    # def save(self):
    #     from datetime import date
    #     if self.dob:
    #         today = date.today()
    #         self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    #     super().save()

    # def __str__(self):
    #     return self.username
