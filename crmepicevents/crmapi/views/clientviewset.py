from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from crmapi.models.client import Client
from crmapi.permissions.isadminuser import IsAdminUser
from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer
from crmapi.serializers.client_serializers.clientdetailserializer import \
    ClientDetailSerializer


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = [
        'id',
        'date_joined',
        'last_login',
        'sales_contact'
    ]
    search_fields = [
        'id',
        'first_name',
        'last_name',
        'email',
        'company_name'
    ]
    permission_classes = IsAuthenticated, IsAdminUser  # add IsSalesContactOrAdmin

    def get_serializer_class(self):
        if self.request.user.is_staff \
                or self.request.user.is_superuser \
                or (self.request.user.groups.all())[0] == 'MANAGER':
            return ClientDetailSerializer
        if self.action == 'list':
            return ClientListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return ClientDetailSerializer
        return ClientListSerializer
