from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import *
from .serializers import *
from .forms import *




class ownerAPIView(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = ownerSerializer

class technicianAPIView(generics.CreateAPIView):
    queryset = technician.objects.all()
    serializer_class = technicianSerializer

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)

class UserLogoutAPIView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)

def index(request):
    return redirect('/user/login/')



def Home(request):

    return render(request, 'accountsAPI/base.html')


def owner_registration(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            owner = form.save()
            # You might want to implement email verification or other actions here
            return redirect('owner_login')  # Redirect to owner login page
    else:
        form = OwnerRegistrationForm()

    return render(request, 'accountsAPI/owner_registration.html', {'form': form})


def owner_login(request):
    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            owner = authenticate(request, email=email, password=password)
            if owner:
                login(request, owner)
                # Redirect to the owner's dashboard or any other page
                return redirect('owner_dashboard')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = OwnerLoginForm()

    return render(request, 'accountsAPI/owner_login.html', {'form': form})

def owner_dashboard(request):
    return render(request, 'accountsAPI/owner_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')




