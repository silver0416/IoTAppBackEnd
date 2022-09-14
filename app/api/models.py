from email import message
from math import fabs
from pyexpat import model
from random import choices
from unicodedata import category
import uuid
from xml.dom.minidom import Identified
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from hashid_field import HashidAutoField
import  django.utils.timezone as timezone
from django.utils import timezone, dateformat
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")

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
    # user_uid = models.AutoField(
    # blank=False, null=False, primary_key=True, auto_created=True
    # )
    username = models.CharField(
        max_length=30, primary_key=True, blank=False, null=False, unique=True
    )
    password = models.TextField(blank=False, null=False, default=" ")
    user_nickname = models.CharField(max_length=30, blank=True, null=True)
    user_phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=False, null=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "使用者"
        verbose_name_plural = "使用者"


class home_list(models.Model):
    home_id = HashidAutoField(primary_key=True, min_length=8)
    home_name = models.CharField(max_length=30, blank=False, null=False)
    user = models.ManyToManyField(User, related_name="detail", blank=False)

    def __str__(self):
        return self.home_name

    class Meta:
        verbose_name = "家庭"
        verbose_name_plural = "家庭"


class home_admin(models.Model):
    id = models.AutoField(blank=False, null=False, primary_key=True, auto_created=True)
    home = models.OneToOneField(home_list, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"管理員ID: {self.home_id}\t家庭{self.home.home_id}: {self.home.home_name}\t管理員:{self.admin.email}"

    class Meta:
        verbose_name = "家庭管理員"
        verbose_name_plural = "家庭管理員"

class device_list(models.Model):
    id = models.UUIDField(
       default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    added_time = models.DateTimeField(default=timezone.now)
    type_name = models.CharField(max_length=30, blank=False, null=False)
    home = models.ForeignKey(home_list, on_delete=models.CASCADE)


class device_data(models.Model):
    home = models.ForeignKey(home_list, blank=False, on_delete=models.CASCADE)
    id = models.AutoField(
        blank=False, null=False, primary_key=True, auto_created=True
    )
    device = models.ForeignKey(device_list, on_delete=models.CASCADE)
    data_status = models.JSONField(null=False)
    data_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)


class mode_key_data(models.Model):
    mode_key_data_id = models.AutoField(
        blank=False, null=False, primary_key=True, auto_created=True
    )
    mode_key_name = models.CharField(
        max_length=30, blank=False, null=False, default=False
    )
    home_id = models.ForeignKey(home_list, on_delete=models.CASCADE)
    tplink_switch_mode_key = models.CharField(max_length=6, blank=False, null=False)
    ac_temperature = models.SmallIntegerField(blank=False, null=False, default=25)
    # ac_mode = models.CharField(max_length=6, blank=False, null=False, default="")
    ac_switch = models.BooleanField(blank=False, null=False, default=False)
    fan_level = models.SmallIntegerField(blank=False, null=False, default=1)
    fan_switch = models.BooleanField(blank=False, null=False, default=False)
    fan_spin = models.BooleanField(blank=False, null=False, default=False)
    mode_key_time = models.DateTimeField(auto_now_add=True)


class chat_room_data(models.Model):
    message_id = models.AutoField(
        blank=False, null=False, primary_key=True, auto_created=True
    )
    chat_room_name = models.CharField(max_length=30, blank=False, null=False)
    message = models.TextField(blank=False, null=False)


class chat_room(models.Model):
    chat_room_name = models.CharField(
        max_length=30, blank=False, null=False, primary_key=True
    )
    message = models.ManyToManyField(
        chat_room_data, related_name="chat_room_message", blank=False
    )
