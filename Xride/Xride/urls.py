"""
URL configuration for Xride project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Auth_V0.views import CustomTokenCreateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin Dashboard
    path('admin/', admin.site.urls),
    # Xride APP
    path('V3/',include('ride_V3.urls')),
    # Djoser & JWT Token obtain URLs
    path('auth/', include('djoser.urls')),
    path('auth/',include('Auth_V0.urls')),
    # JWT Token URLs
    path('auth/jwt/create/', CustomTokenCreateView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# path('V0',include('ride_V0.urls')),
# path('V1/',include('ride_V1.urls')),
# path('V2/',include('ride_V2.urls')),
# path('auth/', include('djoser.urls.jwt')),