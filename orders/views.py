from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Biscuit

from .models import (
    CartItem,
    Order,
    OrderItem
)


@login_required
def add_to_cart(request, biscuit_id):

    biscuit = get_object_or_404(
        Biscuit,
        id=biscuit_id,
        available=True
    )

    if request.method == 'POST':

        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )

        if quantity < 1:
            quantity = 1

        if quantity > biscuit.stock:

            messages.error(
                request,
                f"Only {biscuit.stock} items are available."
            )

            return redirect(
                'biscuit_detail',
                id=biscuit.id
            )

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            biscuit=biscuit
        )

        if created:

            item.quantity = quantity

        else:

            new_quantity = item.quantity + quantity

            if new_quantity > biscuit.stock:

                new_quantity = biscuit.stock

                messages.warning(
                    request,
                    "Cart quantity adjusted to available stock."
                )

            item.quantity = new_quantity

        item.save()

        messages.success(
            request,
            f"{biscuit.name} added to your cart!"
        )

    return redirect('cart')


@login_required
def cart(request):

    items = CartItem.objects.filter(
        user=request.user
    ).select_related('biscuit')

    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        'orders/cart.html',
        {
            'items': items,
            'total': total
        }
    )


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Item removed from your cart."
    )

    return redirect('cart')


@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':

        quantity = int(
            request.POST.get(
                'quantity',
                1
            )
        )

        if quantity <= 0:

            item.delete()

        elif quantity <= item.biscuit.stock:

            item.quantity = quantity
            item.save()

        else:

            item.quantity = item.biscuit.stock
            item.save()

            messages.warning(
                request,
                "Quantity adjusted to available stock."
            )

    return redirect('cart')


@login_required
def checkout(request):

    items = CartItem.objects.filter(
        user=request.user
    ).select_related('biscuit')

    if not items.exists():

        messages.info(
            request,
            "Your cart is empty."
        )

        return redirect('cart')

    total = sum(
        item.total_price()
        for item in items
    )

    if request.method == 'POST':

        address = request.POST.get(
            'address',
            ''
        ).strip()

        if not address:

            messages.error(
                request,
                "Please enter your delivery address."
            )

            return render(
                request,
                'orders/checkout.html',
                {'total': total}
            )

        # Check stock again before placing order

        for item in items:

            if item.quantity > item.biscuit.stock:

                messages.error(
                    request,
                    f"Not enough stock for {item.biscuit.name}."
                )

                return redirect('cart')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                biscuit=item.biscuit,
                quantity=item.quantity,
                price=item.biscuit.price
            )

            item.biscuit.stock -= item.quantity

            if item.biscuit.stock == 0:

                item.biscuit.available = False

            item.biscuit.save()

        items.delete()

        return redirect(
            'order_success'
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'total': total
        }
    )


@login_required
def order_success(request):

    return render(
        request,
        'orders/order_success.html'
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__biscuit'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/myorders.html',
        {
            'orders': orders
        }
    )