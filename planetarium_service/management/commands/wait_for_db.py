import time
import os

from django.core.management import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Waits for database to be ready for connection"

    def handle(self, *args, **options):
        db_name = os.environ["POSTGRES_DB"]

        print("Waiting for DB connection...")

        while True:
            try:
                connections[db_name].ensure_connection()
                print("DB connection established.")
                break
            except Exception:
                time.sleep(0.1)
