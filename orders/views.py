from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from .services import send_order_confirmation_email, send_order_notification_to_admin

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Créer une nouvelle commande"""
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Envoyer l'email de confirmation au client
            email_sent = send_order_confirmation_email(order)
            
            # Envoyer la notification à l'admin
            admin_notification_sent = send_order_notification_to_admin(order)
            
            response_data = {
                'message': 'Commande créée avec succès !',
                'order_id': order.id,
                'status': 'success',
                'email_sent': email_sent,
                'admin_notification_sent': admin_notification_sent
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def confirm_order(self, request, pk=None):
        """Confirmer une commande"""
        order = self.get_object()
        order.status = 'confirmed'
        order.save()
        return Response({
            'message': 'Commande confirmée avec succès !',
            'order_id': order.id,
            'status': 'confirmed'
        })
