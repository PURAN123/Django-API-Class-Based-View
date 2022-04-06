
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ChangePasswordView, CustomLoginTokenView, CustomLogoutView,
                    GroupView, ResetNewPasswordView, SchoolView,
                    SendRestPasswordEmailView, SuccessEmailView,
                    TeacherListView, UserView)

"""Create a default router of rest framework"""
router= DefaultRouter()
router.register("users",UserView,basename="users")
router.register("school",SchoolView,basename="school")
router.register("group",GroupView,basename="group")

urlpatterns = [
   path("", include(router.urls)),
   path("success/<uidb64>/<token>", SuccessEmailView.as_view(), name="success"),
   path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   path("reset-password/", SendRestPasswordEmailView.as_view(),name= 'reset-password'),
   path("reset/<uidb64>/<token>/",ResetNewPasswordView.as_view(), name="reset"),
   path('login/',CustomLoginTokenView.as_view(), name= 'login'),
   path('logout/',CustomLogoutView.as_view(), name= 'logout'),
   path('teacher/',TeacherListView.as_view(),name='teacher')
]
