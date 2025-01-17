from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import status


class CustomResponse:

    def list(data, message="success"):
        return Response(
            {
                "status": "success",
                "message": _(message),
                "results": data,
            },
            data=data,
            status=status.HTTP_200_OK,
        )

    def retrieve(message, data):
        return Response(
            {
                "status": "success",
                "message": _(message),
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def created(message, data, headers=None):
        return Response(
            {
                "status": "success",
                "message": _(message),
                "results": data,
            },
            status=status.HTTP_201_CREATED,
            # headers=headers,
        )

    def updated(message, data):
        return Response(
            {
                "status": "success",
                "message": _(message),
                "results": data,
            },
            status=status.HTTP_200_OK,
        )

    def deleted(message):
        return Response(
            {
                "status": "success",
                "message": _(message),
            },
            status=status.HTTP_200_OK,
        )

    def ok(message):
        return Response(
            {
                "status": "success",
                "message": _(message),
            },
            status=status.HTTP_200_OK,
        )

    def bad_request(message):
        return Response(
            {
                "status": "error",
                "message": _(message),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def unauthorized(message):
        return Response(
            {
                "status": "error",
                "message": _(message),
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def not_found(message):
        return Response(
            {
                "status": "error",
                "message": _(message),
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    def method_not_allowed(message):
        return Response(
            {
                "status": "error",
                "message": _(message),
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def serializers_erros(errors):
        errors = errors.items()
        for key, val in errors:
            print(key, val)
        return Response(
            {
                "status": "error",
                "message": f"{[val for key, val in errors][0][0]} ({[key for key, val in errors][0]})",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def jwt(refresh):
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
