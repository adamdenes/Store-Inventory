from csv_handler import Csv

from collections import OrderedDict
import sys

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField()

    class Meta:
        database = db


def import_csv():
    csv_obj = Csv('inventory.csv')
    cleaned_csv = csv_obj.clean_csv()

    # wrapping bulk insert transaction with atomic()
    # to speed up process
    with db.atomic():
        for data in cleaned_csv:
            Product.insert_many(data).execute()


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


if __name__ == '__main__':
    initialize()
    import_csv()
