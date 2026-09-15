from django.shortcuts import render, get_object_or_404
from .models import Biscuit


def biscuit_list(request):

    biscuits = Biscuit.objects.filter(
        available=True
    ).order_by('-created_at')

    return render(
        request,
        'products/biscuit_list.html',
        {
            'biscuits': biscuits
        }
    )


def biscuit_detail(request, id):

    biscuit = get_object_or_404(
        Biscuit,
        id=id
    )

    return render(
        request,
        'products/biscuit_detail.html',
        {
            'biscuit': biscuit
        }
    )