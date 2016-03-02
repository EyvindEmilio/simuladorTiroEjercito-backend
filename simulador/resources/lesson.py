from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.target_resource import Target, TargetSerializer
from simulador.resources.type_of_fire import TypeOfFire, TypeOfFireSerializer, TypeOfFireDetailSerializer


class Lesson(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    type_of_fire = models.ManyToManyField(TypeOfFire, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'image', 'type_of_fire', 'created_at', 'updated_at')


class LessonDetailSerializer(serializers.ModelSerializer):
    type_of_fire = TypeOfFireDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = (
            'id', 'name', 'description', 'image', 'type_of_fire', 'created_at', 'updated_at')


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('$name',)
