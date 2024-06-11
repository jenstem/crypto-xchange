import os
from dotenv import load_dotenv
import xlsxwriter

load_dotenv()

# Notification function

# Create Excel file
def create_xlsx(sheet_name, headers):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'{sheet_name}.xlsx')
    worksheet = workbook.add_worksheet()

    # Add headers
    for header in headers:
        worksheet.write(0, headers.index(header), header)

    # Add data here


    workbook.close()
