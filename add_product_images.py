#!/usr/bin/env python
"""
Script pour ajouter des images aux produits existants
"""
import os
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

def add_product_images():
    """Ajoute des images aux produits existants"""
    
    # Dictionnaire des images par produit
    product_images = {
        'Tomates Fraîches': 'tomates.jpg',
        'Pain Artisanal': 'pain.jpg', 
        'Fromage de Chèvre': 'fromage.jpg',
        'Miel Local': 'miel.jpg',
        'Pommes Bio': 'pommes.jpg',
        'Huile d\'Olive Extra Vierge': 'huile-olive.jpg'
    }
    
    # Créer le dossier media/products s'il n'existe pas
    media_dir = Path('media/products')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    print("📸 Ajout d'images aux produits...")
    print("=" * 50)
    
    for product in Product.objects.all():
        if product.name in product_images:
            image_name = product_images[product.name]
            image_path = media_dir / image_name
            
            # Vérifier si l'image existe
            if image_path.exists():
                # Mettre à jour le produit avec l'image
                product.image = f'products/{image_name}'
                product.save()
                print(f"✅ {product.name} - Image ajoutée: {image_name}")
            else:
                print(f"⚠️  {product.name} - Image manquante: {image_name}")
        else:
            print(f"❌ {product.name} - Aucune image définie")
    
    print("\n📋 Instructions pour ajouter des images :")
    print("1. Placez vos images dans le dossier 'media/products/'")
    print("2. Nommez-les selon la liste ci-dessus")
    print("3. Formats supportés : JPG, PNG, GIF")
    print("4. Taille recommandée : 400x400 pixels")
    print("\n📁 Dossier d'images :", media_dir.absolute())

def create_sample_images():
    """Crée des images d'exemple avec du texte"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ PIL/Pillow non installé. Installez-le avec : pip install Pillow")
        return
    
    media_dir = Path('media/products')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Images à créer
    images_to_create = {
        'tomates.jpg': '🍅 Tomates Fraîches',
        'pain.jpg': '🥖 Pain Artisanal',
        'fromage.jpg': '🧀 Fromage de Chèvre', 
        'miel.jpg': '🍯 Miel Local',
        'pommes.jpg': '🍎 Pommes Bio',
        'huile-olive.jpg': '🫒 Huile d\'Olive'
    }
    
    print("🎨 Création d'images d'exemple...")
    
    for filename, text in images_to_create.items():
        # Créer une image 400x400
        img = Image.new('RGB', (400, 400), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Ajouter du texte
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Centrer le texte
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (400 - text_width) // 2
        y = (400 - text_height) // 2
        
        draw.text((x, y), text, fill='#333333', font=font)
        
        # Sauvegarder l'image
        img_path = media_dir / filename
        img.save(img_path, 'JPEG', quality=85)
        print(f"✅ Créé : {filename}")
    
    print(f"\n📁 Images créées dans : {media_dir.absolute()}")

if __name__ == '__main__':
    print("🖼️  Gestionnaire d'images pour les produits")
    print("=" * 50)
    
    choice = input("Choisissez une option :\n1. Ajouter des images existantes\n2. Créer des images d'exemple\nVotre choix (1 ou 2) : ")
    
    if choice == '1':
        add_product_images()
    elif choice == '2':
        create_sample_images()
        add_product_images()  # Ajouter les images créées aux produits
    else:
        print("❌ Choix invalide") 