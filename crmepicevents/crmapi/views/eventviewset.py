from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crmapi.models.event import Event
from crmapi.permissions.issupportcontactoradmin import IsSupportContactOrAdmin
from crmapi.serializers.event_serializers.eventlistserializer import \
    EventListSerializer
from crmapi.serializers.event_serializers.eventdetailserializer import \
    EventDetailSerializer
from crmapi.serializers.event_serializers.eventadminserializer import \
    EventAdminSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = [
        'id',
        'customer_instance_id',
        'contract_instance_id',
        'date_created',
        'date_updated',
        'support_contact_id',
        'event_date'
    ]
    search_fields = [
        'id',
        'event_status'
    ]
    permission_classes = [IsAuthenticated, IsSupportContactOrAdmin]

    def get_serializer_class(self):
        if self.request.user.is_staff \
                or self.request.user.is_superuser \
                or str(self.request.user.groups.all()[0]) == 'MANAGER':
            return EventAdminSerializer
        if str(self.request.user.groups.all()[0]) == 'SUPPORT':
            return EventDetailSerializer
        return EventListSerializer

    def create(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == "SALES" or \
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
                {'message': "you are not authorized to do this action"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if Event.objects.filter(id=self.kwargs['pk']):

            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )

            if (str(self.request.user.groups.all()[0]) == "SUPPORT" and
                instance.sales_contact == self.request.user) \
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
                {'message': "This event id doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if Event.objects.filter(id=self.kwargs['pk']):
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response(
                    {'success': "The event has been deleted"},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': "This event id doesn't exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "You are not authorized to delete a event"},
                status=status.HTTP_403_FORBIDDEN
            )
