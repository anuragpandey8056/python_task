from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

# API request function with error handling
def fetch_api_data():
    url = "https://jsonplaceholder.typicode.com/users"  # Updated API URL
    try:
        # Make the GET request to the API
        response = requests.get(url, timeout=10)  # Set a timeout for safety
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()  # Return the JSON data
    except requests.exceptions.RequestException as e:
        # Handle API errors and return an error message
        return {"error": f"Failed to fetch API data: {str(e)}"}

# Fetch the data once for the application
data = fetch_api_data()

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return render(request, 'dashboard.html', {'data': data})  # Pass API data to the dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})  # Show an error
    return render(request, 'login.html')  # Render the login page for GET requests

# Dashboard view (requires login)
@login_required
def dashboard_view(request):
    # Render the dashboard page with API data
    return render(request, 'dashboard.html', {'data': data})

# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to the login page

# Home view (non-protected)
def home_view(request):
    return render(request, 'home.html')

# Redirect to login page (for non-logged-in users)
def home_viewlog(request):
    return render(request, 'login.html')
