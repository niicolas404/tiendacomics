from django.shortcuts import render
from catalogo.models import Comic, Editorial, Reserva

from catalogo.forms import FormReserva

def base(request):
    comics = Comic.objects.filter(disponible=True)
    data = {'comics': comics}
    return render(request, 'base.html', data)

def reservar(request, comic_id):

    form = FormReserva()
    form.fields['id_comic'].initial = comic_id
    comic = Comic.objects.get(id=comic_id)
    data = {'comic': comic, 'form': form}
    return render(request, 'reservar.html', data)