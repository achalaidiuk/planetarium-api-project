import socket
import time
import os

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Waits for database to be ready for connection"

    def handle(self, *args, **options):
        port = int(os.environ["POSTGRES_PORT"])

        db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Waiting for DB connection...")

        while True:
            try:
                db_socket.connect(("db", port))
                print("DB connection established.")
                db_socket.close()
                break
            except socket.error:
                time.sleep(0.1)
