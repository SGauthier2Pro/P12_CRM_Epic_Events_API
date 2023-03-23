from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.contrib.auth.models import User


from crmapi.models.contract import Contract
from crmapi.serializers.contract_serializers.contractlistserializer import \
    ContractListSerializer

from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer
from crmapi.models.client import Client


class EventBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    event_date = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=['%d-%m-%Y', 'iso-8601']
    )

    #misc fields

    event_client = SerializerMethodField()
    contract_id = SerializerMethodField()

    def get_event_client(self, instance):
        contract = Contract.objects.get(event=instance)
        queryset = Client.objects.filter(pk=contract.client.id)
        serializer = ClientListSerializer(queryset, many=True)
        return serializer.data

    def get_contract_id(self, instance):
        queryset = Contract.objects.get(event=instance)
        serializer = ContractListSerializer(queryset, many=True)
        return serializer.data

    def validate_support_contact(self, value):
        """
        Check if user belongs to Support Group
        :param value:
        :return: attributes if from support group
        """

        if value:
            user_instance = User.objects.get(pk=value.id)
            if str(user_instance.groups.all()[0]) != "SUPPORT":
                raise serializers.ValidationError(
                    "support_contact: This user doesn't "
                    "belong to SUPPORT Team.")
            return value

    def validate_event_date(self, value):

        date_now = datetime.now().strftime("%d-%m-%Y")

        # Update
        if self.instance and value:
            if value.strftime("%d-%m-%Y") == '01-01-1900':
                return self.instance.payment_due

            if value.strftime("%d-%m-%Y") != '01-01-1900' and value.strftime(
                    "%d-%m-%Y") < date_now:
                raise serializers.ValidationError(
                    "payment_due : You can not choose an older date than now.")
        # create
        elif not self.instance and value:
            if value.strftime("%d-%m-%Y") == '01-01-1900':
                return None

            if value.strftime("%d-%m-%Y") != '01-01-1900' and value.strftime(
                    "%d-%m-%Y") < date_now:
                raise serializers.ValidationError(
                    "payment_due : You can not choose an older date than now.")
        return value
