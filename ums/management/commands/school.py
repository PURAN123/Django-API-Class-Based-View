from django.core.management.base import BaseCommand,CommandError
from ums.models import School

class Command(BaseCommand):
   def add_arguments(self, parser):
      parser.add_argument("school",type=str)

   def handle(self, *args, **options):
      try:
         grp = School.objects.create(name=options['school'])
         self.stdout.write(self.style.SUCCESS("school '"+ options["school"]+"' created successfully"))
      except:
         raise CommandError