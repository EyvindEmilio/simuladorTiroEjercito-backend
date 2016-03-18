import json
from django.db import models
from rest_framework import viewsets, filters, serializers
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.account import Account
from simulador.resources.program_practice import ProgramPractice
from simulador.resources.results import Results, ResultsSerializer, ResultsDetailSerializer


class Practices(models.Model):
    account = models.ForeignKey(Account)
    results = models.TextField(max_length=300, help_text='''
                                        [
                                            {
                                                "lesson":1,
                                                "type_of_fire":1,
                                                "position":2,
                                                "score": "5",
                                                "time": 13.12
                                            },
                                            {
                                                "lesson":1,
                                                "type_of_fire":2,
                                                "position":2,
                                                "score": "5",
                                                "time": 13.12
                                            }
                                        ]
                                    ''')
    # results = models.ManyToManyField(Results, help_text='''
    #                                     [
    #                                         {
    #                                             "lesson":1
    #                                             "type_of_fire":1
    #                                             "position":2,
    #                                             "score": "5",
    #                                             "time": 13.12
    #                                         },
    #                                         {
    #                                             "lesson":1
    #                                             "type_of_fire":2
    #                                             "position":2,
    #                                             "score": "5",
    #                                             "time": 13.12
    #                                         }
    #                                     ]
    #                                 ''')
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
    filter_fields = ('id', 'account', 'date_practice', 'program_practice',)
    search_fields = ('$id', 'account', 'date_practice', 'program_practice',)

    def retrieve(self, request, pk=None):
        query_params = self.request.query_params
        data = super(PracticesViewSet, self).retrieve(self, request, pk)
        data.data["params"] = query_params
        result = data.data
        result["results"] = result["results"].replace("[", "")
        result["results"] = result["results"].replace("]", "")
        list_id = result["results"].split(",")
        serial = []
        for id_result in list_id:
            objects = Results.objects.filter(id=int(id_result))
            if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
                data_serial = ResultsDetailSerializer(objects, many=True)
            else:
                data_serial = ResultsSerializer(objects, many=True)
            serial.append(data_serial.data[0])
        result["results"] = serial
        return Response(data.data)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        data = super(PracticesViewSet, self).list(self, request)
        data.data["params"] = query_params
        for result in data.data["results"]:
            result["results"] = result["results"].replace("[", "")
            result["results"] = result["results"].replace("]", "")
            list_id = result["results"].split(",")
            serial = []
            for id_result in list_id:
                objects = Results.objects.filter(id=int(id_result))
                if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
                    data_serial = ResultsDetailSerializer(objects, many=True)
                else:
                    data_serial = ResultsSerializer(objects, many=True)
                serial.append(data_serial.data[0])
            result["results"] = serial
        return Response(data.data)

    def create(self, request, *args, **kwargs):
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
                    for result in results:
                        serialized = ResultsSerializer(data=result)
                        if serialized.is_valid():
                            list_serialized.append(serialized)
                        else:
                            last_serialized = serialized
                            is_all_valid = False

                    if is_all_valid is True:
                        list_id = []
                        for serialized in list_serialized:
                            serialized.save()
                            list_id.append(serialized.data["id"])
                        request.data["results"] = list_id
                        is_complete = True
                    else:
                        response = last_serialized.errors
                else:
                    response = {"result": "El formato Json debe ser array"}
            except:
                response = {"result": "Formato Json no valido"}
        if is_complete:
            return super(PracticesViewSet, self).create(request, *args, **kwargs)
        else:
            return Response(response)
