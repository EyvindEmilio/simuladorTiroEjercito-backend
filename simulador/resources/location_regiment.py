from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.battalion import Battalion
from simulador.resources.company import Company
from simulador.resources.regiment import Regiment
from simulador.resources.squadron import Squadron
from simulador.resources.target_resource import Target


class LocationRegiment(models.Model):
    regiment = models.ForeignKey(Regiment)
    battalion = models.ForeignKey(Battalion)
    company = models.ForeignKey(Company)
    squadron = models.ForeignKey(Squadron)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LocationRegimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationRegiment
        fields = ('id', 'regiment', 'battalion', 'company', 'squadron', 'created_at', 'updated_at')


class LessonViewSet(viewsets.ModelViewSet):
    queryset = LocationRegiment.objects.all()
    serializer_class = LocationRegimentSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('$id',)
