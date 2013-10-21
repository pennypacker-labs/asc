import datetime
import csv
from xlrd import open_workbook

XL_START_DATE = datetime.datetime(1899, 12, 30)

NUM_COLUMNS = 16
HEADER_ROW = 22
START_ROW = 27


class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename
        self.wb = open_workbook(filename)
        self.sheet = self.wb.sheets()[0]

    def process(self):
        headers = ['PO #', 'Vendor', 'Date'] + self.get_row(HEADER_ROW)
        headers[6] = "Description Text"

        # Supply qc is always empty so remove it from headers
        headers.pop(4)

        row_data = self.get_data_from_rows()
        return self.output_to_csv(headers, row_data)

    def get_row(self, row):
        """
        Returns a list of all values in row
        """
        row_values = []
        for col in xrange(NUM_COLUMNS):
            row_values.append(
                str(self.sheet.cell(row, col).value))

        return row_values

    def get_data_from_rows(self):
        """
        Gets each line item from each purchase order.
        """
        next_row = START_ROW
        row_data = []

        # Loop over purchase orders until the file runs out
        # Assumes that we hit an IndexError eventually
        while True:
            try:
                line_items, end_row = self.get_line_items_for_purchase_order(
                    next_row)
            except IndexError:
                # Add last purchase order
                row_data.extend(line_items)
                return row_data
            else:
                next_row = end_row + 1
                row_data.extend(line_items)

    def get_line_items_for_purchase_order(self, row_index):
        """
        Assumes that start_row contains purchase order data,
        and that all subsequent line items are two spaces apart
        until empty.

        Returns the last row index so we know where to continue.
        """

        line_items = []

        # Extract PO info
        row = self.get_row(row_index)
        po_number = row[0]
        vendor = row[1]
        po_date = (
            XL_START_DATE + datetime.timedelta(
                days=float(row[3]))).strftime("%Y-%m-%d")
        po_info = [po_number, vendor, po_date]

        # Iterate through the line items
        row_index += 3
        row = self.get_row(row_index)

        # Iterate over each line item as long as first cell is non-empty
        while(row[0]):
            line_item = po_info + row

            # Remove supply qc value since always empty
            line_item.pop(4)
            line_items.append(line_item)

            # There are two empty rows between each line item
            row_index += 3
            row = self.get_row(row_index)

        return line_items, row_index

    def output_to_csv(self, headers, line_items):
        with open('po_line_items.csv', 'wb') as csvfile:
            line_item_writer = csv.writer(csvfile)
            line_item_writer.writerow(headers)
            for line_item in line_items:
                line_item_writer.writerow(line_item)
        print "Output saved to po_line_items.csv"
