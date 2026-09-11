from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Event
from .serializers import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()

        search = self.request.query_params.get('search')

        venue = self.request.query_params.get('venue')

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        if venue:
            queryset = queryset.filter(
                venue__icontains=venue
            )

        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdminUser()]


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]

        return [IsAdminUser()]