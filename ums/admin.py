from django.contrib import admin

from ums.models import School, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display= ["email",'id',"username",'school','groups']

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
   list_display=['name','id']
