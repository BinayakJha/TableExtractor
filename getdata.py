import pdfplumber
import pandas as pd
import os

pdf_name = input("Enter the name of the pdf file with .pdf: ")
output_format = input("Enter the output format (csv or excel): ")
initial_page_input = int(input("Enter the initial page number you want to start extract data from: "))
final_page_input = int(input("Enter the final page number you want to extract data from: "))

pdf = pdfplumber.open(pdf_name)
tables = []
for page in pdf.pages[initial_page_input-1:final_page_input]:
    if table := page.extract_table(): # extract_table() returns None if there are no tables
        print(f'Page {str(page.page_number)} table extracted.')
        tables.append(pd.DataFrame(table[1:], columns=table[0]))
        # save all the tables in a folder called tables
        if not os.path.exists('tables'):
            os.makedirs('tables')
        for i, table in enumerate(tables):
            if output_format == "csv":
                table.to_csv(f'tables/table{str(page.page_number)}.csv', index=False)
            elif output_format == "excel":
                table.to_excel(f'tables/table{str(page.page_number)}.xlsx', index=False)
            else:
                print("Invalid output format. Please enter either csv or excel.")
                break
pdf.close()
