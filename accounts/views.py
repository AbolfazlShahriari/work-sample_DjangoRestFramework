from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        ser_data = UserSerializer(instance=User.objects.all(), many=True)
        return Response(data=ser_data.data)

    def retrieve(self, request, pk):
        query = get_object_or_404(User, pk=pk)
        ser_data = UserSerializer(instance=query)
        return Response(data=ser_data.data)

    def partial_update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        ser_data = UserSerializer(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data)
        return Response(data=ser_data.errors)


    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        user.is_active = False
        user.save()
        return Response({'message': 'user activated'})
