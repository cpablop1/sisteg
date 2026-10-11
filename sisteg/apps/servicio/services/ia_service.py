import random
import time

from django.conf import settings
from google import genai
from google.genai import errors

from apps.servicio.schemas import AnalisisRecepcionIA


INSTRUCCIONES_RECEPCION = """
Eres un asistente de recepción para un taller de soporte técnico
y mantenimiento de computadoras.

Analiza únicamente el problema reportado por el cliente.

Tu función es:

1. Resumir el problema de manera clara y objetiva.
2. Clasificar la incidencia.
3. Sugerir un nivel de prioridad.
4. Identificar posibles causas preliminares.
5. Proponer preguntas sencillas para realizar al cliente.

Reglas obligatorias:

- No presentes las posibles causas como diagnóstico confirmado.
- No afirmes que una pieza debe reemplazarse.
- No inventes marcas, modelos, componentes o síntomas.
- No sugieras procedimientos peligrosos.
- Utiliza lenguaje comprensible para recepción.
- Devuelve como máximo cuatro posibles causas.
- Devuelve como máximo cuatro preguntas.
- Indica que el análisis debe ser validado por el técnico.
"""


def analizar_descripcion_mantenimiento(descripcion):
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "La clave GEMINI_API_KEY no está configurada."
        )

    cliente = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    prompt = f"""
{INSTRUCCIONES_RECEPCION}

Descripción proporcionada por el cliente:

{descripcion}
"""

    maximo_intentos = 3

    for intento in range(1, maximo_intentos + 1):
        try:
            respuesta = cliente.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": (
                        AnalisisRecepcionIA.model_json_schema()
                    ),
                    "temperature": 0.2,
                },
            )

            if not respuesta.text:
                raise ValueError(
                    "La inteligencia artificial no devolvió un análisis."
                )

            analisis = AnalisisRecepcionIA.model_validate_json(
                respuesta.text
            )

            return analisis.model_dump()

        except errors.ServerError as error:
            codigo_estado = getattr(error, "code", None)

            if codigo_estado is None:
                codigo_estado = getattr(
                    error,
                    "status_code",
                    None,
                )

            es_error_temporal = (
                codigo_estado == 503
                or "503" in str(error)
                or "UNAVAILABLE" in str(error).upper()
            )

            if not es_error_temporal:
                raise

            if intento >= maximo_intentos:
                raise

            espera_base = 2 ** (intento - 1)
            variacion = random.uniform(0, 1)
            tiempo_espera = espera_base + variacion

            time.sleep(tiempo_espera)