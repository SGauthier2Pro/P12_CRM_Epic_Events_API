from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime

from crmapi.models.event import Event
from crmapi.models.contract import Contract
from crmapi.serializers.event_serializers.eventlistserializer import \
    EventListSerializer
from crmapi.serializers.event_serializers.eventdetailserializer import \
    EventDetailSerializer

from django_filters.rest_framework import DjangoFilterBackend

from.multipleserializermixin import MultipleSerializerMixin


class EventViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        'id',
        'customer_instance_id',
        'contract_instance_id',
        'date_created',
        'date_updated',
        'support_contact_id',
        'event_date'
    ]
    filter_fields = [
        'event_contract__client__company_name',
        'event_contract__client__email',
        'event_date'
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.all()

        company_name = self.request.GET.get('company_name')
        if company_name:
            queryset = queryset.filter(
                id__in=Contract.objects.filter(
                    client__company_name=company_name)
            )

        client_email = self.request.GET.get('client_email')
        if client_email:
            queryset = queryset.filter(
                id__in=Contract.objects.filter(
                    client__email=client_email)
            )
        event_date_to_test = self.request.GET.get('event_date')
        if event_date_to_test:
            event_date = datetime.datetime.strptime(
                event_date_to_test,
                "%d-%m-%Y")
            queryset = queryset.filter(
                event_date=event_date.strftime("%Y-%m-%d"))
        return queryset

    def create(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == "SALES" or \
                str(self.request.user.groups.all()[0]) == "MANAGER":
            if 'contract_id' in request.data:
                if Contract.objects.filter(pk=request.data['contract_id']):

                    contract = Contract.objects.get(
                        pk=request.data['contract_id']
                    )

                    if contract.status:
                        if self.request.user == contract.client.sales_contact \
                           or \
                           str(self.request.user.groups.all()[0]) == "MANAGER":

                            serializer = self.get_serializer(data=request.data)
                            serializer.is_valid(raise_exception=True)
                            self.perform_create(serializer)

                            headers = self.get_success_headers(serializer.data)
                            return Response(
                                serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers
                            )
                        else:
                            return Response(
                                {'contract_id': "You are not sales "
                                                "contact for this contract !"},
                                status=status.HTTP_403_FORBIDDEN
                            )
                    else:
                        return Response(
                            {'event_contract': "This contract is"
                                               " not signed yet !"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'contract_id': "This contract id does not exists !"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'contract_id': "You must enter a contract id !"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "you are not authorized to do this action"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_create(self, serializer):
        event = serializer.save()

        contract = Contract.objects.get(
            pk=self.request.data['contract_id']
        )

        contract.event = event
        contract.save()

    def update(self, request, *args, **kwargs):
        if self.kwargs['pk'].isdigit():
            if Event.objects.filter(id=self.kwargs['pk']):

                instance = self.get_object()
                contract = Contract.objects.get(event=instance)

                serializer = self.get_serializer(
                    instance,
                    data=request.data,
                    partial=True
                )

                if instance.support_contact == self.request.user \
                    or str(self.request.user.groups.all()[0]) == "MANAGER"\
                        or contract.client.sales_contact == self.request.user:

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
                    {'message': "This event id does not exists"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'message': "This event id is not a valid id"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if self.kwargs['pk'].isdigit():
                if Event.objects.filter(id=self.kwargs['pk']):
                    instance = self.get_object()
                    self.perform_destroy(instance)
                    return Response(
                        {'success': "The event has been deleted"},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'message': "This event id does not exists"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {'message': "This event id is not a valid id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "you are not authorized to do this action"},
                status=status.HTTP_403_FORBIDDEN
            )
