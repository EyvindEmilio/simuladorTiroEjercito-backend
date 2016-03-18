from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.program_practice import ProgramPractice
from simulador.resources.results import Results


class Practices(models.Model):
    account = models.ForeignKey(Account)
    results = models.ManyToManyField(Results, help_text='''
                                        [
                                            {
                                                "lesson":1
                                                "type_of_fire":1
                                                "position":2,
                                                "score": "5",
                                                "time": 13.12
                                            },
                                            {
                                                "lesson":1
                                                "type_of_fire":2
                                                "position":2,
                                                "score": "5",
                                                "time": 13.12
                                            }
                                        ]
                                    ''')
    date_practice = models.DateTimeField(auto_now_add=True)
    program_practice = models.ForeignKey(ProgramPractice)
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
            'id', 'account', 'results', 'date_practice', 'program_practice', 'created_at',
            'updated_at')


class PracticesViewSet(viewsets.ModelViewSet):
    queryset = Practices.objects.all()
    serializer_class = PracticesSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('$id',)
