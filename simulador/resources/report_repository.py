from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.image_repository import ImageRepository


class ReportRepository(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=40, unique=True, blank=False)
    file = models.FileField(upload_to="ReportRepository/")
    images = models.ManyToManyField(ImageRepository)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ReportRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRepository
        fields = ('id', 'account', 'name', 'file', 'images')


class CityViewSet(viewsets.ModelViewSet):
    queryset = ReportRepository.objects.all()
    serializer_class = ReportRepositorySerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'name')
    search_fields = ('$name',)
