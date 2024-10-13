# Proyecto: Webhook con FastAPI y Firebase

Este proyecto es una API desarrollada con FastAPI que permite recibir datos mediante un webhook y almacenarlos en Firebase, así como realizar integraciones con un bot de Telegram para enviar mensajes a usuarios específicos.

## Requisitos previos

- Python 3.7+
- Firebase (URL de tu base de datos)
- Una cuenta de bot en Telegram
- Archivo `.env` con las siguientes variables definidas:
  - `FIREBASE_URL`: URL de la base de datos de Firebase.
  - `TELEGRAM_KEY`: Token del bot de Telegram.
  - `PORT`: Puerto para ejecutar el servidor.

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows, usar `venv\Scripts\activate`
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` en el directorio principal con las siguientes variables:

   ```
   FIREBASE_URL=<URL de tu base de datos Firebase>
   TELEGRAM_KEY=<Token de tu bot de Telegram>
   PORT=<Puerto para el servidor>
   ```

## Ejecución del Proyecto

Para ejecutar la aplicación, usa el siguiente comando:

```bash
uvicorn main:app --host 0.0.0.0 --port <PUERTO>
```

## Endpoints Disponibles

### 1. POST `/webhook`

Este endpoint recibe un webhook con datos JSON y los almacena en Firebase.

- **Parámetros de solicitud**:
  - JSON en el cuerpo de la solicitud con los datos a almacenar.
- **Respuesta**:
  - Mensaje de confirmación si los datos se guardan correctamente en Firebase.
  - Mensaje de error en caso de que haya problemas para conectarse o almacenar los datos.

### 2. GET `/users/{username}`

Este endpoint permite obtener información de un usuario almacenado en Firebase.

- **Parámetros de URL**:
  - `username`: El nombre de usuario para buscar en la base de datos.
- **Respuesta**: Los datos del usuario especificado.

### 3. POST `/send_message`

Este endpoint permite enviar un mensaje a un chat de Telegram mediante el bot configurado.

- **Parámetros de solicitud**:
  - JSON en el cuerpo de la solicitud con los siguientes campos:
    - `chat_id` (int): ID del chat donde se desea enviar el mensaje.
    - `message` (str): Texto del mensaje a enviar.
- **Respuesta**: Confirmación de que el mensaje fue enviado con éxito o un error si no fue posible.

## Dependencias

- [FastAPI](https://fastapi.tiangolo.com/): Framework web para construir APIs.
- [requests](https://docs.python-requests.org/): Librería para hacer solicitudes HTTP.
- [firebase](https://pypi.org/project/python-firebase/): SDK de Firebase para Python.
- [loguru](https://loguru.readthedocs.io/): Librería para gestionar logs de manera sencilla.
- [python-dotenv](https://pypi.org/project/python-dotenv/): Para cargar variables de entorno desde un archivo `.env`.
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/): SDK de Telegram para interactuar con el bot.

## Contribución

Si deseas contribuir al proyecto, puedes hacer un fork del repositorio, crear una rama con tus cambios y abrir un Pull Request para revisarlo.

## Licencia

Este proyecto está bajo la licencia MIT. Por favor revisa el archivo `LICENSE` para más detalles.

