from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models.contract import Contract
# from ..permissions.issalescontactoradmin import IsSalesContactOrAdmin
from crmapi.serializers.contract_serializers.contractlistserializer import ContractListSerializer
from crmapi.serializers.contract_serializers.contractdetailserializer import ContractDetailSerializer


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = [
        'id',
        'sales_contact',
        'client',
        'amount',
        'date_created',
        'date_updated',
        'payment_due'
    ]
    search_fields = [
        'id',
        'status'
    ]
    permission_classes = (IsAuthenticated,)  # add IsSalesContactOrAdmin

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return ContractDetailSerializer
        return ContractListSerializer
