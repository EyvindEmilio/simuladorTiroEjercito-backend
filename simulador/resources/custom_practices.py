import json

from django.db import models
from rest_framework import viewsets, filters, serializers
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountDetailSerializer
from simulador.resources.results import Results, ResultsSerializer, ResultsDetailSerializer
from simulador.resources.results_zone import ResultsZone, ResultsZoneSerializer


class CustomPractices(models.Model):
    practicing = models.ForeignKey(Account)
    results = models.ManyToManyField(Results, help_text='''
                                        [
                                            {
                                                "lesson":1,
                                                "type_of_fire":1,
                                                "position":2,
                                                "results_zone":[
                                                    {
                                                        "zone": 10,
                                                        "time": 3000,
                                                        "score": 10
                                                    },
                                                    {
                                                        "zone": 3,
                                                        "time": 3000,
                                                        "score": 3
                                                    }
                                                ]
                                            },
                                            {
                                                "lesson":1,
                                                "type_of_fire":2,
                                                "position":2,
                                                "results_zone":[
                                                    {
                                                        "zone": 5,
                                                        "time": 3000,
                                                        "score": 10
                                                    },
                                                    {
                                                        "zone": 5,
                                                        "time": 3000,
                                                        "score": 5
                                                    }
                                                ]
                                            }
                                        ]
                                    ''')
    date_practice = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.id

    class Meta:
        ordering = ['created_at']


class CustomPracticesSerializer(serializers.ModelSerializer):
    # results = serializers.CharField(
    #     help_text='''[{"lesson":1,"type_of_fire":1,"position":2,"results_zone":[{"zone": "10","time": 3000,"score": 10},{"zone": "3","time": 3000,"score": 3}]},{"lesson":1,"type_of_fire":2,"position":2,"results_zone":[{"zone": "5","time": 3000,"score": 10},{"zone": "5","time": 3000,"score": 5}]}]''')
    class Meta:
        model = CustomPractices
        fields = (
            'id', 'practicing', 'results', 'date_practice', 'created_at', 'updated_at')


class CustomPracticesDetailSerializer(serializers.ModelSerializer):
    practicing = AccountDetailSerializer(read_only=True)
    results = ResultsDetailSerializer(read_only=True, many=True)

    class Meta:
        model = CustomPractices
        fields = (
            'id', 'practicing', 'results', 'date_practice', 'created_at', 'updated_at')


class CustomPracticesViewSet(viewsets.ModelViewSet):
    queryset = CustomPractices.objects.all()
    serializer_class = CustomPracticesSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'practicing', 'date_practice',)
    search_fields = ('$id', 'practicing', 'date_practice',)

    def get_serializer_class(self):
        query_params = self.request.query_params
        if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
            return CustomPracticesDetailSerializer
        else:
            return CustomPracticesSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        response = {}
        is_complete = False
        if 'results' in data:
            d = json.dumps(data['results'], ensure_ascii=False, encoding='utf8')
            # noinspection PyBroadException
            try:
                results = json.loads(d, encoding='utf-8')
                if type(results) in (tuple, list):
                    list_serialized = []
                    is_all_valid = True
                    last_serialized = ""
                    try:
                        for result in results:
                            # add zones
                            list_result_zone = []
                            list_result_zone_valid = True
                            for result_zone in result['results_zone']:
                                serial_result_zone = ResultsZoneSerializer(data=result_zone)
                                list_result_zone.append(serial_result_zone)
                                if not serial_result_zone.is_valid():
                                    list_result_zone_valid = False
                            if list_result_zone_valid:
                                for result_zone in list_result_zone:
                                    result_zone.save()

                            result["results_zone"] = []
                            [result["results_zone"].append(x.data['id']) for x in list_result_zone]
                            list_id_zones = result["results_zone"]
                            serialized = ResultsSerializer(data=result)
                            if serialized.is_valid():
                                list_serialized.append(serialized)
                            else:
                                last_serialized = serialized
                                is_all_valid = False
                            list_id = []
                            if is_all_valid is True:
                                for serialized in list_serialized:
                                    serialized.save()
                                    list_id.append(serialized.data['id'])
                                is_complete = True
                            else:
                                response = last_serialized.errors
                                for id_result_zone in list_id_zones:
                                    ResultsZone.objects.filter(id=id_result_zone).delete()

                        if is_complete:
                            data_practice = {'results': list_id, 'practicing': request.data['practicing']}
                            practice_serial = CustomPracticesSerializer(data=data_practice)
                            if practice_serial.is_valid():
                                practice_serial.save()
                                response = practice_serial.data
                            else:
                                for id_result in list_id:
                                    Results.objects.filter(id=id_result).delete()
                                response = practice_serial.errors
                        else:
                            for id_result in list_id:
                                Results.objects.filter(id=id_result).delete()

                    except StandardError as err:
                        response = {"results_zone": "El formato Json debe ser array", "fd": repr(err)}
                else:
                    response = {"result": "El formato Json debe ser array"}
            except:
                response = {"result": "Formato Json no valido"}
        return Response(response)
