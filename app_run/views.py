from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.models import Run
from app_run.serializers import RunSerializer


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

    queryset = Run.objects.all()
    serializer_class = RunSerializer
