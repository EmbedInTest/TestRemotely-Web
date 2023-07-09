from datetime import datetime
from rest_framework import permissions, mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Device, Board, BoardStatus, Run, RunStatus, DeviceStatus
from .serializers import DeviceSerializer, BoardSerializer, BoardStatusSerializer, RunSerializer, RunStatusSerializer, DeviceStatusSerializer


class ModelViewCreateReadOnly(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()` and `list()` actions.
    """
    pass


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeviceStatusViewSet(ModelViewCreateReadOnly):
    serializer_class = DeviceStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeviceStatus.objects.filter(device__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(last_update=datetime.now())


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(device__owner=self.request.user)


class BoardStatusViewSet(ModelViewCreateReadOnly):
    serializer_class = BoardStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BoardStatus.objects.filter(board__device__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(last_update=datetime.now())


class RunViewSet(ModelViewSet):
    serializer_class = RunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Run.objects.filter(triggerer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(triggerer=self.request.user, dispatched_at=datetime.now())


class RunStatusViewSet(ModelViewCreateReadOnly):
    serializer_class = RunStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RunStatus.objects.filter(run__triggerer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(last_update=datetime.now())
