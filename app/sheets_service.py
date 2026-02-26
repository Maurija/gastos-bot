import gspread
from google.oauth2.service_account import Credentials

# Configuración
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1I4UGI6rW0tG0kYIhkrAMqtr5Z8X7LKM_IqiSirsXGEo"

def get_sheet():
    # 🔥 Leer credenciales desde variable de entorno
    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    if not creds_json:
        raise Exception("No se encontró GOOGLE_CREDENTIALS en las variables de entorno")

    creds_dict = json.loads(creds_json)

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