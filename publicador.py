# -*- coding: utf-8 -*-

import json
import requests
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN DEL BOT
# =========================

TELEGRAM_BOT_TOKEN = "8662537124:AAHNZj5Q6Bjqfp9aD4ugw461xNkudi3B930"
TELEGRAM_CHAT_ID = "-1003885309720"

RUTA_OFERTAS = "ofertas.json"


def cargar_ofertas(ruta):
    if not os.path.exists(ruta):
        print(f"[{datetime.now()}] Archivo de ofertas no encontrado: {ruta}")
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[{datetime.now()}] Error leyendo {ruta}: {e}")
        return []

    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "ofertas" in data:
        return data["ofertas"]
    else:
        print(f"[{datetime.now()}] Formato de {ruta} no reconocido.")
        return []


def construir_mensaje(oferta):
    """
    Esperamos que 'oferta' sea un dict con al menos:
    - titulo
    - precio
    - enlace

    Si hay más campos (descripción, descuento, etc.), se pueden añadir.
    """
    titulo = oferta.get("titulo") or oferta.get("title") or "Oferta SaaS"
    precio = oferta.get("precio") or oferta.get("price") or ""
    enlace = oferta.get("enlace") or oferta.get("url") or oferta.get("link") or ""

    # Normalizamos precio a string
    if isinstance(precio, (int, float)):
        precio_str = f"{precio}€"
    else:
        precio_str = str(precio) if precio else ""

    # Plantilla profesional y simple
    lineas = []

    lineas.append(f"🔥 {titulo}")

    if precio_str:
        lineas.append(f"💰 Precio: {precio_str}")

    if enlace:
        lineas.append(f"🔗 {enlace}")

    mensaje = "\n".join(lineas)
    return mensaje


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"[{datetime.now()}] Error enviando mensaje a Telegram: {resp.status_code} - {resp.text}")
        else:
            print(f"[{datetime.now()}] Mensaje enviado correctamente a Telegram.")
    except Exception as e:
        print(f"[{datetime.now()}] Excepción enviando mensaje a Telegram: {e}")


def publicar_ultima_oferta():
    ofertas = cargar_ofertas(RUTA_OFERTAS)
    if not ofertas:
        print(f"[{datetime.now()}] No hay ofertas para publicar.")
        return

    # Tomamos la última oferta del listado
    ultima = ofertas[-1]

    mensaje = construir_mensaje(ultima)
    print(f"[{datetime.now()}] Publicando oferta:\n{mensaje}\n")
    enviar_telegram(mensaje)


if __name__ == "__main__":
    publicar_ultima_oferta()
