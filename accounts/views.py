from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import CurrentUserSerializer, EditSerializer, EmailVerificationSerializer, UserSerializer, SignUpSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .models import User, UserProfile
from rest_framework import generics, status
from django.conf import settings
from .serializers import UserSerializer, SignUpSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.fields import CharField, EmailField, ImageField
from rest_framework.permissions import IsAuthenticated 
from datetime import datetime

# Return Current User API
class CurrentUserAPI(generics.GenericAPIView):
    
    serializer_class = CurrentUserSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# Register API
class SignUpAPI(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        profile = UserProfile(user=user)
        profile.save()

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'سلام '+user.username + '\n' +\
            ' لطفا از لینک زیر برای تایید ایمیل خود استفاده کنید \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,

        })


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 'HS256')
            user = User.objects.get(id=payload['user_id'])
            profile = user.userprofile
            profile.is_verified = True
            profile.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

class SigninAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(SigninAPI, self).post(request, format=None)


class EditAPI(generics.UpdateAPIView):
    serializer_class = EditSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if(serializer.data.get("email") != None and serializer.data.get("email") != ""):
                self.object.email = (serializer.data.get("email"))
            if(serializer.data.get("first_name") != None):
                self.object.first_name = (serializer.data.get("first_name"))
            if(serializer.data.get("last_name") != None ):
                self.object.last_name = (serializer.data.get("last_name"))
            self.object.save()

            profile = self.object.userprofile

            if(serializer.data.get("phone_number") != None ):
                profile.phone_number = (serializer.data.get("phone_number"))
            try:
                if(serializer.validated_data["avatar"] != None ):
                    profile.avatar = ((serializer.validated_data["avatar"]))
            except Exception as e:
                pass

            profile.save()
            
            self.object.save()


            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Profile updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
