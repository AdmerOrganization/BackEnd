from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CurrentUserSerializer, EditSerializer, EmailVerificationSerializer, UserSerializer, SignUpSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .models import User, UserProfile
from rest_framework import generics, status
from django.conf import settings
from .serializers import UserSerializer, SignUpSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.template import loader
from django.http import HttpResponse

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

        subject = 'Verification'
        html_message = render_to_string(
            '1.html', {'nameholder': user.username, 'verifylink': absurl})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, html_message, from_email,
                       [to], html_message=html_message)

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
            template = loader.get_template("3.html")
            return HttpResponse(template.render(), status=status.HTTP_200_OK)
            # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
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
        profile = user.userprofile
        if profile.is_verified == False:
            return Response({'error': 'User not verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
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
            if(serializer.data.get("last_name") != None):
                self.object.last_name = (serializer.data.get("last_name"))
            self.object.save()

            profile = self.object.userprofile

            if(serializer.data.get("phone_number") != None):
                profile.phone_number = (serializer.data.get("phone_number"))
            try:
                if(serializer.validated_data["avatar"] != None):
                    profile.avatar = ((serializer.validated_data["avatar"]))
            except Exception as e:
                pass

            profile.save()

            self.object.save()

            return Response({
                "user": CurrentUserSerializer(self.object, context=self.get_serializer_context()).data,
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
