from rest_framework import serializers
from .models import Device, Board, BoardStatus, Run


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


class BoardSerializer(serializers.ModelSerializer):
    status = serializers.HyperlinkedRelatedField(many=True, view_name='boardstatus-detail', read_only=True)
    device = DeviceFilteredPrimaryKeyRelatedField()

    class Meta:
        model = Board
        fields = ['url', 'id', 'name', 'path', 'device', 'status']


class BoardFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
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


class BoardStatusFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context.get('request').user
        queryset = BoardStatus.objects.filter(board__device__owner=user)
        return queryset


class RunSerializer(serializers.ModelSerializer):
    board_status = BoardStatusFilteredPrimaryKeyRelatedField()
    triggerer = serializers.ReadOnlyField(source='owner.username')
    dispatched_at = serializers.ReadOnlyField()

    class Meta:
        model = Run
        fields = ['url', 'id', 'board_status', 'triggerer', 'status', 'file', 'dispatched_at']
