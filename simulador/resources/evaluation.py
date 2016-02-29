from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.program_lesson import ProgramLesson
from simulador.resources.target_resource import Target


class Evaluation(models.Model):
    account = models.ForeignKey(Account)
    data_info = models.TextField(max_length=900, help_text='''{
	"leccion_id": 2,
	"evaluacion": true,
	"resultados": [
		{
			"posicion_id":2,
			"puntuacion": "5v",
			"tiempo": 13.12
		},
		{
			"posicion_id":1,
			"puntuacion": "3",
			"tiempo": 11.2
		}
	]
}''')
    date_practice = models.DateTimeField()
    program_lesson = models.ForeignKey(ProgramLesson)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.account

    class Meta:
        ordering = ['created_at']


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'account', 'data_info', 'date_practice', 'program_lesson', 'created_at', 'updated_at')


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('$id',)
