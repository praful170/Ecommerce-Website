from django.urls import path
from . import views

app_name = "App_Payment"

urlpatterns = [

    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('status/',views.complete,name='complete'),

]
