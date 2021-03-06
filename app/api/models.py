# pylint: disable=missing-module-docstring
from unicodedata import category
from xml.dom.minidom import Identified
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    uid = models.AutoField(blank=False,
                               null=False,
                               primary_key=True,
                               auto_created=True)
    username = models.CharField(max_length=30,
                                blank=False,
                                null=False,
                                unique=True)
    password = models.TextField(blank=False, null=False, default=' ')
    user_nickname = models.CharField(max_length=30, blank=True, null=True)
    user_phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=30,
                              blank=False,
                              null=True,
                              unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    


class user_belong_home(models.Model):
    user_belong_home = models.AutoField(blank=False,
                                        null=False,
                                        primary_key=True,
                                        auto_created=True)
    uid = models.ForeignKey(User,
                                related_name='belong_home',
                                on_delete=models.CASCADE)
    home_id = models.ForeignKey('home_list',
                                related_name='belong_user',
                                on_delete=models.CASCADE)


class home_list(models.Model):
    home_id = models.AutoField(blank=False,
                               null=False,
                               primary_key=True,
                               auto_created=True)
    home_address = models.CharField(max_length=30,
                                    blank=False,
                                    null=False,
                                    default=' ')
    home_owner = models.ForeignKey(User, on_delete=models.CASCADE)


class device_type(models.Model):
    device_type_id = models.AutoField(blank=False,
                                      null=False,
                                      primary_key=True,
                                      auto_created=True)
    device_type_name = models.CharField(max_length=30, blank=False, null=False)
    device_type_description = models.CharField(max_length=30,
                                               blank=True,
                                               null=False)
    category = models.ForeignKey('category_detail', on_delete=models.CASCADE)


class added_device_list(models.Model):
    added_device_id = models.AutoField(blank=False,
                                       null=False,
                                       primary_key=True,
                                       auto_created=True)
    added_time = models.DateTimeField(auto_now=True)
    home_id = models.ForeignKey(home_list, on_delete=models.CASCADE)
    device_type_id = models.ForeignKey(device_type, on_delete=models.CASCADE)


class alive_verification_code(models.Model):
    alive_verification_code_id = models.AutoField(blank=False,
                                                  null=False,
                                                  primary_key=True,
                                                  auto_created=True)
    type = models.CharField(max_length=30, blank=False, null=False)
    verification_code = models.IntegerField(blank=False, null=False)
    start_time = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50, blank=False, null=False)


class category_detail(models.Model):
    category_id = models.AutoField(blank=False,
                                   null=False,
                                   primary_key=True,
                                   auto_created=True)
    category_name = models.CharField(max_length=30, blank=False, null=False)
    category_description = models.CharField(max_length=30,
                                            blank=True,
                                            null=False)


class device_data(models.Model):
    device_data_id = models.AutoField(blank=False,
                                      null=False,
                                      primary_key=True,
                                      auto_created=True)
    device_id = models.ForeignKey(added_device_list, on_delete=models.CASCADE)
    device_type = models.ForeignKey(device_type, on_delete=models.CASCADE)
    data_value = models.CharField(max_length=30, blank=False, null=False)
    data_time = models.DateTimeField(auto_now_add=True)
