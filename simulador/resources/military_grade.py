from django.db import models
from rest_framework import viewsets, views, serializers
from simulador.pagination import BasePagination


class MilitaryGrade(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    short = models.CharField(max_length=10, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MilitaryGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryGrade
        fields = ('id', 'name', 'short', 'created_at', 'updated_at')


class MilitaryGradeViewSet(viewsets.ModelViewSet):
    queryset = MilitaryGrade.objects.all()
    serializer_class = MilitaryGradeSerializer
    pagination_class = BasePagination
    # permission_classes = (IsAuthenticated,)
