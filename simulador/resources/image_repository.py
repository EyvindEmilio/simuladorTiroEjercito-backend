import base64

from django.db import models
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, filters, serializers, status
from rest_framework.response import Response
from simulador.pagination import BasePagination


class ImageRepository(models.Model):
    name = models.CharField(max_length=30, null=False, blank=True)
    image = models.ImageField(upload_to="ImageRepository/")

    def __unicode__(self):
        return "%s" % self.id

    class Meta:
        ordering = ['id']


class ImageRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRepository
        fields = ('id', 'name', 'image')


class ImageRepositoryViewSet(viewsets.ModelViewSet):
    queryset = ImageRepository.objects.all()
    serializer_class = ImageRepositorySerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'image')
    search_fields = ('$id',)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        serial = {'image': 'campo no puede estar vacio'}
        status_ = status.HTTP_400_BAD_REQUEST
        if 'image' in data:
            name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            image_decode = base64.decodestring(data['image'])
            fh = open(("media/ImageRepository/%s.png" % name), "wb")
            fh.write(image_decode)
            fh.close()
            instance = ImageRepository.objects.create()
            instance.name = name
            instance.image = "./ImageRepository/%s.png" % name
            instance.save()
            serial = ImageRepositorySerializer(instance).data
            status_ = status.HTTP_201_CREATED
        return Response(serial, status_)
