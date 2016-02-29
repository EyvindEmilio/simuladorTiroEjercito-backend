from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.program_lesson import ProgramLesson
from simulador.resources.target_resource import Target


class Practices(models.Model):
    account = models.ForeignKey(Account)
    data_info = models.TextField(max_length=900, help_text='''{
                                        "resultados": [
                                            {
                                                "lesson_id":1
                                                "posicion_id":2,
                                                "puntuacion": "5",
                                                "tiempo": 13.12
                                            },
                                            {
                                                "lesson_id":2
                                                "posicion_id":1,
                                                "puntuacion": "3",
                                                "tiempo": 11.2
                                            }
                                        ]
                                    }''')
    date_practice = models.DateTimeField()
    evaluation = models.BooleanField(default=False)
    program_lesson = models.ForeignKey(ProgramLesson)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.account

    class Meta:
        ordering = ['created_at']


class PracticesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practices
        fields = (
        'id', 'account', 'data_info', 'date_practice', 'evaluation', 'program_lesson', 'created_at', 'updated_at')


class PracticesViewSet(viewsets.ModelViewSet):
    queryset = Practices.objects.all()
    serializer_class = PracticesSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('$id',)
