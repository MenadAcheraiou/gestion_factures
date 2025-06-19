from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('produit/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produit/modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('produit/supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('factures/', views.liste_factures, name='liste_factures'),
    path('facture/creer/', views.creer_facture, name='creer_facture'),
    path('facture/<int:id>/', views.detail_facture, name='detail_facture'),
    path('facture/<int:id>/export/', views.export_csv_facture, name='export_csv_facture'),
]


