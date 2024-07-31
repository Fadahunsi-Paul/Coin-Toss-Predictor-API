from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from .serializer import RegistrationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.

User = get_user_model()
@method_decorator(csrf_exempt,name='dispatch')
class UserRegistrationViewset(viewsets.ViewSet):
    serializer_class = RegistrationSerializer


    @action(detail=False,methods=['post'],permission_classes = [AllowAny])
    @method_decorator(csrf_exempt)
    def register(self,request):
        try:
            email            = request.data.get('email')
            password         = request.data.get('password')
            confirm_password = request.data.get('confirm_password')

            if not all([email,password,confirm_password]):
                return Response({'Error: All Inputs Should Be Provided'},status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'Error: Email already exists'},status=status.HTTP_400_BAD_REQUEST)
            if password != confirm_password:
                return Response({'Error: Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)
            
            if email and password:
                user = User.objects.create_user(
                    email = email,
                    password = password
                )
                user.save()
                return Response({'Account Created Successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({"Error: Email and Password Should be Provided"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
    @action(detail=False,methods=['post'],permission_classes = [IsAuthenticated])   
    @method_decorator(csrf_exempt)
    def logout(self,request):
        logout(request)
        return Response({'Logout Successful'},status=status.HTTP_200_OK)
        
@method_decorator(csrf_exempt,name='dispatch')
class LoginViewset(viewsets.ViewSet):
    serializer_class = LoginSerializer
    

    @action(detail=False,methods=['post'],permission_classes = [AllowAny])
    def login(self,request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request,email=email,password=password)
            
            if user:
                if user.is_active:
                    login(request,user)
                    return Response({'Login Successful'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'Error: Account is Inactive'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'Error: Invalid Login Details Supplied'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': f'Internal Server Error:{str(e)}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False,methods=['post'],permission_classes = [IsAuthenticated])
    # @method_decorator(csrf_exempt)
    def logout(self,request):
        logout(request)
        return Response({'Logout Successful'},status=status.HTTP_200_OK)