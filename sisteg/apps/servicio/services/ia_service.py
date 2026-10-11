from django.conf import settings
from openai import OpenAI

from apps.servicio.schemas import AnalisisRecepcionIA


INSTRUCCIONES_RECEPCION = """
Eres un asistente de recepción para un taller de soporte técnico
y mantenimiento de computadoras.

Analiza únicamente el problema reportado por el cliente.

Tu función es:

1. Resumir el problema objetivamente.
2. Clasificar la incidencia.
3. Sugerir un nivel de prioridad.
4. Identificar posibles causas preliminares.
5. Proponer preguntas sencillas para realizar al cliente.

Reglas:

- No presentes las causas como un diagnóstico confirmado.
- No afirmes que se debe reemplazar una pieza.
- No inventes marcas, modelos, componentes o síntomas.
- No sugieras procedimientos peligrosos.
- Utiliza lenguaje comprensible para recepción.
- Devuelve como máximo cuatro posibles causas.
- Devuelve como máximo cuatro preguntas.
- Indica que el análisis debe ser validado por el técnico.
"""


def analizar_descripcion_mantenimiento(descripcion):
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "La clave OPENAI_API_KEY no está configurada."
        )

    cliente = OpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    respuesta = cliente.responses.parse(
        model=settings.OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": INSTRUCCIONES_RECEPCION,
            },
            {
                "role": "user",
                "content": (
                    "Analiza la siguiente descripción proporcionada "
                    "por el cliente:\n\n"
                    f"{descripcion}"
                ),
            },
        ],
        text_format=AnalisisRecepcionIA,
    )

    if respuesta.output_parsed is None:
        raise ValueError(
            "La IA no devolvió un análisis con la estructura esperada."
        )

    return respuesta.output_parsed.model_dump()