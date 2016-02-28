from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination


class UserType(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    short = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'name', 'short', 'description', 'created_at', 'updated_at')


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name', 'short',)
    search_fields = ('$name', '$short',)
    # permission_classes = (IsAuthenticated,)
