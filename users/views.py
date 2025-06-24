from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer


from users.models import User
from users.serializers import UserSerializers

# Create your views here.
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([AllowAny])
def user_list_view(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response('Unauthenticated user', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'admin':
            users = User.objects.all()
        else:
            users = User.objects.filter(id=request.user.id)

        serializer = UserSerializers(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response('Unauthenticated user', status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializers(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)