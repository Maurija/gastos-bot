import re
from datetime import datetime, timedelta

def parse_expense(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    payee = None
    amount = None
    date_time = None
    payment_method = None

    for i, line in enumerate(lines):
        lower = line.lower()

        # =========================
        # 🏪 Pagaste a
        # =========================
        if "pagaste a" in lower and i + 1 < len(lines):
            payee = lines[i + 1]

        # =========================
        # 💵 Monto
        # =========================
        if lower == "monto" and i + 1 < len(lines):
            amount_line = lines[i + 1]
            match = re.search(r'\$([\d.,]+)', amount_line)
            if match:
                amount = match.group(1)
                # Normalizar decimal para Google Sheets (formato argentino)
                amount = amount.replace(",", "")   # elimina separadores de miles si hubiera
                amount = amount.replace(".", ",")  # convierte decimal a coma

        # =========================
        # 📅 Fecha y Hora
        # =========================
        if "fecha y hora" in lower and i + 1 < len(lines):
            date_time = lines[i + 1]
            # 🔧 Correcciones OCR comunes
            date_time = date_time.replace("alas", "a las")
            date_time = date_time.replace("hs", "")
            date_time = date_time.strip()

        # =========================
        # 💳 Medio de pago
        # =========================
        if "medio de pago" in lower and i + 1 < len(lines):
            payment_method = lines[i + 1]

    return {
        "payee": payee,
        "amount": amount,
        "date_time": date_time,
        "payment_method": payment_method
    }