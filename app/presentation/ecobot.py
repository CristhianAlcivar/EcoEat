from fastapi import APIRouter,Header ,HTTPException, Request
import requests
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
from app.ecobot.graph import graph
import os, json, re
import uuid

router = APIRouter(prefix="/ecobot", tags=["EcoBot"])

class WebhookInput(BaseModel):
    user_id: str
    mensaje: str
    thread_id: Optional[str] = "1"
    
VALID_TOKEN = os.getenv("VALID_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID") 

@router.post("/webhook")
async def webhook(request: Request, Authorization: str = Header(default=None)):
    if Authorization and Authorization not in [VALID_TOKEN, f"Bearer {VALID_TOKEN}"]:
        raise HTTPException(status_code=403, detail="Token inválido o faltante")

    body = await request.json()
    try:
        entry = body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            print("No hay mensajes en este evento.")
            return {}
        message = messages[0]
        user_id = message.get("from")
        message_type = message.get("type")
    except Exception as e:
        print("Error extrayendo datos:", e)
        return {}

    if message_type == "text":
        mensaje = message["text"]["body"]
        config = {
            "configurable": {
                "user_id": user_id,
                "thread_id": "1"
            }
        }
        state = {
            "messages": [{"role": "user", "content": mensaje}],
            "last_accion": None,
        }
        for chunk in graph.stream(state, config, stream_mode="values"):
            last_message = chunk.get("messages", [])[-1] if chunk.get("messages") else {"content": "Error procesando mensaje"}
            content = last_message["content"]
            match = re.search(r"(?:Final Answer:\s*)?(\{.*\})", content, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                json_str = json_str.replace("{{", "{").replace("}}", "}")
                try:
                    respuesta = json.loads(json_str)
                    texto = respuesta.get("msg", "Lo siento, no tengo respuesta en este momento.")
                    enviar_whatsapp(user_id, texto)
                    break
                except json.JSONDecodeError:
                    enviar_whatsapp(user_id, "El modelo devolvió un JSON inválido.")
                    break

    elif message_type == "image":
        image_id = message["image"]["id"]
        print("Imagen recibida, id:", image_id)
        image_url = obtener_url_imagen_whatsapp(image_id)
        resultado = procesar_imagen_con_modelo(image_url) 
        print(resultado)
        config = {
            "configurable": {
                "user_id": user_id,
                "thread_id": "1"
            }
        }
        state = {
            "messages": [{"role": "user", "content": resultado}],
            "last_accion": None,
        }
        from app.ecobot.graph import graph
        for chunk in graph.stream(state, config, stream_mode="values"):
            last_message = chunk.get("messages", [])[-1] if chunk.get("messages") else {"content": "Error procesando mensaje"}
            content = last_message["content"]
            match = re.search(r"(?:Final Answer:\s*)?(\{.*\})", content, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                json_str = json_str.replace("{{", "{").replace("}}", "}")
                try:
                    respuesta = json.loads(json_str)
                    texto = respuesta.get("msg", "Lo siento, no tengo respuesta en este momento.")
                    enviar_whatsapp(user_id, texto)
                    break
                except json.JSONDecodeError:
                    enviar_whatsapp(user_id, "El modelo devolvió un JSON inválido.")
                    break
    else:
        print(f"Tipo de mensaje no soportado: {message_type}")
        enviar_whatsapp(user_id, "Por ahora solo proceso texto e imágenes.")

    return {}

def obtener_url_imagen_whatsapp(media_id):
    url = f"https://graph.facebook.com/v19.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    return data.get("url")

def procesar_imagen_con_modelo(image_url):
    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)  # Crea la carpeta si no existe

    nombre_temp = os.path.join(downloads_dir, f"{uuid.uuid4().hex}.jpg")
    try:
        r = requests.get(image_url, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"})
        if r.status_code != 200:
            print("Error descargando la imagen:", r.status_code, r.text)
            return "No pude descargar la imagen enviada."
        with open(nombre_temp, 'wb') as f:
            f.write(r.content)

        from app.ecobot.taco_predictor import predict_image
        resultado = predict_image(nombre_temp)

        os.remove(nombre_temp)  # Borra la imagen después de procesarla
        return resultado

    except Exception as e:
        print("Error procesando imagen:", e)
        if os.path.exists(nombre_temp):
            os.remove(nombre_temp)
        return "Ocurrió un error procesando tu imagen."

def enviar_whatsapp(numero, mensaje):
    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensaje}
    }
    requests.post(url, headers=headers, json=payload)

@router.get("/webhook")
async def verify_webhook(request: Request):
    args = request.query_params
    VERIFY_TOKEN = os.getenv("VALID_TOKEN")
    print("Verificación recibida:", dict(args))
    if (
        args.get("hub.mode") == "subscribe"
        and args.get("hub.verify_token") == VERIFY_TOKEN
    ):
        print("✅ Verificación exitosa")
        return PlainTextResponse(content=args.get("hub.challenge"), status_code=200)
    print("❌ Verificación fallida")
    return PlainTextResponse(content="Token de verificación inválido", status_code=403)