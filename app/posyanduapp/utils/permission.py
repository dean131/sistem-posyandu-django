from django.middleware.csrf import _compare_salted_tokens, rotate_token
from rest_framework.permissions import BasePermission


class HasCsrfTokenValid(BasePermission):
    def has_permission(self, request, view):
        token_valid = False
        try:
            csrf_token = request.headers.get("api-csrftoken")
            csrf_cookie = request.META.get("CSRF_COOKIE")

            """
            Check if both alphanumerics(strings) values are differents to prevent 
            a malicious user get the csrf cookie and send it from the ajax.
            """
            if csrf_token == csrf_cookie:
                rotate_token(request)
                return False

            token_valid =  _compare_salted_tokens(csrf_token, csrf_cookie)
        except ValueError: # if csrf_token & csrf_cookie are not a valid alphanumeric
            return False
        return token_valid