from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_details, name='cart_details'),
    path('add/<int:product_id>', views.add, name='cart_add'),
    path('remove/<int:product_id>', views.remove, name='cart_remove'),
]
