from RPA.Excel.Files import Files

class Excel:
    def __init__(self):
        self.exFile = Files()
        self.exFile.create_workbook("output", "xlsx", "data")
        self.row = 2

        self.exFile.set_cell_value(1,"A","Title")
        self.exFile.set_cell_value(1,"B","Description")
        self.exFile.set_cell_value(1,"C","Date")
        self.exFile.set_cell_value(1,"D","Image Path")
        self.exFile.set_cell_value(1,"E","Count Phrases")
        self.exFile.set_cell_value(1,"F","Months")
        self.exFile.set_cell_value(1,"G","contains money")


    def add_entry(self, title, description, date, picture_path, count_phrases,months,contains_money):
        self.exFile.set_cell_value(self.row, "A", title)
        self.exFile.set_cell_value(self.row, "B", description)
        self.exFile.set_cell_value(self.row, "C", date)
        self.exFile.set_cell_value(self.row, "D", picture_path)
        self.exFile.set_cell_value(self.row, "E", count_phrases)
        self.exFile.set_cell_value(self.row, "F", months)
        self.exFile.set_cell_value(self.row, "G", contains_money)
        self.row += 1

    def save(self,filename):
        if filename == "":
            self.exFile.save_workbook("output/data.xlsx")
        else:
            self.exFile.save_workbook(f"output/{filename}.xlsx")


