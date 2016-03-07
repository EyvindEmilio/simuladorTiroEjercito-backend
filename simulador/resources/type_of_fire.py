from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.position import Position, PositionSerializer
from simulador.resources.target_resource import Target, TargetSerializer


class TypeOfFire(models.Model):
    name = models.CharField(max_length=40, unique=False, blank=False)
    position = models.ForeignKey(Position, null=False)
    distance = models.FloatField(blank=False, null=False)
    selector = models.CharField(max_length=30, blank=True, null=True)
    target = models.ForeignKey(Target, null=False)
    chargers = models.IntegerField(blank=False, null=False)
    cartridges = models.IntegerField(blank=False, null=False)
    modality = models.TextField(max_length=100, blank=True, null=True)
    max_time = models.IntegerField(blank=False, null=False)
    min_score = models.IntegerField(blank=False, null=False)
    max_score = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TypeOfFireSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfFire
        fields = (
            'id', 'name', 'position', 'distance', 'selector', 'target', 'chargers', 'cartridges', 'modality',
            'max_time', 'min_score', 'max_score', 'updated_at')


class TypeOfFireDetailSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)
    target = TargetSerializer(read_only=True)

    class Meta:
        model = TypeOfFire
        fields = (
            'id', 'name', 'position', 'distance', 'selector', 'target', 'chargers', 'cartridges', 'modality',
            'max_time', 'min_score', 'max_score', 'updated_at')


class TypeOfFireViewSet(viewsets.ModelViewSet):
    queryset = TypeOfFire.objects.all()
    serializer_class = TypeOfFireSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name', 'position', 'distance',)
    search_fields = ('$name',)
    # permission_classes = (IsAuthenticated,)
