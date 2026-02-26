from fastapi import FastAPI, Request
from dotenv import load_dotenv

from app.telegram_handler import send_message, download_telegram_file
from app.ocr_service import extract_text_from_image
from app.sheets_service import append_expense
from app.expense_parser import parse_expense

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "running"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})

    chat_id = message.get("chat", {}).get("id")

    text_to_process = None

    # =========================
    # 📝 TEXTO
    # =========================
    if "text" in message:
        text_to_process = message["text"]
        print("📩 Texto recibido:", text_to_process)

    # =========================
    # 📷 FOTO (OCR)
    # =========================
    elif "photo" in message:
        print("📷 Foto recibida")

        file_id = message["photo"][-1]["file_id"]

        # Descargar imagen
        image_file = download_telegram_file(file_id)
        print("Imagen descargada:", image_file)

        # Extraer texto
        extracted_text = extract_text_from_image(image_file)
        print("Texto OCR:", extracted_text)

        text_to_process = extracted_text

    # =========================
    # 🚫 Ignorar otros tipos
    # =========================
    else:
        return {"ok": True}

    # =========================
    # 💰 Procesar gasto
    # =========================
    if text_to_process:
        expense_data = parse_expense(text_to_process)

        append_expense(
            expense_data["payee"],
            expense_data["amount"],
            expense_data["date_time"],
            expense_data["payment_method"]
        )

        send_message(
            chat_id,
            f"""✅ Gasto registrado:
        Pagaste a: {expense_data["payee"]}
        Monto: ${expense_data["amount"]}
        Fecha y hora: {expense_data["date_time"]}
        Medio de pago: {expense_data["payment_method"]}"""
        )

    return {"ok": True}