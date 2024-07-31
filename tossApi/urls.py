from django.urls import path
from .views import *

urlpatterns = [
    path('coin/',CoinListView.as_view(),name='coin-list'),
    path('coin-detail/<int:pk>/',CoinDetailView.as_view(),name='coin-detail'),
    path('toss/',TossApiView.as_view(),name='toss'),
    path('toss-detail/<int:pk>',TossDetailView.as_view()),
    path('result/<int:pk>/',ResultApiView.as_view(),name='result'),

]
