from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class PreventBackNavigationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # If the user is authenticated and tries to access the login page, redirect to the dashboard
        if request.user.is_authenticated and request.path == '/login/':
            return redirect('/dashboard/')

    def process_response(self, request, response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
