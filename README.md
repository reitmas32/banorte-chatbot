# MayaEveriware

MayaEveriware es un bot de Telegram diseñado para proporcionar asistencia a los usuarios con diversas consultas relacionadas con servicios financieros. Utiliza procesamiento de lenguaje natural (NLP) y un modelo LLM para responder a preguntas y proporcionar información precisa y útil de manera personalizada.

## Características

- **Asistencia Financiera Automatizada**: Responde a preguntas sobre saldo de cuentas, movimientos, transferencias, pagos, productos financieros y soporte para banca digital.
- **Personalización Basada en el Usuario**: La IA adapta sus respuestas y estilo de comunicación a la personalidad del usuario.
- **Transcripciones de Audio**: Utiliza la API de OpenAI Whisper para convertir mensajes de voz en texto y proporcionar una respuesta adecuada.
- **Memoria de Conversación**: Mantiene el contexto de la conversación almacenando mensajes anteriores para ofrecer respuestas más precisas y continuas.
- **Conexión a Firebase**: Almacena y recupera información de usuario desde Firebase para personalizar la experiencia del cliente.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal del proyecto.
- **Langchain**: Utilizado para la integración y ejecución de modelos de lenguaje LLM.
- **OpenAI**: Proporciona el modelo de lenguaje y Whisper para transcripción de audio.
- **Firebase**: Base de datos para almacenar información del usuario.
- **Telegram Bot API**: Para la interacción con los usuarios en la plataforma de Telegram.

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/reitmas32/banorte-chatbot.git
   cd mayaeveriware
   ```

2. Crear un entorno virtual e instalar las dependencias:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar las variables de entorno. Cree un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   TELEGRAM_KEY=tu_telegram_bot_token
   OPENAI_API_KEY=tu_openai_api_key
   TAVILY_API_KEY=tu_tavily_api_key
   FIREBASE_URL=tu_firebase_url
   ```

## Uso

1. Inicia el bot ejecutando el siguiente comando:
   ```sh
   python main.py
   ```

2. En Telegram, busca tu bot y comienza una conversación enviando el comando `/start`.

3. El bot responderá a mensajes de texto y mensajes de voz proporcionando respuestas personalizadas basadas en el contenido de la consulta.

## Arquitectura del Proyecto

- **core/settings.py**: Contiene la configuración y las variables de entorno necesarias para el funcionamiento del bot.
- **shared/embedings.py**: Módulo para gestionar las embeddings utilizando OpenAIModels.
- **shared/firebase.py**: Módulo para la integración con Firebase (subir y descargar datos).
- **main.py**: Punto de entrada principal del bot, gestiona los handlers de los comandos y mensajes de Telegram.

## Contribuir

Las contribuciones son bienvenidas. Por favor, siga estos pasos para contribuir:

1. Haga un fork del proyecto.
2. Cree una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realice sus cambios y haga commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Haga push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Cree un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulte el archivo `LICENSE` para obtener más detalles.

¡Gracias por utilizar MayaEveriware! ¡Esperamos que pueda ayudar a mejorar la experiencia financiera de sus usuarios!

