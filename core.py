from xlrd import open_workbook

NUM_COLUMNS = 16
HEADER_ROW = 22


class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename
        self.wb = open_workbook(filename)
        self.sheet = self.wb.sheets()[0]

    def process(self):
        headers = self.get_row(HEADER_ROW)
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

    def get_data_from_rows(self, rows):
        """
        Gets each line item from each purchase order.
        """
        line_items = []
        vendor = None
        date = None
        order_number = None
        for row in rows:
            if self.is_purchase_order_row():
                vendor = self.extract_vendor(row)
                date = self.extract_date(row)
                order_number = self.extract_order_number(row)
                continue
            elif self.is_line_item_row():
                fields = self.get_fields(row)
                fields.extend([vendor, date, order_number])
                line_items.append(fields)
        return line_items

    def get_line_items_for_purchase_order(self, start_row):
        """
        Assumes that start_row contains purchase order data,
        and that all subsequent line items are two spaces apart
        until empty.

        Returns the last row index so we know where to continue.
        """

        line_items = []

        # Extract PO info
        row = self.get_row(start_row)
        po_number = row[0]
        vendor = row[1]
        po_date = row[2]


        # Iterate over each line item as long as first cell is non-empty
        while(row[0]):
            line_items.append(row)

            # There are two empty rows between each line item
            row += 3

        return line_items, row
