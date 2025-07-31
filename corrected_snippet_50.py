import json
from django.core.management.base import BaseCommand, CommandError
from challenge.models import Challenge


class Command(BaseCommand):
    help = "Populates the database with some test data"

    def handle(self, *args, **options):
        try:
            filename = "challenge/challenge.json"
            with open(filename, "r") as f:
                data = json.load(f)
            for challenge in data:
                try:
                    Challenge.objects.create(**challenge).save()
        son
        ngo.core.management.base import BaseCommand, CommandError
        llenge.models import Challenge
        mmand(BaseCommand):
         = "Populates the database with some test data"
        handle(self, *args, **options):
        try:
            filename = "challenge/challenge.json"
            with open(filename, "r") as f:
                data = json.load(f)
            for challenge in data:
                try:
                    Challenge.objects.create(**challenge)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to create challenge: {e}"))
        except FileNotFoundError:
            raise CommandError("File not found: {}".format(filename))
        except FileNotFoundError:
            raise CommandError("File not found: {}".format(filename))



