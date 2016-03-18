from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.lesson import Lesson, LessonDetailSerializer
from simulador.resources.position import Position, PositionSerializer
from simulador.resources.results_zone import ResultsZone, ResultsZoneSerializer
from simulador.resources.type_of_fire import TypeOfFire, TypeOfFireDetailSerializer


class Results(models.Model):
    lesson = models.ForeignKey(Lesson)
    type_of_fire = models.ForeignKey(TypeOfFire)
    position = models.ForeignKey(Position)
    results_zone = models.ManyToManyField(ResultsZone)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.id

    class Meta:
        ordering = ['id']


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ('id', 'lesson', 'type_of_fire', 'position', 'results_zone',)


class ResultsDetailSerializer(serializers.ModelSerializer):
    lesson = LessonDetailSerializer(read_only=True)
    type_of_fire = TypeOfFireDetailSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    result_zone = ResultsZoneSerializer(read_only=True)

    class Meta:
        model = Results
        fields = ('id', 'lesson', 'type_of_fire', 'position', 'results_zone',)


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('type_of_fire', 'results_zone',)
    search_fields = ('$type_of_fire',)

    def get_serializer_class(self):
        query_params = self.request.query_params
        if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
            return ResultsDetailSerializer
        else:
            return ResultsSerializer
            # permission_classes = (IsAuthenticated,)
