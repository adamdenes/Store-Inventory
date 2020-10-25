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
            # if data already exist, do not add extra rows
            Product.get_or_create(**data)


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


def menu():
    menu_choices = OrderedDict([
        ('a', add_record),
        ('v', view_record),
        ('b', backup_data)
    ])

    option = None

    while option != 'q':
        print('\nEnter "q" to quit!')

        for choice, operation in menu_choices.items():
            print(f'{choice} -> {operation.__doc__}')

        option = input('Option: ').lower().strip()

        if option in menu_choices:
            menu_choices[option]()


def add_record():
    """Add a record to the database"""
    pass


def view_record():
    """View a database record"""
    pass


def backup_data():
    """Backup database"""
    pass


if __name__ == '__main__':
    initialize()
    import_csv()
    menu()
