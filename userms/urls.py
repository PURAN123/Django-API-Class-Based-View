
from django.contrib import admin
from django.urls import path,include
# from rest_framework.routers import DefaultRouter1
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ums.urls")),
]
