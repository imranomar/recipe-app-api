"""
Djago command to waui for the daabase to be availabel

"""
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    #gets called when we run django command
    def handle(self,*args, **options):
        self.stdout.write('Waiting for db...')
        db_up  = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up  = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second')
                time.sleep(1)

        #stykle.success is to get green color - optional
        self.stdout.write(self.style.SUCCESS('Database available!'))

