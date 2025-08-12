from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stocks/', views.stocks_list, name='stocks-list'),
    path('alerts/', views.AlertListCreateView.as_view(), name='alerts-list-create'),
    path('alerts/<int:pk>/', views.AlertDetailView.as_view(), name='alert-detail'),
    path('triggered-alerts/', views.TriggeredAlertListView.as_view(), name='triggered-alerts'),
]