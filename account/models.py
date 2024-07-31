from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .usermanager import myUserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address: '),unique=True) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = myUserManager()
    

    def __str__(self):
        return self.email if self.email else ''
