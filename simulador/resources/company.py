from django.db import models
from rest_framework import viewsets, views, serializers
from simulador.pagination import BasePagination
from simulador.resources.battalion import Battalion
from simulador.resources.regiment import Regiment


class Company(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    battalion = models.ForeignKey(Battalion)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'battalion', 'description', 'image', 'created_at', 'updated_at')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = BasePagination
    # permission_classes = (IsAuthenticated,)
