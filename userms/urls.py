
from django.contrib import admin
from django.urls import path,include
# from rest_framework.routers import DefaultRouter1
admin.site.site_header = 'User Management System'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ums.urls")),
]
