import os, requests
from dotenv import load_dotenv
import xlsxwriter

load_dotenv()

# Notification function
def notify(text):
    url = f"https://api.telegram.org/{os.environ.get('TELEGRAM_BOT_ID')}/sendMessage?chat_id={os.environ.get('TELEGRAM_CHAT_ID')}&text={text}"
    requests.get(url)

# Create Excel file
def create_xlsx(sheet_name, headers, results):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'{sheet_name}.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.set_column(0, 9, 15)
    i = 0
    row = 1
    col = 0
    for head in heads:
        letter = 65 + i
        worksheet.write(f"{chr(letter)}1", head, bold)
        i += 1

    # Add headers
    for header in headers:
        worksheet.write(0, headers.index(header), header)

    # Add data here
    for result in results:
        worksheet.write(results.index(result) + 1, 0, result[0])
        for x in result[1:]:
            worksheet.write(results.index(result) + 1, result.index(x), x)

    workbook.close()
