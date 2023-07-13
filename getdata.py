import pdfplumber
import pandas as pd
import os

pdf_name = input("Enter the name of the pdf file with .pdf: ")
pdf = pdfplumber.open(pdf_name)
tables = []
for page in pdf.pages:
    if table := page.extract_table(): # extract_table() returns None if there are no tables
        tables.append(pd.DataFrame(table[1:], columns=table[0]))
        # save all the tables in a folder called tables
        if not os.path.exists('tables'):
            os.makedirs('tables')

        for i, table in enumerate(tables):
            table.to_csv(f'tables/table{str(i)}.csv', index=False)
            print(f'tables/table{str(i)}.csv')
pdf.close()
