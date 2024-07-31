from rest_framework import serializers
from tossApi.models.coin import CoinModel
from tossApi.models.toss import Toss
from tossApi.models.result import Result


class CoinModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinModel
        fields = '__all__'

class TossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toss
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'