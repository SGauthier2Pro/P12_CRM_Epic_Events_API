from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import datetime

from crmapi.models.contract import Contract
from crmapi.models.client import Client

from crmapi.serializers.contract_serializers.contractlistserializer import \
    ContractListSerializer
from crmapi.serializers.contract_serializers.contractdetailserializer import \
    ContractDetailSerializer

from crmapi.views.multipleserializermixin import MultipleSerializerMixin


class ContractViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        'id',
        'client',
        'amount',
        'date_created',
        'date_updated',
        'payment_due'
    ]
    filter_fields = [
        'client__company_name',
        'client__email',
        'amount',
        'date_created'
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.all()
        company_name = self.request.GET.get('company_name')
        if company_name:
            queryset = queryset.filter(client__company_name=company_name)
        client_email = self.request.GET.get('client_email')
        if client_email:
            queryset = queryset.filter(client__email=client_email)
        amount = self.request.GET.get('amount')
        if amount:
            queryset = queryset.filter(amount=amount)
        date_created_to_test = self.request.GET.get('date_created')
        if date_created_to_test:
            date_created = datetime.datetime.strptime(
                date_created_to_test,
                "%d-%m-%Y")
            queryset = queryset.filter(
                date_created__contains=date_created.strftime("%Y-%m-%d"))
        return queryset

    def create(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == "SALES" or \
                str(self.request.user.groups.all()[0]) == "MANAGER":
            if 'client' in request.data:
                if Client.objects.filter(pk=request.data['client']):
                    client = Client.objects.get(
                        pk=request.data['client']
                    )
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    if client.sales_contact == self.request.user or str(
                            self.request.user.groups.all()[0]) == "MANAGER":
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
                            {'message': "you are not sales "
                                        "contact for this client !"},
                            status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    return Response(
                        {'client': "This client id does not exists !"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'client': "This field is needed !"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "you are not authorized to do this action"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if self.kwargs['pk'].isdigit():
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
                    {'message': "This contract id does not exists"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'message': "This contract id is not a valid id"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if self.kwargs['pk'].isdigit():
                if Contract.objects.filter(id=self.kwargs['pk']):
                    instance = self.get_object()
                    self.perform_destroy(instance)
                    return Response(
                        {'success': "The contract has been deleted"},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'message': "This contract id does not exists"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {'message': "This contract id is not a valid id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({'message': "you are not authorized "
                                        "to do this action"},
                            status=status.HTTP_403_FORBIDDEN)
