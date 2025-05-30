from rest_framework import status
from rest_framework.response import Response


def get_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)

    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token

    return Response({'error': 'Authorization header missing or invalid'},
                    status=status.HTTP_401_UNAUTHORIZED)
