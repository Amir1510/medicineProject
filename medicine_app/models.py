from django.db import models
from django.contrib.auth.hashers import make_password
from dirtyfields import  DirtyFieldsMixin
from django.contrib.auth.models import AbstractBaseUser


class CreateUser(DirtyFieldsMixin,AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if not self.pk or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
class Plan(models.Model):
    BLODD_CHOICES = [
        ('0+', '0+'),
        ('0-', '0-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ("B-", 'B-'),
        ("AB+", 'AB+'),
        ("AB-", 'AB-'),
    ]
    AGE_CHOICES = [(str(i), f"{i} лет") for i in range(0, 100)]
    HEIGHT_CHOICES = [(str(i), f"{i} см") for i in range(80, 201)]
    WEIGHT_CHOICES = [(str(i), f"{i} кг") for i in range(10, 201)]
    username = models.CharField(max_length=20, unique=True, default='default_username')
    weight = models.CharField(choices=WEIGHT_CHOICES, default='10')
    group_of_blood = models.CharField(max_length=10, choices=BLODD_CHOICES, default='0+')
    height = models.CharField(max_length=10, choices=HEIGHT_CHOICES, default='80')
    age = models.CharField(max_length=10, choices=AGE_CHOICES, default='0')


