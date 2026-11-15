from django.shortcuts import render


def base(request):
    data = {}
    return render(request, 'base.html', data)