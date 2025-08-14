#!/usr/bin/env python
"""
Script pour lister les produits disponibles avec leurs IDs
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

def list_products():
    """Liste tous les produits avec leurs IDs"""
    
    products = Product.objects.all().order_by('id')
    
    if not products:
        print("Aucun produit trouvé dans la base de données.")
        return
    
    print("📦 PRODUITS DISPONIBLES :")
    print("=" * 50)
    
    for product in products:
        print(f"ID: {product.id}")
        print(f"Nom: {product.name}")
        print(f"Prix: {product.price} FCFA")
        print(f"Stock: {product.stock} unités")
        print(f"URL: http://localhost:8000/api/products/{product.id}/")
        print("-" * 30)
    
    print(f"\n✅ Total: {products.count()} produits")
    print("\n💡 Vous pouvez maintenant tester les liens dans votre application React !")

if __name__ == '__main__':
    list_products() 