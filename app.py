from csv_handler import Csv

from collections import OrderedDict
import sys

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db

def import_csv():
    csv_obj = Csv('inventory.csv')
    cleaned_csv = csv_obj.clean_csv()
    
    for row in cleaned_csv:
        print(row)
        Product.create(product_name=row['product_name'])
        Product.create(product_quantity=row['product_quantity'])
        Product.create(product_price=row['product_price'])
        Product.create(date_updated=row['date_updated'])

def initialize():
    db.connect()
    db.create_tables([Product], safe=True)

if __name__ == '__main__':
    initialize()
    import_csv()