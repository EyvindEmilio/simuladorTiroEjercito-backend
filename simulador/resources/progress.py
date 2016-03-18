from django.db import models
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters, serializers, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.target_resource import Target


class Progress(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        ordering = ['id']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'name', 'description', 'image', 'updated_at')


# @require_http_methods(["GET"])
class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('$name',)
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'render.html'

    # http_method_names = ('get',)

    @detail_route(methods=['post'])
    def set_pass(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @list_route()
    def recent_users(self, request):
        return Response("Emilio")
