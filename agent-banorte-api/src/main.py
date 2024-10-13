from fastapi import FastAPI, Request
import json
import requests
from firebase import firebase
from dotenv import load_dotenv
from loguru import logger

from core.settings import settings
from fastapi import HTTPException
from pydantic import BaseModel
from telegram import Bot

load_dotenv()
app = FastAPI()
firebase = firebase.FirebaseApplication(settings.FIREBASE_URL)

CHAT_ID = 1544829412

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    logger.info(json.dumps(payload, indent=4))
    try:
        url = f"{settings.FIREBASE_URL}/webhooks.json"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info("Datos guardados en Firebase correctamente.")
            try:
                await _send_message(chat_id=CHAT_ID, text="Gracias por llamar 😃")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error enviando el mensaje: {str(e)}")
        else:
            logger.error(f"Error al guardar en Firebase: {response.content}")
            return {
                "message": "Error al guardar en Firebase",
                "error": response.content.decode(),
            }

    except Exception as e:
        logger.error(f"Error al conectar con Firebase: {e}")
        return {"message": "Error al conectar con Firebase", "error": str(e)}

    return {
        "message": "Webhook recibido y datos guardados en Firebase",
        "data": payload,
    }


@app.get("/users/{username}")
async def get_user_info(username: str):
    result = firebase.get(f"/usuarios/{username}", None)
    return result


# Modelo para definir el cuerpo de la solicitud POST
class MessagePayload(BaseModel):
    chat_id: int
    message: str

# Instancia del bot de Telegram
bot = Bot(token=settings.TELEGRAM_KEY)

async def _send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

# Endpoint POST para enviar mensajes
@app.post("/send_message")
async def send_message(payload: MessagePayload):
    try:
        await _send_message(chat_id=payload.chat_id, text=payload.message)
        return {"status": "success", "message": f"Mensaje enviado a {payload.chat_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error enviando el mensaje: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
