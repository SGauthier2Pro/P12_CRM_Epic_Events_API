from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crmapi.permissions.issalescontactoradmin import IsSalesContactOrAdmin

from crmapi.models.client import Client

from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer
from crmapi.serializers.client_serializers.clientdetailserializer import \
    ClientDetailSerializer
from crmapi.serializers.client_serializers.clientadminserializer import \
    ClientAdminSerializer


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    permission_classes = [IsAuthenticated, ]

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

    def get_serializer_class(self):
        if self.request.user.is_staff \
                or self.request.user.is_superuser \
                or str(self.request.user.groups.all()[0]) == 'MANAGER':
            return ClientAdminSerializer
        if str(self.request.user.groups.all()[0]) == 'SALES':
            return ClientDetailSerializer
        return ClientListSerializer

    def create(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == "SALES" or \
                str(self.request.user.groups.all()[0]) == "MANAGER":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if str(self.request.user.groups.all()[0]) == "SALES":
                serializer.validated_data['sales_contact'] = self.request.user
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
        if Client.objects.filter(id=self.kwargs['pk']):

            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )

            if (str(self.request.user.groups.all()[0]) == "SALES" and
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
                {'message': "This client id doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if Client.objects.filter(id=self.kwargs['pk']):
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response(
                    {'success': "The client has been deleted"},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': "This client id doesn't exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "You are not authorized to delete a client"},
                status=status.HTTP_403_FORBIDDEN
            )
