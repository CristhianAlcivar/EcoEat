from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta, timezone
import os, json, re, uuid, requests
import uuid
from app.data.repositories.user_repository_impl import SQLAlchemyUserRepository
from app.domain.entities.user import User
import redis

from app.ecobot.taco_predictor import predict_image
from app.data.repositories.model_repository_impl import SQLAlchemyModelRepository
from app.data.repositories.image_repository_impl import SQLAlchemyImageRepository
from app.application.use_cases.guardar_imagen_clasificada import GuardarImagenClasificadaUseCase
from app.data.db.models import MaterialModel
from app.data.db.database import SessionLocal

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

router = APIRouter(prefix="/ecobot", tags=["EcoBot"])
r = redis.from_url(redis_url, decode_responses=True)

class WebhookInput(BaseModel):
    user_id: str
    mensaje: str
    thread_id: Optional[str] = "1"

VALID_TOKEN = os.getenv("VALID_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

def extraer_materiales_desde_texto(texto: str) -> list[dict]:
    predicciones = re.split(r"✅ Predicción #[0-9]+:", texto)
    materiales = []

    for pred in predicciones:
        if not pred.strip():
            continue

        nombre = re.search(r"🔹 Categoría:\s*(.+)", pred)
        tipo = re.search(r"🔹 Material:\s*(.+)", pred)
        reciclable = re.search(r"🔹 Reciclable:\s*(.+)", pred)
        confianza = re.search(r"🔹 Confianza:\s*([\d.]+)%", pred)
        impacto = "alto" if reciclable and reciclable.group(1).strip().lower() == "no" else "bajo"

        materiales.append({
            "nombre_material": nombre.group(1).strip() if nombre else "Desconocido",
            "tipo_material": tipo.group(1).strip() if tipo else "Desconocido",
            "reciclable": reciclable.group(1).strip().lower() == "sí" if reciclable else False,
            "renovable": False,  # Lógica futura si deseas inferirlo
            "confianza": float(confianza.group(1)) / 100 if confianza else 0.0,
            "impacto_ambiental": impacto
        })

    return materiales

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
        user_phone = message.get("from")
        
    except Exception as e:
        print("Error extrayendo datos:", e)
        return {}

    with SessionLocal() as session:
        user_repo = SQLAlchemyUserRepository(session)
        user_db = user_repo.get_by_telefono(user_phone)
        if not user_db:
            nuevo_usuario = User(
                telefono=user_phone
            )
            user_repo.save(nuevo_usuario)
            print(f"Usuario {user_phone} guardado.")
        else:
            print(f"Usuario {user_phone} ya existe.")
            
    if message_type == "image":
        image_id = message["image"]["id"]
        print("📸 Imagen recibida, id:", image_id)

        image_url = obtener_url_imagen_whatsapp(image_id)
        downloads_dir = "downloads"
        os.makedirs(downloads_dir, exist_ok=True)

        nombre_archivo = f"{uuid.uuid4().hex}.jpg"
        ruta_archivo = os.path.join(downloads_dir, nombre_archivo)
        image_uuid = uuid.uuid4()

        try:
            r = requests.get(image_url, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"})
            if r.status_code != 200:
                enviar_whatsapp(user_id, "No pude descargar la imagen enviada.")
                return {}

            with open(ruta_archivo, 'wb') as f:
                f.write(r.content)

            resultado = predict_image(ruta_archivo)
            if isinstance(resultado, dict) and "error" in resultado:
                enviar_whatsapp(user_id, resultado["error"])
                os.remove(ruta_archivo)
                return {}

            modelo_nombre = resultado.get("resultado_modelo")
            texto_modelo = resultado.get("respuesta_modelo_texto", "")
            
            with SessionLocal() as session:
                user_repo = SQLAlchemyUserRepository(session)
                user = user_repo.get_by_telefono(user_phone)


            model_repo = SQLAlchemyModelRepository()
            modelos = model_repo.list_all()
            modelo_encontrado = next((m for m in modelos if m.nombre == modelo_nombre), None)

            if not modelo_encontrado:
                modelo_encontrado = model_repo.get_best_model()

                if not modelo_encontrado:
                    enviar_whatsapp(user_id, "No se encontró ningún modelo disponible.")
                    return {}
            base_path = r"http://localhost:8080/downloads"
            ruta = os.path.join(base_path, ruta_archivo)

            datos_imagen = {
                "id": image_uuid,
                "nombre_imagen": nombre_archivo,
                "ruta": ruta,
                "usuario_id": user.id,
                "fecha": datetime.now(timezone.utc),
                "modelo_id": modelo_encontrado.id
            }
            with SessionLocal() as session:
                image_repo = SQLAlchemyImageRepository(session)
                use_case = GuardarImagenClasificadaUseCase(image_repo)
                use_case.execute(datos_imagen)

                # Extraer materiales del texto de salida del modelo
            materiales = extraer_materiales_desde_texto(texto_modelo)
            if materiales:
                with SessionLocal() as session:
                    for mat in materiales:
                        session.add(MaterialModel(
                            id=uuid.uuid4(),
                            nombre_material=mat["nombre_material"],
                            tipo_material=mat["tipo_material"],
                            renovable=mat["renovable"],
                            reciclable=mat["reciclable"],
                            confianza=mat["confianza"],
                            impacto_ambiental=mat["impacto_ambiental"],
                            imagen=image_uuid
                        ))
                    session.commit()
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
            
            result = (
                f"Predicción de material:\n"
                f"🔹 Categoría: {resultado['class_name']}\n"
                f"🔹 Material: {resultado['material']}\n"
                f"🔹 Reciclable: {'Sí' if resultado['recyclable'] else 'No'}\n"
                f"🔹 Valor estimado: ${resultado['value']:.2f}\n"
                f"🔹 Confianza: {resultado['confianza_promedio']*100:.2f}%"
            )
            print(result)
            # Procesar la respuesta del modelo y enviar mensaje de WhatsApp            
            from app.ecobot.graph import graph
            config = {"configurable": {"user_id": user_id, "thread_id": "1"}}
            state = {"messages": [{"role": "user", "content": result}], "last_accion": None}

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
        except Exception as e:
            print("❌ Error al procesar imagen:", e)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
            enviar_whatsapp(user_id, "Ocurrió un error procesando tu imagen.")
        return {}
    elif message_type == "text":
        mensaje = message["text"]["body"]
        config = {
            "configurable": {
                "user_id": user_id,
                "thread_id": obtener_conversation_id(user_id)
            }
        }
        state = {
            "messages": [{"role": "user", "content": mensaje}],
            "last_accion": None,
        }

        from app.ecobot.graph import graph
        for chunk in graph.stream(state, config, stream_mode="values"):
            last_message = chunk.get("messages", [])[-1] if chunk.get("messages") else {"content": "Error procesando mensaje"}
            content = last_message["content"]
            match = re.search(r"(?:Final Answer:\s*)?(\{.*\})", content, re.DOTALL)
            if match:
                print(content)
                json_str = match.group(1).strip().replace("{{", "{").replace("}}", "}")
                try:
                    respuesta = json.loads(json_str)
                    texto = respuesta.get("msg", "Lo siento, no tengo respuesta en este momento.")
                    enviar_whatsapp(user_id, texto)
                    break
                except json.JSONDecodeError:
                    enviar_whatsapp(user_id, "El modelo devolvió un JSON inválido.")
                    break

def obtener_conversation_id(user_id):
    key = f"conversation:{user_id}"
    data = r.hgetall(key)

    ahora = datetime.utcnow()
    if data:
        started_at = datetime.fromisoformat(data["started_at"])
        # Si la conversación tiene menos de 24h, regresa el mismo UUID
        if ahora - started_at < timedelta(hours=24):
            return data["conversation_id"]
    
    # Si no hay o está vencido, crea uno nuevo
    conversation_id = str(uuid.uuid4())
    r.hmset(key, {
        "conversation_id": conversation_id,
        "started_at": ahora.isoformat()
    })
    r.expire(key, 60*60*24)  # Expira el registro en 24h automáticamente
    return conversation_id

@router.get("/webhook")
async def verify_webhook(request: Request):
    args = request.query_params
    if (
        args.get("hub.mode") == "subscribe"
        and args.get("hub.verify_token") == VALID_TOKEN
    ):
        print("✅ Verificación exitosa")
        return PlainTextResponse(content=args.get("hub.challenge"), status_code=200)
    print("❌ Verificación fallida")
    return PlainTextResponse(content="Token de verificación inválido", status_code=403)

def obtener_url_imagen_whatsapp(media_id):
    url = f"https://graph.facebook.com/v23.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    resp = requests.get(url, headers=headers)
    return resp.json().get("url")

def enviar_whatsapp(numero, mensaje):
    url = f"https://graph.facebook.com/v23.0/{WHATSAPP_PHONE_ID}/messages"
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
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("❌ Error al enviar mensaje:", response.text)
        # Aquí podrías agregar más lógica, como enviar un correo, un log, etc.
    else:
        print("✅ Mensaje enviado correctamente")
