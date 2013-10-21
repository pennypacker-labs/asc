from xlrd import open_workbook

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
        rows = self.get_rows_from_workbook()
        row_data = self.get_data_from_rows(rows)
        self.output_to_csv(headers, row_data)

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
        while next_row < 1000: #self.sheet.nrows:
            line_items, end_row = self.get_line_items_for_purchase_order(
                next_row)
            next_row = end_row + 1
            row_data.extend(line_items)
        return row_data

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
        po_date = row[3]
        po_info = [po_number, vendor, po_date]

        # Iterate over each line item as long as first cell is non-empty
        while(row[0]):
            line_items.append(po_info + row)

            # There are two empty rows between each line item
            row_index += 3
            row = self.get_row(row_index)

        return line_items, row_index
