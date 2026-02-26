import gspread
from google.oauth2.service_account import Credentials

# Configuración
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1I4UGI6rW0tG0kYIhkrAMqtr5Z8X7LKM_IqiSirsXGEo"

def get_sheet():
    creds = Credentials.from_service_account_file(
        "app/credentials.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet


def append_expense(fecha, descripcion, monto, categoria):
    sheet = get_sheet()
    sheet.append_row([fecha, descripcion, monto, categoria])