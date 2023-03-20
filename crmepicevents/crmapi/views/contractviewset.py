from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models.contract import Contract
from ..models.client import Client
from ..permissions.issalescontactoradmin import IsSalesContactOrAdmin
from crmapi.serializers.contract_serializers.contractlistserializer import \
    ContractListSerializer
from crmapi.serializers.contract_serializers.contractdetailserializer import \
    ContractDetailSerializer


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
    permission_classes = [IsAuthenticated, IsSalesContactOrAdmin]

    def get_serializer_class(self):
        if self.request.user.is_staff \
                or self.request.user.is_superuser \
                or str(self.request.user.groups.all()[0]) == 'MANAGER':
            return ContractDetailSerializer
        if str(self.request.user.groups.all()[0]) == 'SALES':
            return ContractDetailSerializer
        return ContractListSerializer

    def create(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == "SALES" or \
                str(self.request.user.groups.all()[0]) == "MANAGER":

            client = Client.objects.get(
                pk=request.data['client']
            )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if client.sales_contact == self.request.user or \
                    str(self.request.user.groups.all()[0]) == "MANAGER":
                serializer.validated_data['client'] = client
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
            else:
                return Response(
                    {'message': "you are not sales contact for this client !"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'message': "you are not authorized to do this action"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if Contract.objects.filter(id=self.kwargs['pk']):
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )
            sales_contact = instance.client.sales_contact
            if (str(self.request.user.groups.all()[0]) == "SALES"
                and sales_contact == self.request.user) \
                    or str(self.request.user.groups.all()[0]) == "MANAGER":
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                headers = self.get_success_headers(
                    serializer.validated_data
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    headers=headers
                )
            else:
                return Response({'message': "you are not authorized "
                                            "to do this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(
                {'message': "This contract id doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if Contract.objects.filter(id=self.kwargs['pk']):
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response(
                    {'success': "The contract has been deleted"},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': "This contract id doesn't exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({'message': "you are not authorized "
                                        "to do this action"},
                            status=status.HTTP_403_FORBIDDEN)