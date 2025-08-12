from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Stock, Alert, TriggeredAlert
from .serializers import StockSerializer, AlertSerializer, TriggeredAlertSerializer, UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def stocks_list(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

class AlertListCreateView(generics.ListCreateAPIView):
    # queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

class TriggeredAlertListView(generics.ListAPIView):
    serializer_class = TriggeredAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TriggeredAlert.objects.filter(alert__user=self.request.user
                                             ).order_by('-triggered_at')