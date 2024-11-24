''' Wait for the database to be ready '''

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from time import sleep


class Command(BaseCommand):
    """Command to wait for the database to be available."""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for the database...")
        db_ready = False
        while not db_ready:
            try:
                self.check(databases=['default'])
                db_ready = True
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is ready!"))
