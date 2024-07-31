from typing import Any
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class myUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_("Email fields shouldn't be blank"))
        if len(password) < 8:
            raise ValueError(_('Password should have at least 8 characters'))
        if '@' not in email or '.com' not in email:
            raise ValueError(_('Email should contain @ and .com'))
        
             
        user = self.model(email = self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_superuser") != True:
            raise ValueError(_("Superuser should have is_superuser = True"))
        if extra_fields.get("is_staff") != True:
            raise ValueError(_("Superuser should have is_staff = True"))
        if extra_fields.get("is_active") != True:
            raise ValueError (_("Superuser should have is_active = True")) 
        return self.create_user(email,password, **extra_fields)
    
