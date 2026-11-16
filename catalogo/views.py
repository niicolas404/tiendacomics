from django.shortcuts import render
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

    form = FormReserva()
    form.fields['id_comic'].initial = comic_id
    comic = Comic.objects.get(id=comic_id)
    data = {'comic': comic, 'form': form}
    return render(request, 'reservar.html', data)