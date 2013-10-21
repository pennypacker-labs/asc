from xlrd import open_workbook

NUM_COLUMNS = 16
HEADER_ROW = 22


class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename
        self.wb = open_workbook(filename)
        self.sheet = self.wb.sheets()[0]

    def process(self):
        headers = self.get_headers()
        rows = self.get_rows_from_workbook()
        row_data = self.get_data_from_rows(rows)
        self.output_to_csv(headers, row_data)

    def get_headers(self):
        """
        Returns a tuple of the column names
        """
        headers = []
        for col in xrange(NUM_COLUMNS):
            headers.append(
                str(self.sheet.cell(HEADER_ROW, col).value))
        return headers

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
