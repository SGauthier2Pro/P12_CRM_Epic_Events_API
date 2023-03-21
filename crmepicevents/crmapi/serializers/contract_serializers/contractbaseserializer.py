from datetime import datetime

from rest_framework import serializers

from django.contrib.auth.models import User


class ContractBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    payment_due = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=['%d-%m-%Y', 'iso-8601']
    )

    def validate_payment_due(self, value):

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
