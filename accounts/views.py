# accounts/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken

#Registeration view for to register user
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # No authentication required for registration
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Login view
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # No authentication required for login
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])  # Authentication required for profile
def profile(request):
    if request.method == 'GET':
        user_data = {
            "username": request.user.username,

        }
        return Response(user_data)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
