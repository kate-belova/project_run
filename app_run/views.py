from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

    queryset = Run.objects.all()
    serializer_class = RunSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API для работы с User'ами"""

    queryset = User.objects.filter(is_superuser=False).order_by('id')
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        type_param = (self.request.query_params.get('type', '')
                      .lower().strip())

        type_mapping = {
            'coach': qs.filter(is_staff=True),
            'athlete': qs.filter(is_staff=False)
        }

        return type_mapping.get(type_param, qs)
