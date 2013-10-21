class DataCleaner(object):
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        headers = self.get_headers()
        rows = self.get_rows()
        self.output_to_csv(headers, rows)

    def get_headers(self):
        """
        Returns a tuple of the column names
        """
        pass
