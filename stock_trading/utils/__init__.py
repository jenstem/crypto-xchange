import os, requests
from dotenv import load_dotenv
import xlsxwriter

load_dotenv()

# Notification function
def notify(text):
    url = f"https://api.telegram.org/{os.environ.get('TELEGRAM_BOT_ID')}/sendMessage?chat_id={os.environ.get('TELEGRAM_CHAT_ID')}&text={text}"
    requests.get(url)

# Create Excel file
def create_xlsx(sheet_name, headers, contents):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'{sheet_name}.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.set_column(0, 9, 15)
    i = 0
    row = 1
    col = 0
    for header in headers:
        letter = 65 + i
        worksheet.write(f"{chr(letter)}1", header, bold)
        i += 1

    print(content[0])
    for content in contents:
            worksheet.write_string(row, col, str(content[0]))
            j = 1
            for _c in content[1:]:
                worksheet.write_string(row, col + j, str(_c))
                j += 1
            row += 1

    workbook.close()
