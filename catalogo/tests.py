import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock, call, patch

from django.core.exceptions import ValidationError
from django.http import Http404
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .forms import FormReserva
from .models import Comic, Reserva
from .validators import validar_rut
from .views import base, reservar


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


class ReservaFormTests(SimpleTestCase):
    def test_validates_email_rut_and_quantity(self):
        form = FormReserva(data={
            'nombre_cliente': 'Ana Pérez',
            'correo_cliente': 'ana@example.com',
            'rut_cliente': '12.345.678-5',
            'cantidad_ejemplares': '3',
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_shows_errors_for_invalid_email_rut_and_quantity(self):
        form = FormReserva(data={
            'nombre_cliente': 'Ana Pérez',
            'correo_cliente': 'correo-invalido',
            'rut_cliente': '12.345.678-4',
            'cantidad_ejemplares': '4',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors),
            {'correo_cliente', 'rut_cliente', 'cantidad_ejemplares'},
        )

    def test_quantity_range_errors_are_in_spanish(self):
        for quantity, message in (
            ('0', 'La cantidad mínima es 1.'),
            ('4', 'La cantidad máxima es 3.'),
        ):
            with self.subTest(quantity=quantity):
                form = FormReserva(data={
                    'nombre_cliente': 'Ana Pérez',
                    'correo_cliente': 'ana@example.com',
                    'rut_cliente': '12.345.678-5',
                    'cantidad_ejemplares': quantity,
                })

                self.assertFalse(form.is_valid())
                self.assertEqual(
                    str(form.errors['cantidad_ejemplares'][0]),
                    message,
                )


class ReservaSubmissionTests(SimpleTestCase):
    @staticmethod
    def valid_data(cantidad='1'):
        return {
            'nombre_cliente': 'Ana Pérez',
            'correo_cliente': 'ana@example.com',
            'rut_cliente': '12.345.678-5',
            'cantidad_ejemplares': cantidad,
        }

    @staticmethod
    def comic_with_stock(stock):
        return SimpleNamespace(
            stock=stock,
            titulo='Batman',
            editorial='DC',
            autor='Autor',
            precio_chileno=MagicMock(return_value='$1.000'),
            tomo=1,
            portada=SimpleNamespace(url='/media/batman.jpg'),
            save=MagicMock(),
        )

    def test_rejects_reservation_above_available_stock(self):
        comic = self.comic_with_stock(stock=2)
        with (
            patch('catalogo.views.get_object_or_404', side_effect=[comic, comic]),
            patch('catalogo.views.Comic.objects.select_for_update'),
            patch('catalogo.views.transaction.atomic'),
            patch('catalogo.views.Reserva.objects.create') as create_reservation,
        ):
            response = reservar(
                RequestFactory().post('/reservar/1', self.valid_data(cantidad='3')),
                comic_id=1,
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn('Solo hay 2 ejemplares disponibles.', response.content.decode())
        create_reservation.assert_not_called()
        comic.save.assert_not_called()

    def test_saves_reservation_decreases_stock_and_redirects_to_receipt(self):
        comic = self.comic_with_stock(stock=5)
        reservation_code = uuid.uuid4()
        with (
            patch('catalogo.views.get_object_or_404', side_effect=[comic, comic]),
            patch('catalogo.views.Comic.objects.select_for_update'),
            patch('catalogo.views.transaction.atomic'),
            patch(
                'catalogo.views.Reserva.objects.create',
                return_value=MagicMock(codigo=reservation_code),
            ) as create_reservation,
        ):
            response = reservar(
                RequestFactory().post('/reservar/1', self.valid_data(cantidad='3')),
                comic_id=1,
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('comprobante', kwargs={'codigo': reservation_code}),
        )
        self.assertEqual(comic.stock, 2)
        comic.save.assert_called_once_with(update_fields=['stock'])
        create_reservation.assert_called_once_with(
            comic=comic,
            nombre_cliente='Ana Pérez',
            correo_cliente='ana@example.com',
            rut_cliente='12.345.678-5',
            cantidad_ejemplares=3,
        )

    def test_displays_exhausted_message_without_reservation_form(self):
        comic = self.comic_with_stock(stock=0)
        with patch('catalogo.views.get_object_or_404', return_value=comic):
            response = reservar(RequestFactory().get('/reservar/1'), comic_id=1)

        page = response.content.decode()
        self.assertIn('Agotado. No se pueden hacer reservas de este cómic.', page)
        self.assertNotIn('name="correo_cliente"', page)


class ComicAvailabilityTests(SimpleTestCase):
    def test_disponibilidad_is_independent_of_stock(self):
        self.assertTrue(Comic(disponible=True, stock=0).disponible)
        self.assertFalse(Comic(disponible=False, stock=5).disponible)

    @patch('catalogo.views.Editorial.objects.all', return_value=[])
    @patch('catalogo.views.Comic.objects.filter')
    def test_out_of_stock_comic_shows_detail_button(self, comic_filter, editorial_all):
        comic_filter.return_value = [SimpleNamespace(
            id=42,
            titulo='Batman',
            editorial='DC',
            precio_chileno='$1.000',
            stock=0,
            portada=None,
        )]

        response = base(RequestFactory().get('/'))
        page = response.content.decode()

        self.assertIn('AGOTADO', page)
        self.assertIn('href="reservar/42"', page)
        self.assertIn('VER DETALLE', page)


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
