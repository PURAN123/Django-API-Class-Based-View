
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
   def add_arguments(self, parser):
      parser.add_argument("group",type=str)

   def handle(self, *args, **options):
      try:
         grp = Group.objects.create(name=options['group'])
         self.stdout.write(self.style.SUCCESS("Group '"+ options["group"]+"' created successfully"))
      except:
         raise CommandError
