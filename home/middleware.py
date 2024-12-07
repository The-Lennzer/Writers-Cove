from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages


class JWTTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')

        # if request.path in ['/auth/login/', '/auth/logout/']:
        #     return None
        # if not access_token:
        #     # If no token is found, redirect to login page
        #     msg = messages.error(request, "Please log in to continue.")  # Optional message
        #     return redirect('login')
        
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            
