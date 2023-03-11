from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.serializers.userlistserializer \
    import UserListSerializer
from authentication.serializers.userdetailserializer \
    import UserDetailSerializer
from authentication.serializers.useradminserializer \
    import UserAdminSerializer
from authentication.permissions.isadminorowner \
    import IsAdminOrOwner


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    searching_fields = [
        'id',
        'first_name',
        'last_name',
        'email',
        'group'
    ]
    fields_to_order = [
        'id',
        'username',
        'date_created',
        'date_updates',
        'is_superuser'
    ]

    def get_serializer_class(self):
        if self.request.user.is_superuser \
                or (self.request.user.groups.all())[0] == 'MANAGER':
            return UserAdminSerializer
        try:
            pk = int(self.kwargs['pk'])
            if pk == self.request.user.id:
                return self.detail_serializer_class
        except KeyError:
            return self.serializer_class

    def perform_create(self, serializer):
        if self.request.user.groups == 'MANAGER':
            if 'password' in self.request.data:
                password = make_password(self.request.data['password'])
                user = serializer.save(password=password)
            else:
                user = serializer.save()

            if 'groups' in self.request.data:
                try:
                    group = Group.objects.get(name=(self.request.data['groups']))
                    if group.name == 'MANAGER':
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                    else:
                        user.is_staff = False
                        user.is_superuser = False
                        user.save()
                    group.user_set.add(user)
                except ValueError:
                    return Response(
                        {'Groups': "The group you enter is not a valid one !"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response({'message': "you are not authorized "
                                        "to do this action"},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_superuser \
                or self.request.user.id == self.kwargs['pk']:

            if User.objects.filter(id=self.kwargs['pk']):
                instance = self.get_object()

                serializer = self.get_serializer(
                    instance,
                    data=request.data,
                    partial=True
                )
                print(type(serializer))
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
                return Response(
                    {'message': "This user id doesn't exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({'message': "you are not authorized "
                                        "to do this action"},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):

        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            user = serializer.save(password=password)
        else:
            user = serializer.save()
        if 'groups' in self.request.data:
            try:
                user.groups.clear()
                group = Group.objects.get(name=(self.request.data['groups']))
                if group.name == 'MANAGER':
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                else:
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                group.user_set.add(user)
            except ValueError:
                return Response(
                    {'Groups': "The group you enter is not a valid one !"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def destroy(self, request, *args, **kwargs):
        if self.request.user.groups == 'MANAGER' \
           or self.request.user.is_superuser:

            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'success': "The user has been deleted"},
                status=status.HTTP_200_OK)
        else:
            return Response({'message': "You are not authorized "
                                        "to delete a user"},
                            status=status.HTTP_403_FORBIDDEN)
