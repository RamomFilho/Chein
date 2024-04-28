from django.urls import path, include

from produto import views

urlpatterns = [
    path('latest-products/', views.ListaUltimosProdutos.as_view()),
    path('products/search/', views.search),
    path('products/<slug:categoria_slug>/<slug:produto_slug>/', views.DetalheProduto.as_view()),
    path('products/<slug:categoria_slug>/', views.DetalheCategoria.as_view()),
]