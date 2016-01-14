from django.db import models
from rest_framework import viewsets, views, serializers
from simulador.pagination import BasePagination
from simulador.resources.regiment import Regiment


class Battalion(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    regiment = models.ForeignKey(Regiment)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BattalionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battalion
        fields = ('id', 'name', 'regiment', 'description', 'image', 'created_at', 'updated_at')


class BattalionViewSet(viewsets.ModelViewSet):
    queryset = Battalion.objects.all()
    serializer_class = BattalionSerializer
    pagination_class = BasePagination
    # permission_classes = (IsAuthenticated,)
