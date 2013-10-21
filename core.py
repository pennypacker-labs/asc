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
        rows = self.get_rows()
        self.output_to_csv(headers, rows)

    def get_headers(self):
        """
        Returns a tuple of the column names
        """
        headers = []
        for col in xrange(NUM_COLUMNS):
            headers.append(
                str(self.sheet.cell(HEADER_ROW, col).value))

        return headers
