import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Configuración
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS")

def get_sheet():
    if not CREDS_JSON:
        raise Exception("No se encontró GOOGLE_CREDENTIALS en las variables de entorno")

    creds_dict = json.loads(CREDS_JSON)

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet


def append_expense(fecha, descripcion, monto, categoria):
    sheet = get_sheet()
    sheet.append_row([fecha, descripcion, monto, categoria])