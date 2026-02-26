import requests
import os
from app.config import TELEGRAM_TOKEN

print("Telegram token:", TELEGRAM_TOKEN)

def download_telegram_file(file_id: str) -> str:
    # Obtener file_path
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    file_path = response.json()["result"]["file_path"]

    # Descargar archivo
    download_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    file_response = requests.get(download_url)

    file_name = file_path.split("/")[-1]

    with open(file_name, "wb") as f:
        f.write(file_response.content)

    return file_name


def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })