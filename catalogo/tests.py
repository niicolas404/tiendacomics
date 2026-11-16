from unittest.mock import call, patch

from django.core.exceptions import ValidationError
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase

from .models import Comic, Reserva
from .validators import validar_rut
from .views import base


class ComicSearchTests(SimpleTestCase):
    @patch('catalogo.views.Editorial.objects.all', return_value=[])
    @patch('catalogo.views.Comic.objects.filter')
    def test_title_and_editorial_filters_can_be_combined(
        self, comic_filter, editorial_all
    ):
        comics = comic_filter.return_value
        comics.filter.return_value = comics

        base(RequestFactory().get('/', {'q': 'Batman', 'editorial': '2'}))

        self.assertEqual(comic_filter.call_args, call(disponible=True))
        self.assertEqual(
            comics.filter.call_args_list,
            [
                call(titulo__icontains='Batman'),
                call(editorial_id='2'),
            ],
        )
        editorial_all.assert_called_once_with()


class ComicDetailAvailabilityTests(SimpleTestCase):
    @patch('catalogo.views.get_object_or_404', side_effect=Http404)
    def test_missing_or_unavailable_comic_returns_404(self, comic_lookup):
        response = self.client.get('/reservar/999')

        self.assertEqual(response.status_code, 404)
        comic_lookup.assert_called_once_with(Comic, id=999, disponible=True)


class ComicAvailabilityTests(SimpleTestCase):
    def test_disponibilidad_is_independent_of_stock(self):
        self.assertTrue(Comic(disponible=True, stock=0).disponible)
        self.assertFalse(Comic(disponible=False, stock=5).disponible)


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
