
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ChangePasswordView,
                    NewPasswordCreateView, RestPasswordEmailView,
                    SuccessEmailView, UserView, Customtokencreate)

"""Create a default router of rest framework"""
router= DefaultRouter()
router.register("users",UserView,basename="users")

urlpatterns = [
   path("", include(router.urls)),
   path("api/", include("rest_framework.urls"),name= "api"),
   path("success/<uidb64>/<token>", SuccessEmailView.as_view(), name="success"),
   path('rest-auth/', include('rest_auth.urls')),
   path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   path("password-reset/", RestPasswordEmailView.as_view(),name= 'password-reset'),
   path("reset/<uidb64>/<token>/",NewPasswordCreateView.as_view(), name="reset"),
   path('token/',Customtokencreate.as_view(), name= 'token')
]

