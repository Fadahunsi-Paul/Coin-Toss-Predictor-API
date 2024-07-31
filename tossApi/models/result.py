from django.db import models
from tossApi.basemodels import TimeBaseModel
from tossApi.models.toss import Toss


class Result(TimeBaseModel):
    outcome = models.CharField(max_length=4)
    toss = models.OneToOneField(Toss, on_delete=models.CASCADE) 
    toss_status = models.BooleanField(default=False)


    def __str__(self):
        return f"Toss ID {self.toss.toss_id} --- Outcome {self.outcome} --- Status {self.toss_status}"
    