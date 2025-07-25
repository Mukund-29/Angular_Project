from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class EmployeeUserManager(BaseUserManager):
    def create_user(self, NTID, Email_Id, password=None, **extra_fields):
        if not NTID:
            raise ValueError("The NTID is required")
        if not Email_Id:
            raise ValueError("The Email_Id is required")

        Email_Id = self.normalize_email(Email_Id)
        user = self.model(NTID=NTID, Email_Id=Email_Id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, NTID, Email_Id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError('Superuser must have a password.')

        return self.create_user(NTID, Email_Id, password, **extra_fields)


class Unit(models.Model):
    Unit_Id = models.AutoField(primary_key=True)
    Unit_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Unit_Name


class Employee(AbstractBaseUser, PermissionsMixin):
    Employee_Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email_Id = models.EmailField(unique=True)
    Unit_Name = models.CharField(max_length=100)
    IsActive = models.BooleanField(default=True)
    PhotoFileName = models.CharField(max_length=100, blank=True, null=True)

    # Auth fields
    NTID = models.CharField(max_length=15, unique=True)  # Used as username
    password = models.CharField(max_length=128, default='')  # Required by AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = EmployeeUserManager()

    USERNAME_FIELD = 'NTID'
    REQUIRED_FIELDS = ['Email_Id', 'First_Name', 'Last_Name']

    def __str__(self):
        return self.NTID
