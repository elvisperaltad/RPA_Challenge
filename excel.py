from RPA.Excel.Files import Files

class Excel:
    def __init__(self, headers=None):
        self.exFile = Files()
        self.exFile.create_workbook("output", "xlsx", "data")
        self.row = 2

        if headers is None:
            headers = ["Title", "Description", "Date", "Image Path", "Count Phrases", "Months", "Contains Money"]
        
        for col_num, header in enumerate(headers, start=1):
            self.exFile.set_cell_value(1, self._num_to_col_letter(col_num), header)


    def _num_to_col_letter(self, num):
        """Convert a column number to an Excel column letter."""
        letter = ''
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter
    
    def add_entry(self, title, description, date, picture_path, count_phrases, months, contains_money):
        """Create a dictionary of column mappings"""
        entry_data = {
            "A": title,
            "B": description,
            "C": date,
            "D": picture_path,
            "E": count_phrases,
            "F": months,
            "G": contains_money
        }

        """Iterate over the dictionary and set cell values"""
        for column, value in entry_data.items():
            self.exFile.set_cell_value(self.row, column, value)

        """Increment the row counter"""
        self.row += 1

    def save(self,filename):
        if filename == "":
            self.exFile.save_workbook("output/data.xlsx")
        else:
            self.exFile.save_workbook(f"output/{filename}.xlsx")


