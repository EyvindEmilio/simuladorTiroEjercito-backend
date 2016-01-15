from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination


class Regiment(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RegimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiment
        fields = ('id', 'name', 'description', 'image', 'created_at', 'updated_at')


class RegimentViewSet(viewsets.ModelViewSet):
    queryset = Regiment.objects.all()
    serializer_class = RegimentSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('$name',)
    # permission_classes = (IsAuthenticated,)
