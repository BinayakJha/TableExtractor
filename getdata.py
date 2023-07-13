import pdfplumber
import pandas as pd
import os

class TableExtractor:
    def __init__(self, pdf_name, output_format, initial_page_input, final_page_input, merge_or_not):
        self.pdf_name = pdf_name
        self.output_format = output_format
        self.initial_page_input = initial_page_input
        self.final_page_input = final_page_input
        self.merge_or_not = merge_or_not
        self.tables = []

    def extract_tables(self):
        pdf = pdfplumber.open(self.pdf_name)
        for page in pdf.pages[self.initial_page_input-1:self.final_page_input]:
            if table := page.extract_table(): # extract_table() returns None if there are no tables
                print(f'Page {str(page.page_number)} table extracted.')
                self.tables.append(pd.DataFrame(table[1:], columns=table[0]))
                # save all the tables in a folder called tables
                if not os.path.exists('tables'):
                    os.makedirs('tables')
                for table in self.tables:
                    if self.output_format == "csv":
                        table.to_csv(f'tables/table{str(page.page_number)}.csv', index=False)
                    elif self.output_format == "excel":
                        table.to_excel(f'tables/table{str(page.page_number)}.xlsx', index=False)
                    else:
                        print("Invalid output format. Please enter either csv or excel.")
                        break
        pdf.close()

    def merge_tables(self):
        return pd.concat(self.tables)

    def save_merged_table(self, merged_table):
        if self.output_format == "csv":
            merged_table.to_csv('tables/merged_table.csv', index=False)
            print("Tables merged.")
        elif self.output_format == "excel":
            merged_table.to_excel('tables/merged_table.xlsx', index=False)
            print("Tables merged.")
        else:
            print("Invalid output format. Please enter either csv or excel.")

    def run(self):
        self.extract_tables()
        if self.merge_or_not == 'y':
            merged_table = self.merge_tables()
            self.save_merged_table(merged_table)
        else:
            print("Tables not merged.")

if __name__ == "__main__":
    pdf_name = input("Enter the name of the pdf file with .pdf: ")
    output_format = input("Enter the output format (csv or excel): ")
    initial_page_input = int(input("Enter the initial page number you want to start extract data from: "))
    final_page_input = int(input("Enter the final page number you want to extract data from: "))
    merge_or_not = input("Do you want to merge the tables? (y/n): ")
    extractor = TableExtractor(pdf_name, output_format, initial_page_input, final_page_input, merge_or_not)
    extractor.run()
