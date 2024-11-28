from api.views import *
from django.urls import path


urlpatterns = [
    path('v1/users/', UserAPIView.as_view()),
    path('v1/click/', PointAPIView.as_view()),
    path('v1/click/<int:id>/', PointAPIView.as_view()),
    path('v1/ticket/', TicketAPIView.as_view()),
]
