from rest_framework import serializers
from django.contrib.auth.models import User


class ClientBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)

    # misc informations

    contracts = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id",
        many=True
    )

    def validate_sales_contact(self, value):
        """
        Check if user belongs to Sales Group
        :param value:
        :return: attributes if from sales group
        """

        print(value)
        if value:

            sales_contact = User.objects.get(pk=value.id)
            if str(sales_contact.groups.all()[0]) != 'SALES':
                raise serializers.ValidationError(
                    {'sales_contact':
                        "This employee does not belong to Sales group"}
                )
            return value

