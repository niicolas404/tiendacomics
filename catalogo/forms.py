from django import forms

class FormReserva(forms.Form):

    id_comic = forms.IntegerField(widget=forms.HiddenInput())
    nombre_cliente = forms.CharField(max_length=50, label="Nombre")
    correo_cliente = forms.EmailField(max_length=50, label="Correo", required=False)
    rut_cliente = forms.CharField(max_length=12, label="RUT")
    cantidad_ejemplares = forms.IntegerField(min_value=1, max_value=3, label="Cantidad de ejemplares")

    id_comic.widget.attrs['class'] = 'form-control'
    nombre_cliente.widget.attrs['class'] = 'form-control'
    correo_cliente.widget.attrs['class'] = 'form-control'
    rut_cliente.widget.attrs['class'] = 'form-control'
    cantidad_ejemplares.widget.attrs['class'] = 'form-control'