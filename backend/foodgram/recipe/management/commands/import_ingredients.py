import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('Файл ingredients.csv уже загружен.')
        else:
            with open(
                os.path.join(
                    settings.BASE_DIR, 'data/ingredients.csv'
                ), newline=''
            ) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)
                for row in reader:
                    Ingredient.objects.create(
                        name=row[0],
                        units=row[1],
                    )
        print('Файл ingredients.csv загружен.')
