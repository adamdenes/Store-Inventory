from csv_handler import CSV

from collections import OrderedDict
import sys

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)