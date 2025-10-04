from django.contrib.auth.models import User
from rest_framework import serializers

from app_run.models import Run, AthleteInfo


class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'first_name', 'last_name',
                  'type', 'runs_finished']
        read_only_fields = fields

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'

class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='athlete.id', read_only=True)

    class Meta:
        model = AthleteInfo
        fields = ['user_id', 'weight', 'goals']

    def validate_weight(self, value):
        if value is not None and (value <= 0 or value >= 900):
            raise serializers.ValidationError(
                'Вес должен быть больше 0 и меньше 900')
        return value
