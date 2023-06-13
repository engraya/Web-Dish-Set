from django.urls import path

from . import views


urlpatterns = [
    path("shop", views.shop, name="shop"),
    path("", views.landingPage, name="landingPage"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contactPage", views.contactPage, name="contactPage"),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),

	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]
