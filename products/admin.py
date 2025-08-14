from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'image_preview', 'created_at']
    list_filter = ['created_at', 'stock']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'description', 'price', 'stock')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />'
        return "Aucune image"
    image_preview.short_description = 'Aperçu'
    image_preview.allow_tags = True
