from django.db import models



class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    date_peremption = models.DateField()

    def __str__(self):
        return self.nom

class Facture(models.Model):
    produits= models.ManyToManyField(Produit)
    client = models.CharField(max_length=100,default="Client")
    date_creation = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(ligne.produit.prix * ligne.quantite for ligne in self.lignes.all())

    def nombre_produits(self):
        return sum(ligne.quantite for ligne in self.lignes.all())
        
    def __str__(self):
        return f"Facture #{self.id} - {self.client}"

class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def sous_total(self):
        return self.produit.prix * self.quantite
        
        
    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

