from django.urls import path

from . import views


urlpatterns = [
    path("shop", views.shop, name="shop"),
    path("", views.landingPage, name="landingPage"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contactPage", views.contactPage, name="contactPage"),

	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
