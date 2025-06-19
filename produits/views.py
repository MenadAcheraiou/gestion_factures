from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Produit, Facture,LigneFacture
from .forms import ProduitForm
import csv
from django.http import HttpResponse

def export_csv_facture(request, id):
    facture = get_object_or_404(Facture, id=id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="facture_{id}.csv"'

    writer = csv.writer(response)

    # Informations générales de la facture
    writer.writerow([f"Facture n° {facture.id}"])
    writer.writerow([f"Client : {facture.client}"])
    writer.writerow([f"Date : {facture.date_creation.strftime('%d/%m/%Y %H:%M')}"])
    writer.writerow([])  # ligne vide

    # En-têtes
    writer.writerow(['Nom du produit', 'Prix unitaire (€)', 'Quantité', 'Sous-total (€)'])

    # Lignes de produits
    for ligne in facture.lignes.all():
        produit = ligne.produit
        quantite = ligne.quantite
        sous_total = produit.prix * quantite
        writer.writerow([produit.nom, f"{produit.prix:.2f}", quantite, f"{sous_total:.2f}"])

    # Total
    writer.writerow([])
    writer.writerow(['TOTAL', '', '', f"{facture.total():.2f} €"])

    return response

def liste_produits(request):
    query = request.GET.get('q', '')
    tri = request.GET.get('sort', 'nom')
    produits = Produit.objects.filter(nom__icontains=query).order_by(tri)
    paginator = Paginator(produits, 5)
    page = request.GET.get('page')
    produits_page = paginator.get_page(page)
    return render(request, 'produits/liste_produits.html', {'produits': produits_page, 'query': query, 'tri': tri})

def ajouter_produit(request):
    form = ProduitForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_produits')
    return render(request, 'produits/form_produit.html', {'form': form})

def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    form = ProduitForm(request.POST or None, instance=produit)
    if form.is_valid():
        form.save()
        return redirect('liste_produits')
    return render(request, 'produits/form_produit.html', {'form': form})

def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    produit.delete()
    return redirect('liste_produits')

def creer_facture(request):
    if request.method == 'POST':
        client_name = request.POST.get('client', 'Client')
        facture = Facture.objects.create(client=client_name)
        lignes_a_ajouter = []
        for key, value in request.POST.items():
            if key.startswith('produit_'):
                produit_id = key.split('_')[1]
                try:
                    quantite = int(value)
                    if quantite > 0:
                        produit = Produit.objects.get(id=produit_id)
                        lignes_a_ajouter.append((produit, quantite))
                except (ValueError, Produit.DoesNotExist):
                    continue

        if not lignes_a_ajouter:
            # Aucun produit sélectionné, afficher un message
            produits = Produit.objects.all()
            message = "Veuillez sélectionner au moins un produit avec une quantité > 0."
            return render(request, 'produits/creer_facture.html', {'produits': produits, 'message': message})


        for produit, quantite in lignes_a_ajouter:
            LigneFacture.objects.create(facture=facture, produit=produit, quantite=quantite)

        return redirect('detail_facture', facture.id)

    produits = Produit.objects.all()
    return render(request, 'produits/creer_facture.html', {'produits': produits})


def liste_factures(request):
    factures = Facture.objects.all()
    paginator = Paginator(factures, 5)
    page = request.GET.get('page')
    factures_page = paginator.get_page(page)
    return render(request, 'produits/liste_factures.html', {'factures': factures_page})

def detail_facture(request, id):
    facture = get_object_or_404(Facture, id=id)
    return render(request, 'produits/detail_facture.html', {'facture': facture})

