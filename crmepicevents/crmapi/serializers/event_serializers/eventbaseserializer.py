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
            if user_instance.group != "SUPPORT":
                raise serializers.ValidationError(
                    "support_contact: Pour être affecté à ce client, "
                    "ce professionnel doit être du groupe 'SUPPORT'.")
            return value

    def validate_event_date(self, value):

        date_now = datetime.now().strftime("%Y-%m-%d")

        # Update
        if self.instance and value:
            if value.strftime("%Y-%m-%d") == '1900-01-01':
                return self.instance.event_date

            if value.strftime("%Y-%m-%d") != '1900-01-01' and value.strftime(
                    "%Y-%m-%d") < date_now:
                raise serializers.ValidationError(
                    "event_date : Une date antérieure à celle du jour "
                    "actuel ne peut être selectionnée.")
        # create
        elif not self.instance and value:
            if value.strftime("%Y-%m-%d") == '1900-01-01':
                return None

            if value.strftime("%Y-%m-%d") != '1900-01-01' and value.strftime(
                    "%Y-%m-%d") < date_now:
                raise serializers.ValidationError(
                    "event_date : Une date antérieure à celle du "
                    "jour actuel ne peut être selectionnée.")
        return value
