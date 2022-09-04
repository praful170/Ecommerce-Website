from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy

#To create automatically one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MyUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("Please input your email")

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("SuperUser must be is_staff")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("SuperUser must be is_superuser")

        return self.create_user(email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True,null=False)
    is_staff = models.BooleanField(
        gettext_lazy('Staff Status'),default=False,
        help_text = gettext_lazy('Designates whether the user can log in the site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=False,
        help_text = gettext_lazy('Designates whether the user should be treated as active')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

        def get_short_name(self):
            return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=250,blank=True)
    Full_name = models.CharField(max_length=100,blank=True)
    address_1 = models.CharField(max_length=300,blank=True)
    city = models.TextField(max_length=40,blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile"


    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    #function after profile is created

    @receiver(post_save,sender=User)
    def create_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_profile(sender,instance,**kwargs):
        instance.profile.save()
