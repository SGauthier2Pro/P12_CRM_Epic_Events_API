from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crmapi.models.client import Client

from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer
from crmapi.serializers.client_serializers.clientdetailserializer import \
    ClientDetailSerializer

from crmapi.views.multipleserializermixin import MultipleSerializerMixin


class ClientViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = [
        'id',
        'date_joined',
        'last_login',
        'sales_contact'
    ]
    search_fields = [
        'email',
        'company_name'
    ]

    def get_queryset(self):
        queryset = Client.objects.all()
        company_name = self.request.GET.get('company_name')
        email = self.request.GET.get('email')
        if company_name:
            queryset = queryset.filter(company_name=company_name)
        if email:
            queryset = queryset.filter(email=email)
        return queryset

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
        if self.kwargs['pk'].isdigit():
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
                    {'message': "This client id does not exists"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'message': "This client id is not a valid id"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if str(self.request.user.groups.all()[0]) == 'MANAGER':
            if self.kwargs['pk'].isdigit():
                if Client.objects.filter(id=self.kwargs['pk']):
                    instance = self.get_object()
                    self.perform_destroy(instance)
                    return Response(
                        {'success': "The client has been deleted"},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'message': "This client id does not exists"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {'message': "This client id is not a valid id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': "You are not authorized to delete a client"},
                status=status.HTTP_403_FORBIDDEN
            )
