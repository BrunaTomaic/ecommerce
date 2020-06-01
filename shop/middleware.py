import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout


# first example

# EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
# if hasattr(settings, 'LOGIN_EXEMPT_URL'):
#     EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URL]

# class AuthMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         assert hasattr(request, 'user')
#         path = request.path_info.lstrip('/')
#         url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

#         if path == reverse('shop:shop').lstrip('/'):
#             logout(request)

#         if request.user.is_authenticated and url_is_exempt:
#             return redirect(settings.LOGIN_EXEMPT_URL)

#         elif request.user.is_authenticated or url_is_exempt:
#             return None
        
#         else:
#             return redirect(settings.LOGIN_URL)