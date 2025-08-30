from datetime import datetime, timedelta
from django.shortcuts import render , get_object_or_404
from rest_framework import viewsets , status , mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import action , api_view
from django.utils.crypto import get_random_string 
from django.core.mail import send_mail

from .serializers import SignUpSerializer , UserSerializer , UserUpdateSerializer

# Create your views here.

class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class CurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self , request , *args , **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# class UpdateUserViewSet(mixins.UpdateModelMixin,viewsets.GenericViewSet):
#     serializer_class = UserUpdateSerializer
#     permission_classes = [IsAuthenticated]
#     def get_object(self):
#         return self.request.user

class UpdateUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['put', 'patch'])
    def update_user(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol , host=host)


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User , email=data['email'])
    token = get_random_string(40)
    exprire_date = datetime.now()+timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = exprire_date
    user.profile.save()
    host = get_current_host(request)
    link = "http://127.0.0.1:8000/account/reset_password/{token}".format(token=token)
    body = "Your Password Reset Link is : {link}".format(link=link)
    send_mail(
        "password Reset From E_Market",
        body,
        "E_Market@gmail.com",
        [data['email']],
    )
    return Response({'details': 'Password Reset Sent To {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_password(request , token):
    data = request.data
    user = get_object_or_404(User , profile__reset_password_token = token)
    
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token Is Expire'} , status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']: 
        return Response({'error': 'Password Are Not Same'} , status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({'details': 'Password Reset Successfully'})




