"""
serializer base class for User model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers


class UserBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        ormat="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    date_updated = serializers.DateTimeField(
        ormat="%d-%m-%Y %H:%M:%S",
        read_only=True
    )

    assigned_customers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='readable_reverse_key'
    )
    assigned_contracts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='readable_reverse_key'
    )
    assigned_events = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='readable_reverse_key'
    )

    def update(self, instance, validated_data):
        if validated_data.get('password') == instance.password:
            password = validated_data.pop('password')
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
