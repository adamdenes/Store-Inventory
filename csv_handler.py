import re
import csv
from datetime import datetime


class Csv():
    """
    Csv class will read an existing CSV file in,
    convert the data into list of dicts and clean it.
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def read_csv(self):
        """Reading csv file."""
        with open(self.file_name, newline='') as csvfile:
            filereader = csv.DictReader(csvfile, delimiter=',')
            return list(filereader)

    def clean_csv(self):
        """Cleaning csv file."""
        list_of_data = self.read_csv()

        for row in list_of_data:
            # converting csvfile to DictReader object cleaned '"' automatically
            # cleaning it just in case
            if '"' in row['product_name']:
                row['product_name'].replace('"', '')

            # converting dollar to pure cents
            if re.match(r'\W+', row['product_price']):
                row['product_price'] = re.sub(r'\W+', '', row['product_price'])

            # converting product_quantity to integer
            row['product_quantity'] = int(row['product_quantity'])

            # converting product_price to integer
            row['product_price'] = int(row['product_price'])

            # converting date_updated to datetime
            row['date_updated'] = datetime.strptime(
                row['date_updated'], '%m/%d/%Y').date()

        return list_of_data
