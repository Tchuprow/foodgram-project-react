import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            logging.error('Файл ingredients.csv уже загружен.')
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
                        measurement_unit=row[1],
                    )
        logging.info('Файл ingredients.csv загружен.')
