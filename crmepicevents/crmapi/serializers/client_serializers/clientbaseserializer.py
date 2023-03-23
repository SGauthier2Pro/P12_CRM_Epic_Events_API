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

    def validate_sales_contact(self, attributes):
        """
        Check if user belongs to Sales Group
        :param attributes:
        :return: attributes if from sales group
        """

        if attributes['sales_contact']:
            sales_contact = User.objects.get(
                pk=attributes['sales_contact'].id
            )
            if sales_contact.groups.all()[0] != 'SALES':
                raise serializers.ValidationError(
                    {"sales contact":
                        "This employee doesn't belong to Sales group"}
                )
            return attributes['sales_contact']

