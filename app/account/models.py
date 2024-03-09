from random import randint

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, whatsapp, full_name, password=None):
        if not whatsapp:
            raise ValueError("Users must have an whatsapp number")

        user = self.model(
            whatsapp=whatsapp,
            full_name=full_name,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp, full_name, password=None):
        user = self.create_user(
            whatsapp=whatsapp,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        USER = "USER", "User"
        MIDWIFE = "MIDWIFE", "Midwife"
        PARENT = "PARENT", "Parent"
        CADRE = "CADRE", "Cadre"

    base_role = Role.USER

    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    role = models.CharField(max_length=10, choices=Role.choices, default=base_role, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "whatsapp"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"OTP for {self.user.full_name}"

    def generate_otp(self):
        self.otp = str(randint(100000, 999999))
        self.expired_at = timezone.now() + timezone.timedelta(minutes=5)
        self.save()
        return self.otp

    def validate_otp(self, otp):
        return self.otp == otp and self.expired_at > timezone.now()
    

class ParentManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.PARENT)


class MidwifeManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.MIDWIFE)


class CadreManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CADRE)
    

class Parent(User):
    base_role = User.Role.PARENT
    objects = ParentManager()

    class Meta:
        proxy = True 
    

class Midwife(User):
    base_role = User.Role.MIDWIFE
    objects = MidwifeManager()

    class Meta:
        proxy = True


class Cadre(User):
    base_role = User.Role.CADRE
    objects = CadreManager()

    class Meta:
        proxy = True


