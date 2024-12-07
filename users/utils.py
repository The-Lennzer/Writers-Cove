from rest_framework.views import exception_handler
from django.shortcuts import redirect
from django.contrib import messages

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response)
    if response is not None and response.status_code == 401:
        # Add a message before redirecting to the login page
        request = context['request']  # Extract the request object from context
        messages.error(request, "Your session has expired. Please log in again.")
        return redirect('login')

    return response
