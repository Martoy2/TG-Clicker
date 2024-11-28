from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, PoolSerializer, HistorySerializer
from main.models import TelegramUser, Pool, History
from django.utils import timezone
# Create your views here.
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class TicketAPIView(APIView):
    def get(self, request):
        ticket_instance = get_object_or_404(Pool, pool_name='Main')
        coin = ticket_instance.coin
        ticket = ticket_instance.ticket
        price = coin/ticket
        return Response({
            "price": round(price, 2),
        })

    def post(self, request):
        data = request.data
        coin = Decimal(data.get('coin'))
        ticket = data.get('ticket')
        user_id = data.get('user_id')

        if not coin:
            return Response({'error': 'Missing coin parameter'}, status=400)
        if not ticket:
            return Response({'error': 'Missing ticket parameter'}, status=400)
        if not user_id:
            return Response({'error': 'Missing user_id parameter'}, status=400)

        ticket_instance = get_object_or_404(Pool, pool_name='Main')
        ticket_instance.ticket = ticket_instance.ticket-ticket
        ticket_instance.coin = ticket_instance.coin + round(coin, 2)
        ticket_instance.save()
        user_instance = get_object_or_404(TelegramUser, user_id=user_id)
        user_instance.click -= round(coin, 2)
        user_instance.save()
        user_instance.ticket += ticket
        user_instance.save()
        new_data = {
            'user_id': user_id,
            'action': "Обмен",
            'ticket_count': ticket,
            'coin_count': round(coin, 2),
            'balance': Decimal(user_instance.click)
        }
        history_ser = HistorySerializer(data=new_data)
        if history_ser.is_valid():
            history_ser.save()
            return Response(history_ser.data, status=status.HTTP_201_CREATED)
        else:
            print("DON'T Save logs")
            return Response({"error": f"{history_ser.errors} {coin}"} , status=400)

        return Response(status=200)


class UserAPIView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointAPIView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        new_click = Decimal(data.get('clicks'))

        if not user_id:
            return Response({'error': 'Missing user_id parameter'}, status=400)
        if not new_click:
            return Response({'error': 'Missing new_click parameter'}, status=400)

        user_instance = get_object_or_404(TelegramUser, user_id = user_id)

        user_instance.click += round(new_click, 2)
        user_instance.save()
        new_data = {
            'user_id': user_id,
            'action': "Клик",
            'ticket_count': -1,
            'coin_count': new_click,
            'balance': user_instance.click
        }
        history_ser = HistorySerializer(data=new_data)
        if history_ser.is_valid():
            history_ser.save()
            return Response(history_ser.data, status=status.HTTP_201_CREATED)
        else:
            print("DON'T Save logs")
        return Response(status=200)

    def get(self, request, id):
        try:
            user_instance = get_object_or_404(TelegramUser, user_id=id)

            points = user_instance.click
            return Response({
                "user_id": id,
                "click": round(points, 0)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)