
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AccountActivatedView, ChangePasswordView, GroupView,
                    LoginView, LogoutView, ResetPasswordView, SchoolView,
                    SendResetPasswordEmailView, UserView)

"""Create a default router of rest framework"""
router= DefaultRouter()
router.register("users",UserView,basename="users")
router.register("school",SchoolView,basename="school")
router.register("group",GroupView,basename="group")


urlpatterns = [
   path("", include(router.urls)),
   path("success/<uidb64>/<token>", AccountActivatedView.as_view(), name="success"),
   path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   path("reset-password/", SendResetPasswordEmailView.as_view(),name= 'reset-password'),
   path("reset/<uidb64>/<token>/",ResetPasswordView.as_view(), name="reset"),
   path('login/',LoginView.as_view(), name= 'login'),
   path('logout/',LogoutView.as_view(), name= 'logout'),
   path('rest-auth/', include('rest_auth.urls'))
]
