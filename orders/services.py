from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_order_confirmation_email(order):
    """
    Envoie un email de confirmation de commande
    """
    subject = f'Confirmation de commande #{order.id} - Boutique E-commerce'
    
    # Contexte pour le template
    context = {
        'order': order,
        'items': order.items.all(),
        'total': order.total_amount,
    }
    
    # Générer le contenu HTML de l'email
    html_message = render_to_string('orders/email/order_confirmation.html', context)
    
    # Version texte simple
    plain_message = strip_tags(html_message)
    
    # Envoyer l'email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER or 'noreply@boutique-ecommerce.com',
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False

def send_order_notification_to_admin(order):
    """
    Envoie une notification à l'administrateur pour une nouvelle commande
    """
    subject = f'Nouvelle commande #{order.id} - {order.customer_name}'
    
    context = {
        'order': order,
        'items': order.items.all(),
        'total': order.total_amount,
    }
    
    html_message = render_to_string('orders/email/order_notification_admin.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER or 'noreply@boutique-ecommerce.com',
            recipient_list=[settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@boutique-ecommerce.com'],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification admin: {e}")
        return False 