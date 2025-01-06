from django.shortcuts import render, HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework import generics,  status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


from userauths.models import User, Profile
from userauths.serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer, ProfileSerializer

import shortuuid
# Create your views here.

class MyTokenObtainPairView (TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Registerview(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes= (AllowAny, )
    serializer_class = RegisterSerializer

def generate_otp():
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:6]
    return unique_key

class PaswordResetEmailVerify(generics.RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp = generate_otp()
            user.save()

            uidb64 = user.pk 
            otp = user.otp

            link = f"http://localhost:5173/password-reset?otp={otp}&uidb64={uidb64}"
            print("link ====", link)

            #Send Email

        return user
    

class PasswordChangeView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uidb64 = payload['uidb64']
       
        password = payload['password']

        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
        else:
             return Response({"message": "An error occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']

        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        return profile