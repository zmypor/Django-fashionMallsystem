from rest_framework import serializers

from django.contrib.flatpages.models import FlatPage


class FlatPageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FlatPage
        exclude = ('template_name',)
