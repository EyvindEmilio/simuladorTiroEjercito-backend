from django.db import models
from rest_framework import viewsets, filters, serializers


# from simulador.models import City
from simulador.pagination import BasePagination


class City(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    short = models.CharField(max_length=10, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

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
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'name', 'short')
    search_fields = ('$name',)
    # permission_classes = (IsAuthenticated,)
