from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination


class ResultsZone(models.Model):
    zone = models.IntegerField()
    time = models.IntegerField()
    score = models.IntegerField()

    def __unicode__(self):
        return "Zone: %s, time: %s, score: %s" % (self.zone, self.time, self.score,)

    class Meta:
        ordering = ['id']


class ResultsZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultsZone
        fields = ('id', 'zone', 'score', 'time',)


class ResultsZoneViewSet(viewsets.ModelViewSet):
    queryset = ResultsZone.objects.all()
    serializer_class = ResultsZoneSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('zone', 'time', 'score',)
    search_fields = ('$zone', '$time', '$score',)
