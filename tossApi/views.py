from django.shortcuts import render ,get_object_or_404
import random
from .serializer import (
    CoinModelSerializer,TossSerializer,ResultSerializer
)
from .models.toss import Toss
from .models.result import Result
from .models.coin import CoinModel
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics,status,response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import logging

logger =logging.getLogger(__name__)
User = get_user_model

# Create your views here. 
class CoinListView(generics.ListAPIView):
    queryset = CoinModel.objects.all()
    serializer_class = CoinModelSerializer

class CoinDetailView(generics.RetrieveAPIView):
    queryset = CoinModel.objects.all()
    serializer_class = CoinModelSerializer
    # lookup_field = 'coin_sides'

class TossApiView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Toss.objects.all()
    serializer_class = TossSerializer
    def user_input_validations(self,request):
        user = self.request.user 
        stake = self.request.data.get('staked_amount') 
        side_predicted = self.request.data.get('predicted_side')
 
        if not side_predicted:
            raise ValidationError({'Error: Invalid Predicted Side'},status.HTTP_400_BAD_REQUEST)
        if not stake:
            raise ValidationError({'Error: Provide a stake amount'},status.HTTP_400_BAD_REQUEST)
        try:
            stake = float(stake)
            if stake <= 0:
                raise ValidationError({'Error: Stake amount must be a Positive Number'},status.HTTP_400_BAD_REQUEST)
        except ValueError:
            raise ValidationError({'Stake only accepts a numbers'},status.HTTP_400_BAD_REQUEST)
        
    def user_prediction(self,side):
        try:
            user_predicted_side = get_object_or_404(CoinModel,id=side)
            print(f"Predicted side value: {user_predicted_side}")
            return user_predicted_side
        except Exception as e:
            raise ValidationError({'Error': 'Invalid Predicted Side'}, status.HTTP_400_BAD_REQUEST)

    
    

    def coin_toss(self,predicted_side):
        user = self.request.user
        if not user.is_authenticated:
            raise ValidationError({'Error: User must login'})
        toss_result= random.choice([side.coin_sides for side in CoinModel.objects.all()])
        win = toss_result == predicted_side.coin_sides
        return toss_result,win
    
    def post(self,request):
        try:
            self.user_input_validations(request)
            staker = request.user
            amount_staked = Decimal(request.data.get('staked_amount'))
            prediction = self.user_prediction(request.data.get('predicted_side'))

            toss = Toss.objects.create(user=staker,staked_amount=amount_staked,predicted_side=prediction)
            result,win = self.coin_toss(prediction)
            result =  Result.objects.create(outcome=result, toss_status=win, toss=toss)
            if win:
                staker.balance += amount_staked * 2
            else:
                staker.balance -= amount_staked
            staker.save()
            return Response({
                'toss': TossSerializer(toss).data,
                'result': result.toss_status,
                'outcome': result.outcome,
                'Balance': staker.balance,
            }, status=status.HTTP_201_CREATED,)
        
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error: An unexpected error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TossDetailView(generics.RetrieveAPIView):
    queryset = Toss.objects.all()
    serializer_class = TossSerializer

class ResultApiView(generics.RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer