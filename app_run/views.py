from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.models import Run
from app_run.serializers import RunSerializer, UserSerializer


@api_view(['GET'])
def company_details(request):
    """API endpoint для получения информации о компании"""
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.COMPANY_SLOGAN,
        'contacts': settings.COMPANY_CONTACTS,
    }

    return Response(details)


class RunViewSet(viewsets.ModelViewSet):
    """API для работы с пробежками"""

    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

class RunStartView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'init':
            message = {'error': 'Забег уже стартовал или завершен.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        run.status = 'in_progress'
        run.save()
        return Response(RunSerializer(run).data, status=status.HTTP_200_OK)


class RunStopView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)

        if run.status != 'in_progress':
            message = {'error': 'Забег нельзя завершить - '
                                'он еще не начат или уже завершен.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        run.status = 'finished'
        run.save()
        return Response(RunSerializer(run).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API для работы с User'ами"""

    queryset = User.objects.filter(is_superuser=False).order_by('id')
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset
        type_param = (self.request.query_params.get('type', '')
                      .lower().strip())

        type_mapping = {
            'coach': qs.filter(is_staff=True),
            'athlete': qs.filter(is_staff=False)
        }

        return type_mapping.get(type_param, qs)
