
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
   """ Create a custom command to add default groups """
   def handle(self, *args, **options):
      groups= ['Coach','Teacher']
      for group in groups:
         try:
            group_instance, created= Group.objects.get_or_create(name= group)
            if created:
               self.stdout.write(self.style.SUCCESS("Groups " + group +" created successfully"))
            else:
               self.stdout.write(self.style.WARNING(group +" already exists"))
         except:
            raise CommandError(group+" already registered")
