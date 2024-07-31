from django.db import models
from tossApi.basemodels import TimeBaseModel
from tossApi.models.coin import CoinModel
from django.contrib.auth import get_user_model
from account.models import User



class Toss(TimeBaseModel):
    toss_id = models.CharField(max_length=5,null=False,blank=False)
    predicted_side = models.ForeignKey(CoinModel, on_delete=models.CASCADE)
    staked_amount = models.DecimalField(max_digits=8,decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"User :{self.user.email} Predicted {self.predicted_side} with {self.staked_amount}"