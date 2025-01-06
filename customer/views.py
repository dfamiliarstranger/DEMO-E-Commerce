
from django.shortcuts import render, redirect
from django.conf import settings
import stripe.error
from store.models import *
from store.serializer import ProductSerializer, CategorySerializer, CartSerializer, CartOrderItem, CartOrderItemSerializer, CartOrderSerializer, CouponSerializer, NotificationSerializer, ReviewSerializer, WishlistSerializer

from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
import stripe

class OrdersAPIView(generics.ListAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        orders = CartOrder.objects.filter(buyer=user, payment_status="paid")
        return orders
    
class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        order_oid = self.kwargs['order_oid']

        user = User.objects.get(id=user_id)

        order = CartOrder.objects.get(buyer=user, oid=order_oid, payment_status="paid")
        return order
    
class WishListAPIVIEW(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id= self.kwargs['user_id']

        user = User.objects.get(id=user_id)
        wishlist = Wishlist.objects.filter(user=user)
        return wishlist
    
    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload['product_id']
        user_id = payload['user_id']

        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)

        wishlist = Wishlist.objects.filter(product=product, user=user)
        if wishlist:
            wishlist.delete()
            return Response({"message":"Wishlist deleted successfully"}, status=status.HTTP_200_OK)
        else:
            Wishlist.objects.create(product=product, user=user)
            return Response({"message":"Added to wishlist"}, status=status.HTTP_201_CREATED)
        
class CustomerNotification(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        user = User.objects.get(id=user_id)
        return Notification.objects.filter(user=user, seen=False)
    
class MarkCustomerNotificationAsSeen(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        noti_id = self.kwargs['noti_id']

        user = User.objects.get(id=user_id)
        noti = Notification.objects.get(id=noti_id, user=user)

        if noti.seen != True:
            noti.seen = True
            noti.save()
        
        return noti