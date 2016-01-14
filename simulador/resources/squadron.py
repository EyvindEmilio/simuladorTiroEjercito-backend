from django.db import models
from rest_framework import viewsets, views, serializers
from simulador.pagination import BasePagination
from simulador.resources.battalion import Battalion
from simulador.resources.company import Company
from simulador.resources.regiment import Regiment


class Squadron(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SquadronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squadron
        fields = ('id', 'name', 'company', 'created_at', 'updated_at')


class SquadronViewSet(viewsets.ModelViewSet):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer
    pagination_class = BasePagination
    # permission_classes = (IsAuthenticated,)
