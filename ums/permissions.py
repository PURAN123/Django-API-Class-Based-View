
from rest_framework import permissions



class CustomPermissionUser(permissions.BasePermission):
   """Set the permission that a authenticated user can not make post request and """
   def has_permission(self, request, view):
      if request.method=="POST" and request.user.is_authenticated:
         return False
      return True

   def has_object_permission(self, request, view, obj):
      """An special User can access its own data and update and delete its data but can't access other user's data
      Give super user all permission to make changes with the data"""
      if request.user.is_superuser:
         return True
      #"""Restrict the user to make change the other user data But it can change its own data"""
      elif request.user.is_authenticated and obj.id == request.user.id:
         return True
      return False



class CustomPermissions(permissions.BasePermission):
   def has_permission(self, request, view):
      """Super user can perform all tasks and authenticate user
       has view permission and unauthenticate user has no any permission"""
      if request.method == "POST":
         if not request.user.is_superuser:
            return False
      if not request.user.is_authenticated:
         return False
      return True

   def has_object_permission(self, request, view, obj):
      """Only super user can modify object data not other user"""
      if request.user.is_superuser:
         return True
      return False