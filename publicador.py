import os
import time
import json
import requests
from hashlib import md5
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

HISTORIAL_FILE = "historial.json"
OFERTAS_FILE = "ofertas.json"


def enviar(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)


def cargar_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return set()
    with open(HISTORIAL_FILE, "r") as f:
        return set(json.load(f))


def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(list(historial), f)


def cargar_ofertas():
    with open(OFERTAS_FILE, "r") as f:
        return json.load(f)


def hash_oferta(oferta):
    texto = f"{oferta['titulo']}{oferta['precio']}{oferta['url']}"
    return md5(texto.encode()).hexdigest()


def loop(intervalo_min=30):
    historial = cargar_historial()
    ofertas = cargar_ofertas()

    while True:
        for oferta in ofertas:
            h = hash_oferta(oferta)

            if h not in historial:
                texto = f"{oferta['titulo']}\nPrecio: {oferta['precio']}\n{oferta['url']}"
                enviar(texto)
                historial.add(h)
                guardar_historial(historial)
                print("Oferta publicada:", oferta["titulo"])
            else:
                print("Oferta repetida, saltando:", oferta["titulo"])

            time.sleep(intervalo_min * 60)


if __name__ == "__main__":
    loop(30)

