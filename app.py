from csv_handler import Csv

from collections import OrderedDict
import datetime
import sys
import re
import os

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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    menu_choices = OrderedDict([
        ('a', add_record),
        ('v', view_record),
        ('b', backup_data)
    ])

    option = None

    try:
        while option != 'q':
            print('\nEnter "q" to quit!')

            for choice, operation in menu_choices.items():
                print(f'{choice} -> {operation.__doc__}')

            try:
                option = input('Option: ').lower().strip()
                clear()

                if option not in ['a', 'b', 'v']:
                    raise ValueError(
                        'Please use the available options! ["a", "v", "b"]')

            except ValueError as ve:
                print(ve)

            if option in menu_choices:
                menu_choices[option]()

    except EOFError:
        print('\n\nApplication stoped with ctrl+d.\n\n')
        sys.exit()
    except KeyboardInterrupt:
        print(f'\n\nClosed application.\n\n')
        sys.exit()


def add_record():
    """Add a record to the database"""
    first_row = []
    answers = []

    for header in list(Product.select().dicts()):
        for key in header.keys():
            if key not in first_row:
                first_row.append(key)

    for answer in first_row[1:4]:
        while True:
            try:
                input_data = input(f'Enter {answer}: ')

                if answer == 'product_name':
                    if len(input_data) == 0:
                        raise ValueError('Empty field is not allowed')
                    elif re.match(r'\d+', input_data, re.I):
                        raise ValueError(
                            f'Numbers are not allowed for {answer}!')
                    elif re.match(r'[^\w_]', input_data, re.I):
                        raise ValueError(f'Only characters are accepted for {answer}!')
                    else:
                        answers.append(input_data)
                        break
                if answer == 'product_quantity':
                    if re.match(r'[a-z|\W_]+', input_data, re.I):
                        raise ValueError(
                            f'Only numbers are accepted for {answer}!')
                    else:
                        answers.append(int(input_data))
                        break
                if answer == 'product_price':
                    if re.match(r'[a-z|\W_]+', input_data, re.I):
                        raise ValueError(
                            f'Only numbers are accepted for {answer}!')
                    else:
                        input_data = re.sub(r'\W+', '', input_data)
                        answers.append(int(input_data))
                        break
            except ValueError as ve:
                print(ve)
                continue

    answers.append(datetime.datetime.now())
    new_data = dict(zip(first_row[1:], answers))

    with db.atomic():
        Product.create(**new_data)


def view_record():
    """View a database record"""
    while True:
        try:
            record_id = input('Enter the product id: ')

            if re.match(r'[a-z\s]+', record_id, re.I):
                raise ValueError('Only integers allowed!')
            elif re.match(r'-\d+', record_id):
                raise ValueError('Negative numbers are not allowed!')
            elif '.' in record_id:
                raise ValueError('Decimal numbers are not allowed!')
            elif re.match(r'[^\w_]+', record_id, re.I):
                raise ValueError('Symbols are not allowed!')
            else:
                break

        except ValueError as ve:
            clear()
            print(f'{ve} You have entered "{record_id}".')
            continue

    record = Product.select().where(Product.product_id == int(record_id))

    if not record.exists():
        clear()
        print('Not found in database!')
    else:
        clear()
        for data in record:
            data.date_updated = data.date_updated.strftime('%m/%d/%Y')
            print('+' * 100)
            print(
                f'\n{data.product_id}\t | \t{data.product_name}\t | \t{data.product_quantity}\t | \t{data.product_price}\t | \t{data.date_updated}\n')
            print('+' * 100)


def backup_data():
    """Backup database to a csv file"""
    query = Product.select().dicts()
    Csv('backup.csv').write_csv(query)


if __name__ == '__main__':
    initialize()
    import_csv()
    clear()
    menu()
