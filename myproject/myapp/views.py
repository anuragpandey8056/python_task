from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

# API request function with error handling
def fetch_api_data():
    url = "https://api.restful-api.dev/objects?id=3&id=5&id=10"
    try:
        # Modify this if proxy settings are required
        proxies = None  # Set to {"https": "http://proxy_address:proxy_port"} if needed
        response = requests.get(url, proxies=proxies, timeout=10)  # Add a timeout for safety
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()  # Return the data
    except requests.exceptions.ProxyError:
        return {"error": "Proxy connection error. Please check proxy settings."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch API data: {str(e)}"}

# Fetch the data when the app starts
data = fetch_api_data()  # Store it in a global variable if reused

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Pass API data to the dashboard
            return render(request, 'dashboard.html', {'data': data})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Dashboard view (protected)
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'data': data})  # Pass data to the template

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Home view
def home_view(request):
    return render(request, 'home.html')

# Home view for login
def home_viewlog(request):
    return render(request, 'login.html')
