from django.urls import path

from pedido import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('orders/', views.ListaPedidos.as_view()),  
]
