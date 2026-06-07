"""
Student grades processing.

Zuzanna Masklak

This module defines the Alumno class and the leeAlumnos() function, which
reads a text file containing student data using regular expressions.
"""

import re


class Alumno:
    """
    Class used to process student grades. Each student has the following
    attributes:
    numIden:   Identification number. It is an integer. If it is not given,
               its default value is 'numIden=-1'.
    nombre:    Full name of the student.
    notas:     List of real numbers with the student's grades.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Return a new Alumno object with its list of grades extended with the
        value passed as an argument. In this way, adding a grade to an Alumno
        is done with the command 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Return the student's average grade.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Return the official representation of the student. By copying and
        pasting the resulting string, it is possible to create an identical
        Alumno object.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Return the pretty representation of the student. It displays three
        tab-separated columns: the identification number, the full name and
        the student's average grade with one decimal place.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Read a student file and return a dictionary.
    The dictionary key is the student's name, and the value is the
    corresponding Alumno object.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumnos = {}

    patron = re.compile(
        r"^\s*(\d+)\s+(.+?)\s+((?:\d+(?:\.\d+)?\s*)+)$"
    )

    with open(ficAlum, encoding="utf-8") as fichero:
        for linea in fichero:
            linea = linea.strip()

            if not linea:
                continue

            coincidencia = patron.fullmatch(linea)

            if coincidencia:
                num_iden = int(coincidencia.group(1))
                nombre = coincidencia.group(2)
                notas = [
                    float(nota)
                    for nota in re.findall(r"\d+(?:\.\d+)?", coincidencia.group(3))
                ]

                alumnos[nombre] = Alumno(nombre, num_iden, notas)

    return alumnos


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)