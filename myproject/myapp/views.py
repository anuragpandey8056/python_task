from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import requests
url = "https://api.restful-api.dev/objects?id=3&id=5&id=10"
r = requests.get(url)
data = r.json()
print(data)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('dashboard')
            return render(request,'dashboard.html',{'data':data})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')


def home_viewlog(request):
    return render(request, 'login.html')
