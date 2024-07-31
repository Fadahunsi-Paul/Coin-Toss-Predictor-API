from django.db import models
from tossApi.basemodels import TimeBaseModel


COIN_SIDES = [
    ('Head', 'Head'),
    ('Tail', 'Tail') 
]
class CoinModel(TimeBaseModel):
    coin_sides = models.CharField(max_length=4,choices=COIN_SIDES)
    
    def __str__(self):
        return self.coin_sides if self.coin_sides else ''
    