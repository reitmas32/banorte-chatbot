from enum import Enum

from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel


class Embedding(BaseModel):
    id: str
    vector: list[float]


class EmbeddingsModels(str, Enum):
    pass


class OpenAIModels(EmbeddingsModels):
    ada_02 = "text-embedding-ada-002"


class Lamma3Models(EmbeddingsModels):
    llama_7b = "llama:7b"


class EmbeddingsController:
    def __init__(self, model: EmbeddingsModels):
        self.model: EmbeddingsModels = model
        self.controller: OpenAIEmbeddings = OpenAIEmbeddings(
            model=model,
        )

    def get_embeddings(self, data: list[str]):
        self.vector_store = InMemoryVectorStore.from_texts(
            data,
            embedding=self.controller,
        )

    def get_silimitary(self, query: str):
        vector_store = self.vector_store

        @chain
        def retriever(query: str) -> list[Document]:
            docs, scores = zip(
                *vector_store.similarity_search_with_score(query), strict=False
            )
            for doc, score in zip(docs, scores, strict=False):
                doc.metadata["score"] = score

            return docs

        return retriever.invoke(query)

    def load_embeddings(self):
        self.get_embeddings(
            [
                "Todos los clientes de Banorte deben presentar una identificación oficial para abrir una cuenta bancaria.",
                "Los clientes de Banorte deben tener al menos 18 años para abrir una cuenta individual.",
                "Los menores de edad pueden abrir una cuenta en Banorte, pero deben estar acompañados por un tutor legal.",
                "Banorte requiere un comprobante de domicilio actualizado para abrir una cuenta.",
                "Los clientes deben firmar un contrato de servicios bancarios para operar con Banorte.",
                "Los clientes pueden acceder a sus cuentas en línea mediante credenciales seguras proporcionadas por Banorte.",
                "Para realizar una transferencia internacional, el cliente debe proporcionar el código SWIFT del banco receptor.",
                "Los retiros en efectivo están sujetos a límites diarios, los cuales varían según el tipo de cuenta en Banorte.",
                "Las cuentas de ahorro en Banorte generan intereses mensuales que se depositan directamente en la misma cuenta.",
                "Los clientes deben notificar a Banorte sobre cualquier actividad sospechosa en sus cuentas.",
                "Los créditos personales de Banorte están sujetos a evaluaciones de historial crediticio.",
                "Los clientes deben pagar una comisión mensual si el saldo promedio en su cuenta de Banorte es inferior al mínimo requerido.",
                "Los pagos de tarjetas de crédito de Banorte deben realizarse antes de la fecha de corte para evitar cargos por intereses.",
                "Los clientes pueden solicitar una extensión de línea de crédito en Banorte, sujeta a aprobación.",
                "Las tarjetas de débito de Banorte tienen un límite diario para retiros en cajeros automáticos.",
                "Banorte ofrece protección contra fraude en transacciones no autorizadas.",
                "Los clientes deben notificar a Banorte si pierden su tarjeta para evitar transacciones fraudulentas.",
                "Las cuentas inactivas por más de un año podrían estar sujetas a cargos por inactividad en Banorte.",
                "Los clientes pueden establecer débitos automáticos para pagos recurrentes desde sus cuentas de Banorte.",
                "Las transferencias entre cuentas de Banorte suelen ser gratuitas.",
                "Las transferencias a otros bancos pueden generar una comisión.",
                "Los clientes deben establecer una clave de seguridad para operaciones por teléfono con Banorte.",
                "Los préstamos hipotecarios de Banorte requieren una evaluación del inmueble como parte del proceso de aprobación.",
                "Banorte puede congelar una cuenta si sospecha de actividad ilícita.",
                "Los clientes deben presentar justificación documental para movimientos de altas sumas de dinero en Banorte.",
                "Banorte está obligado a informar a las autoridades sobre transacciones sospechosas.",
                "Las tarjetas de crédito de Banorte tienen una cuota anual que debe pagarse para mantener la tarjeta activa.",
                "Los clientes pueden acceder a créditos con tasas preferenciales en Banorte si cumplen ciertos requisitos.",
                "Las cuentas conjuntas en Banorte requieren la firma de todos los titulares para ciertos movimientos.",
                "Los clientes deben mantener actualizada su información de contacto en Banorte para evitar problemas de comunicación.",
                "Las tarjetas de crédito de Banorte tienen un período de gracia en el cual no se generan intereses si se paga el total.",
                "Los clientes pueden solicitar el bloqueo temporal de sus tarjetas de Banorte si sospechan de una pérdida temporal.",
                "Banorte no se hace responsable de transacciones realizadas con tarjetas perdidas sin notificación previa.",
                "Las cuentas empresariales en Banorte tienen requisitos adicionales, como la presentación de documentos de constitución.",
                "Los pagos realizados en día inhábil se procesarán el siguiente día hábil.",
                "Las transferencias internacionales en Banorte pueden tardar entre 2 y 5 días hábiles en completarse.",
                "Banorte cobra una comisión por el uso de cajeros automáticos que no son de su red.",
                "Los clientes pueden establecer límites personalizados para sus tarjetas de débito y crédito de Banorte.",
                "Los intereses generados en cuentas de ahorro de Banorte están sujetos a impuestos.",
                "Banorte ofrece servicios de inversión, pero los clientes deben firmar un acuerdo de riesgos.",
                "Los clientes pueden acceder a su estado de cuenta mensual a través de la banca en línea de Banorte.",
                "Los clientes pueden recibir asesoría financiera gratuita en Banorte para planificar inversiones.",
                "Las transferencias programadas en Banorte deben establecerse al menos con un día de anticipación.",
                "Banorte puede solicitar información adicional para cumplir con las regulaciones contra el lavado de dinero.",
                "Las cuentas pueden ser bloqueadas por Banorte si se sospecha de intentos de acceso no autorizado.",
                "Los clientes pueden solicitar una tarjeta de reemplazo en caso de robo o pérdida en Banorte.",
                "Las transacciones en monedas extranjeras en Banorte están sujetas a la tasa de cambio vigente al momento de la operación.",
                "Los clientes pueden optar por recibir notificaciones SMS para movimientos mayores a una cantidad establecida en Banorte.",
                "Las solicitudes de préstamo en Banorte requieren la presentación de comprobantes de ingresos.",
                "Banorte ofrece la posibilidad de contratar seguros de vida, vehículo, y hogar asociados a sus cuentas.",
                "Los clientes pueden retirar efectivo en cajeros automáticos de Banorte utilizando su tarjeta de débito.",
                "Banorte proporciona acceso a servicios de banca móvil para una gestión fácil y segura de las cuentas.",
                "Los clientes de Banorte pueden solicitar créditos personales desde la banca en línea.",
                "Los pagos automáticos en Banorte pueden configurarse para servicios como electricidad, agua y teléfono.",
                "Banorte permite a los clientes establecer un PIN personalizado para sus tarjetas de crédito y débito.",
                "Los clientes deben realizar un depósito mínimo para abrir una cuenta de ahorro en Banorte.",
                "Banorte ofrece tarjetas adicionales a los titulares de tarjetas de crédito, sujetas a ciertas condiciones.",
                "Los titulares de cuentas de Banorte pueden recibir alertas vía correo electrónico sobre transacciones.",
                "Las cuentas de nómina de Banorte están exentas de ciertas comisiones.",
                "Banorte ofrece beneficios exclusivos a clientes con cuentas de alto saldo promedio.",
                "Los clientes pueden recibir asesoría sobre créditos hipotecarios en cualquier sucursal de Banorte.",
                "Banorte realiza una evaluación de riesgo antes de aprobar cualquier solicitud de crédito.",
                "Los clientes deben actualizar su firma en Banorte si cambia su documento de identificación oficial.",
                "Banorte permite realizar transferencias internacionales desde la banca en línea.",
                "Los clientes de Banorte pueden recibir promociones y ofertas especiales según el tipo de cuenta.",
                "Banorte ofrece un programa de recompensas para los titulares de tarjetas de crédito.",
                "Las cuentas de ahorro infantiles en Banorte deben ser supervisadas por un tutor legal.",
                "Los clientes pueden recibir estados de cuenta impresos, si así lo solicitan, en Banorte.",
                "Banorte permite realizar retiros sin tarjeta utilizando la aplicación de banca móvil.",
                "Los clientes deben presentar una identificación oficial vigente para realizar retiros mayores a cierta cantidad en Banorte.",
                "Banorte ofrece planes de ahorro programado para metas financieras específicas.",
                "Los clientes de Banorte pueden cancelar una tarjeta de crédito llamando al servicio al cliente.",
                "Banorte puede cobrar una penalización si se cancela un crédito antes de lo acordado.",
                "Las transferencias entre cuentas de Banorte son inmediatas y sin costo adicional.",
                "Los clientes de Banorte pueden elegir recibir sus tarjetas de crédito en su domicilio.",
                "Banorte ofrece una opción de préstamos express con aprobación rápida.",
                "Los créditos hipotecarios de Banorte pueden tener tasas fijas o variables según la preferencia del cliente.",
                "Banorte proporciona información detallada sobre las tasas de interés aplicables a sus productos financieros.",
                "Los clientes pueden solicitar un cambio de tipo de cuenta en Banorte según sus necesidades financieras.",
                "Banorte permite realizar pagos de tarjetas de crédito de otros bancos desde la banca en línea.",
                "Los clientes deben proporcionar una dirección de correo electrónico válida para recibir notificaciones de Banorte.",
                "Banorte ofrece créditos educativos con condiciones preferenciales para estudiantes.",
                "Los clientes pueden descargar la aplicación de Banorte para monitorear sus transacciones en cualquier momento.",
                "Banorte proporciona servicios de banca personalizada para clientes premium.",
                "Los clientes pueden solicitar asesoría en inversiones con un especialista financiero de Banorte.",
                "Banorte cuenta con una línea de atención exclusiva para reportar tarjetas perdidas o robadas.",
                "Los clientes deben presentar una justificación documentada para retiros en efectivo superiores a cierto monto en Banorte.",
                "Banorte ofrece cuentas especiales para pequeñas y medianas empresas.",
                "Los titulares de cuentas empresariales en Banorte pueden acceder a servicios adicionales, como líneas de crédito.",
                "Los clientes pueden cambiar el NIP de sus tarjetas en cajeros automáticos Banorte.",
                "Banorte cobra comisiones por operaciones en cajeros automáticos internacionales.",
                "Los clientes pueden solicitar chequeras para sus cuentas corrientes en Banorte.",
                "Banorte ofrece descuentos en tiendas y comercios asociados para clientes de tarjetas de crédito.",
                "Las cuentas de plazo fijo en Banorte ofrecen tasas de interés garantizadas por el período contratado.",
                "Los clientes de Banorte pueden realizar consultas de saldo en cajeros automáticos sin costo.",
                "Banorte proporciona herramientas en línea para planificar la adquisición de una vivienda.",
                "Los clientes pueden solicitar un aumento de límite en sus tarjetas de crédito a través de la aplicación Banorte.",
                "Banorte permite a los clientes realizar pagos diferidos en sus tarjetas de crédito.",
                "Los clientes deben proporcionar un comprobante de ingresos actualizado para solicitar créditos en Banorte.",
                "Banorte ofrece tarjetas de crédito sin cuota anual bajo ciertas condiciones.",
            ]
        )
