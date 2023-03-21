from datetime import datetime

from rest_framework import serializers

from django.contrib.auth.models import User


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
        format="%d-%m-%Y"
    )

    def validate_support_contact(self, value):

        if value:
            user_instance = User.objects.get(pk=value.id)
            if user_instance.groups != "SUPPORT":
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
