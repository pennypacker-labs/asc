from xlrd import open_workbook


class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename
        self.wb = open_workbook(filename)

    def process(self):
        headers = self.get_headers()
        rows = self.get_rows()
        self.output_to_csv(headers, rows)

    def get_headers(self):
        """
        Returns a tuple of the column names
        """
        pass
