import re
from django.core.exceptions import ValidationError


def validar_rut(value):
    rut = str(value).strip()
    formatos_validos = (
        re.fullmatch(r"[0-9]+[0-9kK]", rut)
        or re.fullmatch(r"[0-9]+-[0-9kK]", rut)
        or re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{3})+-[0-9kK]", rut)
    )
    if not formatos_validos:
        raise ValidationError("El formato del RUT no es válido.", code="invalid")

    rut_limpio = rut.replace(".", "").replace("-", "")
    cuerpo = rut_limpio[:-1]
    digito_verificador = rut_limpio[-1].upper()

    if len(cuerpo) > 8 or int(cuerpo) == 0:
        raise ValidationError("El RUT ingresado no es válido.", code="invalid")

    suma = 0
    multiplo = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    esperado = 11 - (suma % 11)
    if esperado == 11:
        digito_calculado = "0"
    elif esperado == 10:
        digito_calculado = "K"
    else:
        digito_calculado = str(esperado)

    if digito_calculado != digito_verificador:
        raise ValidationError(
            "El dígito verificador del RUT no es válido.",
            code="invalid",
        )
