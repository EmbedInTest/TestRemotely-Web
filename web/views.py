from datetime import datetime
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .models import Device, Board, BoardStatus, Run
from .serializers import DeviceSerializer, BoardSerializer, BoardStatusSerializer, RunSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(device__owner=self.request.user)


class BoardStatusViewSet(ModelViewSet):
    serializer_class = BoardStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BoardStatus.objects.filter(board__device__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(last_update=datetime.now())

    def perform_update(self, serializer):
        serializer.save(last_update=datetime.now())


class RunStatusViewSet(ModelViewSet):
    serializer_class = RunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Run.objects.filter(board_status__board__device__owner=self.request.user)
