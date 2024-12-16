from django.shortcuts import redirect
from django.conf import settings
import re

class HtmlRedirectMiddleware:
    """
    Middleware to remove `.html` from the requested URL and redirect to the cleaned path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and re.search(r'\.html/?$', request.path):
            if request.path.startswith('/static/') or request.path.startswith('/media/'):
                return self.get_response(request)

            new_path = re.sub(r'\.html/?$', '/', request.path)
            if new_path != request.path:  
                return redirect(new_path)

        return self.get_response(request)


class LoginRequiredMiddleware:
    """
    Redirect unauthenticated users to the login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            settings.LOGIN_URL,  
            '/register/',  
            '/static/', 
            '/media/',  
            '/admin/',  
        ]

        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in exempt_urls):
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
