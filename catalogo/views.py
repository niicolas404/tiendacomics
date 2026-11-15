from django.shortcuts import render
from catalogo.models import Comic, Editorial, Reserva


def base(request):
    comics = Comic.objects.filter(disponible=True)
    data = {'comics': comics}
    return render(request, 'base.html', data)