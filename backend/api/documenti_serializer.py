from rest_framework import serializers

from home.models import Documenti


class Documentiserializer(serializers.ModelSerializer):

    class Meta:
        model = Documenti

        fields = '__all__'
