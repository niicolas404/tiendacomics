from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from catalogo.models import Comic, Editorial, Reserva

from catalogo.forms import FormReserva

def base(request):
    comics = Comic.objects.filter(disponible=True)
    search_query = request.GET.get('q', '').strip()
    selected_editorial = request.GET.get('editorial', '')

    if search_query:
        comics = comics.filter(titulo__icontains=search_query)
    if selected_editorial.isdecimal():
        comics = comics.filter(editorial_id=selected_editorial)

    data = {
        'comics': comics,
        'editoriales': Editorial.objects.all(),
        'search_query': search_query,
        'selected_editorial': selected_editorial,
    }
    return render(request, 'base.html', data)

def reservar(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id, disponible=True)

    if request.method == 'POST':
        form = FormReserva(request.POST)
        if form.is_valid():
            with transaction.atomic():
                comic = get_object_or_404(
                    Comic.objects.select_for_update(),
                    id=comic_id,
                    disponible=True,
                )
                cantidad = form.cleaned_data['cantidad_ejemplares']
                if cantidad > comic.stock:
                    form.add_error(
                        'cantidad_ejemplares',
                        f'Solo hay {comic.stock} ejemplares disponibles.',
                    )
                else:
                    reserva = Reserva.objects.create(
                        comic=comic,
                        nombre_cliente=form.cleaned_data['nombre_cliente'],
                        correo_cliente=form.cleaned_data['correo_cliente'],
                        rut_cliente=form.cleaned_data['rut_cliente'],
                        cantidad_ejemplares=cantidad,
                    )
                    comic.stock -= cantidad
                    comic.save(update_fields=['stock'])
                    return redirect('comprobante', codigo=reserva.codigo)
    else:
        form = FormReserva()

    data = {'comic': comic, 'form': form}
    return render(request, 'reservar.html', data)


def comprobante(request, codigo):
    reserva = get_object_or_404(Reserva, codigo=codigo)
    return render(request, 'comprobante.html', {'reserva': reserva})