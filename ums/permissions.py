
from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
   """Set the permission that a authenticated user can not make post request and """
   def has_permission(self, request, view):
      if request.method=="POST" and request.user.is_authenticated:
         return False
      return True


   def has_object_permission(self, request, view, obj):
      """Give the authenticated user special permissions and avoide unautherized user to makechanges with registered API
      An special User can access its own data and update and delete iets data but can't access other user's data"""
      """Give super user all permission to make changes with the data"""
      if request.user.is_superuser:
         return True
      #"""Restrict the user to make change the other user data But it can change its own data"""
      elif request.method in permissions.SAFE_METHODS and request.user.is_authenticated and obj.username == request.user:
         return True

      return obj.id == request.user.id


class GroupSchoolPermissions(permissions.BasePermission):
   def has_permission(self, request, view):
      if request.method == "POST":
         if not request.user.is_superuser:
            return False
         return True
      if not request.user.is_authenticated:
         return False
      return True
   def has_object_permission(self, request, view, obj):
      if request.user.is_superuser:
         return True
      if request.method == "GET":
         return True
      if not request.user.is_authenticated:
         return False
      return False
      