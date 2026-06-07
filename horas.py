"""
Time expression normalization.

Zuzanna Masklak

This module contains the normalizaHoras() function, which reads a text file
and writes another file where time expressions are normalized to the HH:MM
format using regular expressions.
"""

import re


PERIODO = (
    r"de la mañana|del mediodía|de la tarde|de la noche|de la madrugada"
)


def hora_con_periodo(hora, periodo):
    """
    Convert a 12-hour clock time according to the period of the day.
    If the combination is incorrect, return None.
    """
    if not 1 <= hora <= 12:
        return None

    if periodo == "de la mañana":
        if 4 <= hora <= 12:
            return hora
        return None

    if periodo == "del mediodía":
        if hora == 12:
            return 12
        if 1 <= hora <= 3:
            return hora + 12
        return None

    if periodo == "de la tarde":
        if 3 <= hora <= 8:
            return hora + 12
        return None

    if periodo == "de la noche":
        if hora == 12:
            return 0
        if 8 <= hora <= 11:
            return hora + 12
        if 1 <= hora <= 4:
            return hora
        return None

    if periodo == "de la madrugada":
        if 1 <= hora <= 6:
            return hora
        return None

    return None


def formato(hora, minuto):
    """
    Return a time in HH:MM format.
    """
    return f"{hora:02d}:{minuto:02d}"


def normalizaHoras(ficText, ficNorm):
    """
    Read ficText and write ficNorm with the time expressions normalized.
    """
    with open(ficText, encoding="utf-8") as entrada:
        texto = entrada.read()

    texto = normaliza_texto(texto)

    with open(ficNorm, "w", encoding="utf-8") as salida:
        salida.write(texto)


def normaliza_texto(texto):
    """
    Normalize the time expressions found in a text.
    """

    def cambia_horas_con_h(match):
        hora = int(match.group(1))
        minuto = int(match.group(2) or 0)
        periodo = match.group(3)

        if minuto > 59:
            return match.group(0)

        if periodo:
            hora = hora_con_periodo(hora, periodo)
            if hora is None:
                return match.group(0)
        elif not 0 <= hora <= 23:
            return match.group(0)

        return formato(hora, minuto)

    def cambia_estandar(match):
        hora = int(match.group(1))
        minuto = int(match.group(2))

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return formato(hora, minuto)

        return match.group(0)

    def cambia_en_punto_y_media(match):
        hora = int(match.group(1))
        expresion = match.group(2)
        periodo = match.group(3)

        if not 1 <= hora <= 12:
            return match.group(0)

        if expresion == "en punto":
            minuto = 0
        elif expresion == "y cuarto":
            minuto = 15
        elif expresion == "y media":
            minuto = 30
        else:
            minuto = 45

        if periodo:
            hora_normal = hora_con_periodo(hora, periodo)

            if hora_normal is None:
                return match.group(0)

            if expresion == "menos cuarto":
                hora_normal = (hora_normal - 1) % 24

            return formato(hora_normal, minuto)

        hora_normal = hora % 12

        if expresion == "menos cuarto":
            hora_normal = (hora_normal - 1) % 12

        return formato(hora_normal, minuto)

    def cambia_hora_con_periodo(match):
        hora = int(match.group(1))
        periodo = match.group(2)

        hora_normal = hora_con_periodo(hora, periodo)

        if hora_normal is None:
            return match.group(0)

        return formato(hora_normal, 0)

    patron_h = re.compile(
        rf"\b(\d{{1,2}})h(?:(\d{{1,2}})m)?"
        rf"(?:\s+({PERIODO}))?\b"
    )

    patron_en_punto = re.compile(
        rf"\b(\d{{1,2}})\s+"
        rf"(en punto|y cuarto|y media|menos cuarto)"
        rf"(?:\s+({PERIODO}))?\b"
    )

    patron_periodo = re.compile(
        rf"\b(\d{{1,2}})\s+({PERIODO})\b"
    )

    patron_estandar = re.compile(
        r"\b(\d{1,2}):([0-5]\d)\b"
    )

    texto = patron_h.sub(cambia_horas_con_h, texto)
    texto = patron_en_punto.sub(cambia_en_punto_y_media, texto)
    texto = patron_periodo.sub(cambia_hora_con_periodo, texto)
    texto = patron_estandar.sub(cambia_estandar, texto)

    return texto
