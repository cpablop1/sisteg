from typing import Literal

from pydantic import BaseModel, Field


class AnalisisRecepcionIA(BaseModel):
    resumen: str = Field(
        description="Resumen claro y objetivo del problema reportado."
    )

    categoria: Literal[
        "Hardware",
        "Software",
        "Red",
        "Seguridad",
        "Rendimiento",
        "Periféricos",
        "Energía",
        "Otro",
    ]

    subcategoria: str = Field(
        description="Clasificación específica del problema."
    )

    prioridad: Literal[
        "Baja",
        "Media",
        "Alta",
        "Crítica",
    ]

    posibles_causas: list[str] = Field(
        description="Entre una y cuatro causas preliminares."
    )

    preguntas_sugeridas: list[str] = Field(
        description="Entre una y cuatro preguntas para el cliente."
    )

    advertencia: str = Field(
        description="Aviso de que el análisis requiere validación técnica."
    )