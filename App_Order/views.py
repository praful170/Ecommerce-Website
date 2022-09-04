from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from .models import Cart,Order
from App_Shop.models import Product


from django.contrib import messages

# Create your views here.

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)                         #add new object to the cart or add to the existing one(quantity+)
    order_qs = Order.objects.filter(user=request.user, ordered=False)                                              #incomplete ordered
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'This item quantity is updated')
            return redirect("App_Shop:home")
        else:
            order.order_items.add(order_item[0])
            messages.info(request, 'This item is addedd to your cart')
            return redirect("App_Shop:home")

    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, 'This item is added to your cart')
        return redirect("App_Shop:home")

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart.html',context={'carts':carts,'order':order})

    else:
        messages.warning(request,'You dont have any item in your cart!')
        return redirect('App_Shop:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove()
            order_item.delete()
            messages.warning(request, 'This item is removed from your cart!')
            return redirect("App_Order:cart")

        else:
            messages.info("This item is in your cart!")
            return redirect("App_Shop:home")

    else:
        messages.info(request, "You don't have any active order!")
        return redirect("App_Shop:home")


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.name} is not in your cart")
                return redirect("App_Shop:home")
        else:
            messages.info(request, "You dont have an active order")
            return redirect("App_Shop:home")

@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("App_Order:cart")
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has been removed from your cart")
                return redirect("App_Order:cart")
        else:
            messages.info(request, "You dont have an active order")
            return redirect("App_Shop:home")
