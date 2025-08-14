#!/usr/bin/env python
"""
Script pour ajouter des produits de test dans la base de données
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

def add_sample_products():
    """Ajoute des produits de test"""
    
    # Supprimer les produits existants
    Product.objects.all().delete()
    
    # Produits de test avec prix en FCFA
    products_data = [
        {
            'name': 'Tomates Fraîches',
            'description': 'Tomates bio cultivées localement, parfaites pour vos salades et sauces.',
            'price': 250,
            'stock': 25
        },
        {
            'name': 'Pain Artisanal',
            'description': 'Pain traditionnel cuit au four à bois, croûte dorée et mie moelleuse.',
            'price': 150,
            'stock': 15
        },
        {
            'name': 'Fromage de Chèvre',
            'description': 'Fromage de chèvre affiné, saveur douce et texture crémeuse.',
            'price': 1200,
            'stock': 8
        },
        {
            'name': 'Miel Local',
            'description': 'Miel pur récolté dans nos ruches, saveur naturelle et authentique.',
            'price': 2500,
            'stock': 12
        },
        {
            'name': 'Pommes Bio',
            'description': 'Pommes bio de saison, croquantes et juteuses.',
            'price': 300,
            'stock': 30
        },
        {
            'name': 'Huile d\'Olive Extra Vierge',
            'description': 'Huile d\'olive pressée à froid, saveur intense et fruitée.',
            'price': 3500,
            'stock': 10
        }
    ]
    
    # Créer les produits
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        print(f"Produit ajouté : {product.name} - {product.price} FCFA")
    
    print(f"\n✅ {len(products_data)} produits ajoutés avec succès !")
    print("Tu peux maintenant voir les produits dans l'API : http://127.0.0.1:8000/api/products/")

if __name__ == '__main__':
    add_sample_products() 