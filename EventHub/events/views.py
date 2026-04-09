from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_queryset(self):
        queryset = Event.objects.all()
        status = self.request.query_params.get('status')
        # if status in ['upcoming', 'ongoing', 'completed', 'cancelled']:
        #     queryset = queryset.filter(status=status)
        venue = self.request.query_params.get('venue')
        # if venue:
        #     queryset = queryset.filter(venu__icontains=venue)
        if status:
            queryset = queryset.filter(status=status)
        if venue:
            queryset = queryset.filter(venu__icontains=venue)
        return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    def get_queryset(self):
        queryset = Reservation.objects.all()
        event_id = self.request.query_params.get('event_id')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset
    @action(detail=True, methods=['post'], url_path='cancel')
    def delete(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'cancelled':
            return Response({'error': 'Already cancelled reservation.'}, status=400)
        reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()
        reservation.status = 'cancelled'
        reservation.save()
        return Response(self.get_serializer(reservation).data)