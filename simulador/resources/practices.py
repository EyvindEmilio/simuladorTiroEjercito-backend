import json

from django.contrib.sites import requests
from django.db import models
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountSerializer, AccountDetailSerializer
from simulador.resources.program_practice import ProgramPractice, ProgramPracticeSerializer, \
    ProgramPracticeDetailSerializer
from simulador.resources.results import Results, ResultsSerializer, ResultsDetailSerializer
from simuladorTiroEjercitoBackend import settings


class Practices(models.Model):
    practicing = models.ForeignKey(Account)
    results = models.ManyToManyField(Results, help_text='''
                                        [
                                            {
                                                "lesson":1,
                                                "type_of_fire":1,
                                                "position":2,
                                                "results_zone":[
                                                    {
                                                        "zone": "10",
                                                        "time": 3000,
                                                        "score": 10
                                                    },
                                                    {
                                                        "zone": "3",
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
                                                        "zone": "5",
                                                        "time": 3000,
                                                        "score": 10
                                                    },
                                                    {
                                                        "zone": "5",
                                                        "time": 3000,
                                                        "score": 5
                                                    }
                                                ]
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
    results = serializers.CharField(
        help_text='''[{"lesson":1,"type_of_fire":1,"position":2,"results_zone":[{"zone": "10","time": 3000,"score": 10},{"zone": "3","time": 3000,"score": 3}]},{"lesson":1,"type_of_fire":2,"position":2,"results_zone":[{"zone": "5","time": 3000,"score": 10},{"zone": "5","time": 3000,"score": 5}]}]''')

    class Meta:
        model = Practices
        fields = (
            'id', 'practicing', 'results', 'date_practice', 'program_practice', 'created_at',
            'updated_at')


class PracticesDetailSerializer(serializers.ModelSerializer):
    account = AccountDetailSerializer(read_only=True)
    program_practice = ProgramPracticeDetailSerializer(read_only=True)

    class Meta:
        model = Practices
        fields = (
            'id', 'practicing', 'results', 'date_practice', 'program_practice', 'created_at',
            'updated_at')


def serializer_result(_list, query_params):
    for result in _list:
        result['results'] = result['results'].replace('[', '')
        result['results'] = result['results'].replace(']', '')
        list_id = result['results'].split(",")
        serial = []
        for id_result in list_id:
            objects = Results.objects.filter(id=int(id_result))
            if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
                data_serial = ResultsDetailSerializer(objects, many=True)
            else:
                data_serial = ResultsSerializer(objects, many=True)
            serial.append(data_serial.data[0])
        result['results'] = serial
    return _list


class PracticesViewSet(viewsets.ModelViewSet):
    queryset = Practices.objects.all()
    serializer_class = PracticesSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'practicing', 'date_practice', 'program_practice',)
    search_fields = ('$id', 'practicing', 'date_practice', 'program_practice',)

    @list_route()
    def list_results(self, request):

        return Response("Emilio")

    @detail_route(methods=['get'])
    def progress(self, request, pk=None):
        query_params = {'is_complete_serializer': '1'}
        list_practices = Practices.objects.filter(id=pk)
        serial_data = PracticesDetailSerializer(list_practices, many=True)
        serializer_result(serial_data.data, query_params)
        info_practice = serial_data.data[0]

        progreso = {"id:": info_practice['id']}
        progreso['account'] = {'id': info_practice['account']['id']}
        progreso['account']['first_name'] = info_practice['account']['first_name']
        progreso['account']['last_name'] = info_practice['account']['last_name']
        progreso['account']['ci'] = info_practice['account']['ci']
        progreso['account']['phone_number'] = info_practice['account']['phone_number']
        progreso['account']['email'] = info_practice['account']['email']
        progreso['account']['user_type'] = {'id': info_practice['account']['user_type']['id']}
        progreso['account']['user_type']['name'] = info_practice['account']['user_type']['name']
        progreso['account']['city'] = {'id': info_practice['account']['city']['id']}
        progreso['account']['city']['short'] = info_practice['account']['city']['short']
        progreso['account']['military_grade'] = {'id': info_practice['account']['military_grade']['id']}
        progreso['account']['military_grade']['short'] = info_practice['account']['military_grade']['short']
        progreso['account']['image'] = settings.GET_API_URL(request, info_practice['account']['image'])
        progreso['date_practice'] = info_practice['date_practice']
        progreso['program_practice'] = {'id': info_practice['program_practice']['id']}
        progreso['program_practice']['name'] = info_practice['program_practice']['title']
        progreso['program_practice']['is_evaluation'] = info_practice['program_practice']['is_evaluation']

        # global score
        results_global_time = 0
        results_global_score = 0
        for result in info_practice['results']:
            results_global_score += result['score']
            results_global_time += result['time']
        progreso['results_global'] = {'time': results_global_time, 'score': results_global_score}
        # score per lesson
        results_global_time = 0
        results_global_score = 0
        for result in info_practice['results']:
            results_global_score += result['score']
            results_global_time += result['time']
        progreso['results_global'] = {'time': results_global_time, 'score': results_global_score}
        # for result in info_practice['results']:
        #     temp_result = {'id': result['id']}
        #     temp_result['score'] = result['score']
        #     temp_result['time'] = result['time']
        #     progreso['results_global'].append(temp_result)
        return Response(progreso)  # Response("Emilio")

    # def retrieve(self, request, pk=None):
    #     query_params = self.request.query_params
    #     data = super(PracticesViewSet, self).retrieve(self, request, pk)
    #     serializer_result([data.data], query_params)
    #     return Response(data.data)
    #
    # def list(self, request, *args, **kwargs):
    #     query_params = self.request.query_params
    #     data = super(PracticesViewSet, self).list(self, request)
    #     data.data['results'] = serializer_result(data.data['results'], query_params)
    #     return Response(data.data)
    #
    def create(self, request, *args, **kwargs):
        # return super(PracticesViewSet, self).create(request, *args, **kwargs)
        data = self.request.data
        response = ""
        is_complete = False
        if 'results' in data:
            try:
                results = json.loads(data['results'])
                if type(results) in (tuple, list):
                    list_serialized = []
                    is_all_valid = True
                    last_serialized = ""
                    try:
                        for result in results:
                            result_zone = json.loads(result["results_zone"])
                            # result_zone =
                            # result["result_zone"] = "2, 4"
                            # serialized = ResultsSerializer(data=result)
                            # if serialized.is_valid():
                            #     list_serialized.append(serialized)
                            # else:
                            #     last_serialized = serialized
                            #     is_all_valid = False

                            # if is_all_valid is True:
                            #     list_id = []
                            #     for serialized in list_serialized:
                            #         serialized.save()
                            #         list_id.append(serialized.data['id'])
                            #     request.data['results'] = list_id
                            #     is_complete = True
                            # else:
                            #     response = last_serialized.errors
                    except StandardError as err:
                        response = {"results_zone": "El formato Json debe ser array", "fd": repr(err)}
                else:
                    response = {"result": "El formato Json debe ser array"}
            except:
                response = {"result": "Formato Json no valido"}
        if is_complete:
            return super(PracticesViewSet, self).create(request, *args, **kwargs)
        else:
            return Response(response)
