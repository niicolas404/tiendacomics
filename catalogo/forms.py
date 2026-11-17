from django import forms

from .validators import validar_rut


class FormReserva(forms.Form):
    nombre_cliente = forms.CharField(max_length=50, label="Nombre")
    correo_cliente = forms.EmailField(max_length=50, label="Correo")
    rut_cliente = forms.CharField(
        max_length=12, label="RUT", validators=[validar_rut]
    )
    cantidad_ejemplares = forms.IntegerField(
        min_value=1,
        max_value=3,
        label="Cantidad de ejemplares",
        error_messages={
            'min_value': 'La cantidad mínima es 1.',
            'max_value': 'La cantidad máxima es 3.',
        },
    )

    nombre_cliente.widget.attrs['class'] = 'form-control'
    correo_cliente.widget.attrs['class'] = 'form-control'
    rut_cliente.widget.attrs['class'] = 'form-control'
    cantidad_ejemplares.widget.attrs['class'] = 'form-control'