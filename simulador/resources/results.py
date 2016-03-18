from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.lesson import Lesson
from simulador.resources.position import Position
from simulador.resources.type_of_fire import TypeOfFire


class Results(models.Model):
    lesson = models.ForeignKey(Lesson)
    type_of_fire = models.ForeignKey(TypeOfFire)
    position = models.ForeignKey(Position)
    score = models.IntegerField()
    time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Id: %s, Score: %s, Time: %s" % (self.id, self.score, self.time,)

    class Meta:
        ordering = ['id']


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ('id', 'lesson', 'type_of_fire', 'position', 'time', 'score')


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('type_of_fire', 'time', 'score')
    search_fields = ('$type_of_fire',)
    # permission_classes = (IsAuthenticated,)
