from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Billing_Address
from .forms import Billing_Form
from App_Order.models import Order,Cart

from django.contrib.auth.decorators import login_required

#Razorpay
import razorpay
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
@login_required
def checkout(request):
    saved_address = Billing_Address.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = Billing_Form(instance=saved_address)
    if request.method == 'POST':
        form = Billing_Form(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = Billing_Form(instance=saved_address)
            messages.success(request, "Shipping Address Saved!")

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()

    return render(request,'App_Payment/checkout.html', context={'form':form,'order_items':order_items,'order_total':order_total,'saved_address':saved_address})


@login_required
def payment(request):
    saved_address = Billing_Address.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request,'Please update your shipping address!')
        return redirect('App_Payment:checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request,'Please update your profile details!')
        return redirect("App_Login:profile")

    key_id = 'rzp_test_pcOeWDsVbX2wU9'
    key_secret = '2oo52keqAvNhbg8ZysQlUORI'


    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_item_count = order_qs[0].order_items.count()
    order_total = order_qs[0].get_totals()
    total_amount = int(order_total)
    current_user = request.user

    client = razorpay.Client(auth=(key_id, key_secret))

    data = {"amount": total_amount * 100, "currency": "INR", "receipt": "order_rcptid_11",'payment_capture':'1'}
    payment = client.order.create(data=data)
    # order = Order.objects.create(name=request.user.profile.Full_name, amount=total_amount, provider_order_id=payment["id"])



    # status_url = request.build_absolute_url(reverse('App_Payment:complete'))
    # mypayment.set_urls(success_url='example.com/success', fail_url='example.com/failed', cancel_url='example.com/cancel', ipn_url='example.com/payment_notification')



    return render(request,'App_Payment/payment.html',context={'payment':payment,'current_user':current_user})



def complete(request):
    return render(request,'App_Payment/complete.html',context={})
