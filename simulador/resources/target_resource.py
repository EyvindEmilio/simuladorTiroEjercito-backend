from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination


class Target(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False, help_text="fdsf")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    zones = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ('id', 'name', 'description', 'image', 'zones', 'updated_at')


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('$name',)
    # permission_classes = (IsAuthenticated,)
