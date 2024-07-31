from django.contrib import admin
from django.contrib.auth.models import Group
from tossApi.models.coin import CoinModel
from tossApi.models.toss import Toss
from tossApi.models.result import Result

# Register your models here.
@admin.register(CoinModel)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('coin_sides',)
    search_fields = ('coin_sides',)

@admin.register(Toss)
class TossAdmin(admin.ModelAdmin):
    list_display = ('toss_id', 'user','predicted_side','staked_amount')
    search_fields = ('toss_id','user')
    list_filter = ('toss_id',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=('toss','outcome','toss_status')
    search_fields = ('outcome', 'toss_status')
    list_filter = ('outcome',)