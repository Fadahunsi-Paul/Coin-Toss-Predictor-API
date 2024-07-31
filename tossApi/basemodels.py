from django.db import models

# Create your models here.
class TimeBaseModel(models.Model):
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated at', auto_now_add=True)

    class Meta:
        abstract =True