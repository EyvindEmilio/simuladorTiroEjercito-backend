
from django.db import models
from rest_framework import viewsets, views, serializers
# from simulador.models import City


class City(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    short = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'short')


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    # permission_classes = (IsAuthenticated,)