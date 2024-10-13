import json
import logging
import os

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from openai import OpenAI
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from core.settings import settings
from shared.embedings import EmbeddingsController, OpenAIModels
from shared.firebase import get_from_firebase, upload_to_firebase

os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

search = TavilySearchResults()

tools = [search]

# Telegram Bot
controller_embeddings = EmbeddingsController(model=OpenAIModels.ada_02)
controller_embeddings.load_embeddings()
llm = ChatOpenAI(model_name="gpt-4o", api_key=settings.OPENAI_API_KEY)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

conversations: dict[list[dict]] = {}


def get_response_of_llm(chat_dest: str, user_msg: str, idTelegram: str = ""):
    results = controller_embeddings.get_silimitary(user_msg)

    url_firebase = f"{settings.FIREBASE_URL}/test/usuarios/{idTelegram}"

    data_of_user = get_from_firebase(url_firebase)

    message_to_llm = f"""
    current_data = {data_of_user}

Consulta de saldo y movimientos: Uno de los usos más comunes es pedir el saldo de sus cuentas o consultar los últimos movimientos de forma rápida.
Transferencias y pagos: Dudas sobre transferencias interbancarias, pagos automáticos o cómo realizar transferencias electrónicas.
Consultas sobre productos: Información básica sobre productos financieros como cuentas, tarjetas de crédito, préstamos, o promociones.
Estado de trámites: Consultar el estado de solicitudes de crédito, tarjetas, o aclaraciones de algún trámite iniciado previamente.
Soporte con banca digital: Resolución de problemas menores con la app del banco, como restablecer contraseñas, desbloquear cuentas, o asistencia con el uso de funciones de la banca en línea.
Alertas de seguridad: Recibir notificaciones o reportar actividades sospechosas o intentos de fraude en tiempo real.
Promociones y ofertas: Información sobre promociones activas, programas de recompensas o descuentos por el uso de tarjetas.
Pago de servicios: Algunos bancos permiten realizar pagos de servicios o recargas de saldo de manera directa desde el chat con comandos rápidos o con enlaces para completar la transacción.
Funcionalidades extras:

Consulta de consejos: El usuario puede preguntar sobre la factibilidad de una compra o cómo obtener un producto sin comprometer sus finanzas. La IA guiará la conversación hacia una conclusión financieramente responsable.
Promociones personalizadas: Se enviarán promociones periódicas al usuario basadas en su perfil, edad y hábitos de gastos, analizando su información y las promociones activas.
Resumen mensual: En cada corte de tarjeta de crédito o mensualidad de débito, se enviará un resumen de gastos y se ofrecerán consejos financieros personalizados.
Pagos y alertas: En cada corte de tarjeta, se enviarán recordatorios y se permitirá pagar usando la cuenta de débito. También se avisará tras cada depósito de nómina, brindando recomendaciones sobre el uso responsable de sus finanzas.
Nuevas Funcionalidades:
Adaptación del estilo: El agente ajustará su manera de hablar según la personalidad y el tipo de agente asignado. Si el usuario es cómico, el agente aprenderá a ser más divertido; si es serio, será más formal. El agente evolucionará a medida que interactúa más con el usuario.
Respuestas claras y concisas: El agente responderá de forma directa, sin textos largos o repetitivos, para no agobiar al usuario.

Consulta del cliente: {user_msg}
Respuestas sugeridas: {[r.page_content for r in results[:5]]}
prev_messages: {conversations.get(chat_dest)}

## Funcionalidades en Agente por Mensajería

- *Consulta de saldo y movimientos*: Uno de los usos más comunes es pedir el saldo de sus cuentas o consultar los últimos movimientos de forma rápida.
- *Transferencias y pagos*: Dudas sobre transferencias interbancarias, pagos automáticos o cómo realizar transferencias electrónicas.
- *Consultas sobre productos*: Información básica sobre productos financieros como cuentas, tarjetas de crédito, préstamos, o promociones.
- *Estado de trámites*: Consultar el estado de solicitudes de crédito, tarjetas, o aclaraciones de algún trámite iniciado previamente.
- *Soporte con banca digital*: Resolución de problemas menores con la app del banco, como restablecer contraseñas, desbloquear cuentas, o asistencia con el uso de funciones de la banca en línea.
- *Alertas de seguridad*: Recibir notificaciones o reportar actividades sospechosas o intentos de fraude en tiempo real.
- *Promociones y ofertas*: Información sobre promociones activas, programas de recompensas o descuentos por el uso de tarjetas.
- *Pago de servicios*: Algunos bancos permiten realizar pagos de servicios o recargas de saldo de manera directa desde el chat con comandos rápidos o con enlaces para completar la transacción.

Funcionalidades extras: 

- Consulta de consejos: el usuario preguntará mediante un chat que tan factible es la compra de un producto y/o como puede obtener un producto sin comprometer sus finanzas, la IA lo ayudará a comprender si esto es o no posible, esta será una conversación general pues el usuario podrá hacer varias preguntas al chat y este responder hasta llegar a una conclusión financieramente responsble
- Periodicamente se le enviaran promociones al usuario de acuerdo a su perfil, sus edad y sus gastos, estos mediante un analisis previo de la información del usuario y de las promos activas
- Cada corte de tarjeta de crédito se le enviará al usuario un resumen de sus gastos y se le preguntará si quiere ver consejos financieros, gastos hormigoas, consejos, etc.
- Cada mes de tarjeta de debito se le enviará al usuario un resumen de sus gastos y se le preguntará si quiere ver consejos financieros, gastos hormigoas, consejos, etc.
- Mandar un mensaje de texto cada corte de tarjeta de credito y unos días antes de tarjeta de crédito
- Poner la opción de pagar tarjeta de crédito tomando el dinero en su cuenta de débito
- Pagos de servicio mediante cuenta de débito
- Cada pago de nómina avisar al usuario como puede usar sus finanzas de mejor manera de acuerdo a lo que ya debe actualmente y a su pronósitico

Si lo consideras a decuado añade la url de una de stas imagenes al final de la conversacion pero no añadas informacion al mensaje de que es la imagen solo si consideras en el contexto adecuado mandalo pero si no, no
    URL: https://i.imgflip.com/4/1bij.jpg Descripción: "Meme del 'Distracted Boyfriend' donde el novio se distrae por la 'inversión riesgosa' mientras ignora la 'inversión segura'."

    URL: https://i.kym-cdn.com/entries/icons/original/000/028/021/work.jpg Descripción: "Meme del 'Monkey Puppet' con cara de sorpresa, ilustrando el momento de darse cuenta que las acciones cayeron en picada."

    URL: https://i.imgflip.com/2y0xr4.jpg Descripción: "Meme de 'Elmo on Fire', representando la sensación de 'comprar en el dip' cuando el mercado sigue colapsando."

    URL: https://i.redd.it/xr0f9t4m1zz51.jpg Descripción: "Meme de gato triste mirando una caída del mercado, perfecta para expresar el dolor financiero al ver cómo caen los activos."

    URL: https://i.imgflip.com/1ur9b0.jpg Descripción: "'Expanding Brain' ilustrando las diferentes estrategias de inversión: desde guardar el dinero bajo el colchón hasta el trading de cripto."

    URL: https://i.imgflip.com/4/26am.jpg Descripción: "Meme del 'Roll Safe', donde sugiere que si no revisas tu portafolio, técnicamente no has perdido dinero."

    URL: https://i.imgflip.com/3sw1p0.jpg Descripción: "Meme de 'Panik - Kalm - Panik' ilustrando cómo te sientes viendo el gráfico del mercado caer, luego calmarte pensando que recuperará, para volver a entrar en pánico."

    URL: https://i.imgflip.com/2gnnjh.jpg Descripción: "Meme del 'Distracted Boyfriend' pero esta vez ignorando 'presupuesto mensual' y prestando atención a 'compras impulsivas'."

    URL: https://i.imgflip.com/30b1gx.jpg Descripción: "'Change My Mind' meme donde el texto sugiere que las criptomonedas siempre son una buena inversión, a pesar de la volatilidad."

    URL: https://i.imgflip.com/3g6tw8.jpg Descripción: "Meme de 'Shaquille O'Neal Squinting' mirando los gráficos, intentando encontrar patrones en un mercado completamente aleatorio."

    URL: https://i.imgflip.com/4t0m5.jpg Descripción: "'One Does Not Simply' invierte en acciones sin hacer una investigación previa."

    URL: https://i.imgflip.com/2vyvpb.jpg Descripción: "Meme de 'Drake' rechazando 'ahorrar dinero' y aprobando 'comprar más cripto'."

    URL: https://i.imgflip.com/1otk96.jpg Descripción: "Meme de 'American Chopper Argument' sobre cómo los padres no entienden la inversión en criptomonedas."

    URL: https://i.imgflip.com/3kmn4s.jpg Descripción: "'Is This a Pigeon?' meme donde un inversor pregunta si la caída del mercado es una oportunidad de compra."

    URL: https://i.imgflip.com/1o00in.jpg Descripción: "Meme de 'Surprised Pikachu' mostrando la sorpresa al ver caer tus inversiones después de hacer un análisis superficial."

    URL: https://i.imgflip.com/2qmf6k.jpg Descripción: "Meme de 'Winnie the Pooh' mostrando cómo te sientes al diversificar: 'sin diversificar' vs 'invirtiendo en muchos sectores'."

    URL: https://i.imgflip.com/3lx8i7.jpg Descripción: "'SpongeBob Mocking' ilustrando el consejo común de 'compra en el dip' mientras el mercado sigue cayendo."

    URL: https://i.imgflip.com/46rhzk.jpg Descripción: "Meme de 'Gru’s Plan' sobre hacer un plan financiero sólido solo para luego gastar impulsivamente."

    URL: https://i.imgflip.com/3vzej3.jpg Descripción: "Meme de 'Bernie Sanders' pidiendo 'una vez más' que el mercado suba después de días de caída."

    URL: https://i.imgflip.com/3txgi3.jpg Descripción: "'Distracted Boyfriend' versión inversor ignorando 'fondos de emergencia' y mirando 'acciones especulativas'."

    URL: https://i.imgflip.com/4hmlm8.jpg Descripción: "Meme de 'Ancient Aliens' culpando la volatilidad del mercado a los 'algoritmos'."

    URL: https://i.imgflip.com/4e5oi.jpg Descripción: "'Success Kid' feliz porque finalmente ha ahorrado lo suficiente para hacer una pequeña inversión."

    URL: https://i.imgflip.com/3q7doj.jpg Descripción: "Meme de 'Distracted Boyfriend' viendo 'invertir en acciones' mientras ignora 'pagar deudas'."

    URL: https://i.imgflip.com/3od1md.jpg Descripción: "'Doge Shiba Inu' mirando nervioso cuando el mercado está volátil y no sabes si vender o aguantar."

    URL: https://i.imgflip.com/4yc1d.jpg Descripción: "Meme de 'Third World Skeptical Kid' escuchando sobre promesas de rendimientos garantizados."

    URL: https://i.imgflip.com/2po6h1.jpg Descripción: "'Oprah You Get a Car' ilustrando cómo se siente la impresión de dinero y el estímulo económico."

    URL: https://i.imgflip.com/2hgfw.jpg Descripción: "'Confused Math Lady' calculando cuánto tendrás que ahorrar para tu jubilación después de ver el rendimiento del mercado."

    URL: https://i.imgflip.com/3np5qk.jpg Descripción: "Meme del 'Galaxy Brain' sugiriendo que si todo sube, entonces definitivamente es una buena oportunidad de compra, sin considerar el análisis real."

    URL: https://i.imgflip.com/4jcg5k.jpg Descripción: "'Two Buttons' meme donde el personaje debe elegir entre 'invertir con sentido común' y 'seguir el FOMO'."

    URL: https://i.imgflip.com/3sz3be.jpg Descripción: "Meme de 'Distracted Boyfriend' viendo la 'nueva criptomoneda prometedora' en lugar de sus 'inversiones seguras'."

    Importatnte: No adjuntes en el mensaje la descripcion del meme


    Datos a tomar en cuenta
    - si te preguntan por la linea de ayuda o consideras pertinente redirigir al cliente da este numero 0013343674974
    - para identificar al usuario usa idTelegram {idTelegram}
    - No des datos si no se solicitan es muy importante
    - Responde en menos de 250 caracteres
    - pudes cambiar la informacion simple de la data que tiene el usuario va
    - responderas de la siguiente forma (
        "mensaje": Aqui va el mensaje que le daremos al cliente,
        "new_data": nueva data del usuario solo en el caso de que se haya cambiado sino manda toda la data actual siempre
    )
    """

    prompt = hub.pull("hwchase17/openai-functions-agent")

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": message_to_llm})

    output = result["output"]

    cleaned_json_str = output.replace("```json", "").replace("```", "").strip()

    output_dict = json.loads(cleaned_json_str)

    message_to_send = output_dict["mensaje"]
    new_data = output_dict["new_data"]

    upload_to_firebase(url=url_firebase, data=new_data)


    if conversations.get(chat_dest) is not None:
        conversations[chat_dest].append(
            {
                "step": len(conversations[chat_dest]) + 1,
                "user": user_msg,
                "response": message_to_send,
            }
        )

    else:
        conversations[chat_dest] = [
            {
                "step": 1,
                "user": user_msg,
                "response": message_to_send,
            }
        ]

    name = agent_executor.invoke(
        {
            "input": f"Coneta informacion podrias saber cual es el nombre del cliente si es asi responde solo con el nombre del cliente y si no responde con el string None {conversations[chat_dest]}"
        }
    )

    if name.get("output") != "None":
        print("Obtener la data")

    return message_to_send


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    audio = update.message.voice or update.message.audio
    text = update.message.text
    idTelegram= update.effective_chat.username
    if audio:
        # Obtener el archivo de Telegram
        file = await context.bot.get_file(audio.file_id)

        # Definir el nombre del archivo mp3 para guardarlo localmente
        file_path = f"{audio.file_id}.mp3"

        # Descargar el archivo
        await file.download_to_drive(file_path)

        audio_file = open(file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )

        text = transcription.text
    if text:
        response = get_response_of_llm(
            chat_dest=update.message.author_signature, user_msg=text,
            idTelegram=idTelegram
        )
        await update.message.reply_text(response)


def get_voice(update: Update, context: CallbackContext) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = context.bot.get_file(update.message.voice.file_id)
    # download the voice note as a file
    new_file.download(f"voice_note.ogg")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(settings.TELEGRAM_KEY)
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND | filters.VOICE, echo)
    )
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
