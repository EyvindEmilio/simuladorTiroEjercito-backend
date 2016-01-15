from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.battalion import Battalion
from simulador.resources.company import Company
from simulador.resources.regiment import Regiment


class Squadron(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    company = models.ForeignKey(Company)
    list = models.ManyToManyField(Account)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SquadronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squadron
        fields = ('id', 'name', 'company', 'list', 'created_at', 'updated_at')


class SquadronViewSet(viewsets.ModelViewSet):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('$name',)
    # permission_classes = (IsAuthenticated,)
