from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import Comic, Reserva
from .validators import validar_rut


class ComicAvailabilityTests(SimpleTestCase):
    def test_disponible_depends_on_stock(self):
        self.assertTrue(Comic(stock=1).disponible)
        self.assertFalse(Comic(stock=0).disponible)


class ValidarRutTests(SimpleTestCase):
    def test_accepts_valid_rut_formats(self):
        for rut in ("12.345.678-5", "12345678-5", "123456785", "6-K", "6-k"):
            with self.subTest(rut=rut):
                validar_rut(rut)

    def test_rejects_invalid_checksum(self):
        with self.assertRaises(ValidationError):
            validar_rut("12.345.678-4")

    def test_rejects_malformed_rut_as_validation_error(self):
        for rut in (
            "1K-2",
            "abc12.345.678-5",
            "12..345.678-5",
            "123456789-5",
            "",
        ):
            with self.subTest(rut=rut):
                with self.assertRaises(ValidationError):
                    validar_rut(rut)


class ReservaValidationTests(SimpleTestCase):
    def test_quantity_must_be_at_least_one(self):
        quantity_field = Reserva._meta.get_field("cantidad_ejemplares")
        with self.assertRaises(ValidationError):
            quantity_field.clean(0, None)
        self.assertEqual(quantity_field.clean(1, None), 1)
