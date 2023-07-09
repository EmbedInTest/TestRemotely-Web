from rest_framework import serializers
from .models import Device, Board, BoardStatus, Run, RunStatus


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    boards = serializers.HyperlinkedRelatedField(many=True, view_name='board-detail', read_only=True)

    class Meta:
        model = Device
        fields = ['url', 'id', 'name', 'owner', 'boards']


class DeviceFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context.get('request').user
        queryset = Device.objects.filter(owner=user)
        return queryset


class DeviceStatusSerializer(serializers.ModelSerializer):
    device = DeviceFilteredPrimaryKeyRelatedField()
    last_update = serializers.ReadOnlyField()

    class Meta:
        model = BoardStatus
        fields = ['url', 'id', 'device', 'status', 'last_update']


class BoardSerializer(serializers.ModelSerializer):
    status = serializers.HyperlinkedRelatedField(many=True, view_name='boardstatus-detail', read_only=True)
    device = DeviceFilteredPrimaryKeyRelatedField()

    class Meta:
        model = Board
        fields = ['url', 'id', 'name', 'path', 'device', 'status']


class BoardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        user = self.context.get('request').user
        queryset = Board.objects.filter(device__owner=user)
        return queryset


class BoardStatusSerializer(serializers.ModelSerializer):
    board = BoardFilteredPrimaryKeyRelatedField()
    last_update = serializers.ReadOnlyField()

    class Meta:
        model = BoardStatus
        fields = ['url', 'id', 'board', 'status', 'last_update']


class RunSerializer(serializers.ModelSerializer):
    triggerer = serializers.ReadOnlyField(source='owner.username')
    dispatched_at = serializers.ReadOnlyField()
    board = BoardFilteredPrimaryKeyRelatedField(allow_null=True, required=False)

    class Meta:
        model = Run
        fields = ['url', 'id', 'triggerer', 'file', 'dispatched_at', 'board']


class RunFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context.get('request').user
        queryset = Run.objects.filter(triggerer=user)
        return queryset


class RunStatusSerializer(serializers.ModelSerializer):
    run = RunFilteredPrimaryKeyRelatedField()
    last_update = serializers.ReadOnlyField()

    class Meta:
        model = RunStatus
        fields = ['url', 'id', 'run', 'status', 'last_update']
