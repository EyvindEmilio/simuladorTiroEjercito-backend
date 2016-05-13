from django.db import models
from django.utils import timezone
from rest_framework import viewsets, filters, serializers, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountDetailSerializer
from simulador.resources.lesson import LessonDetailSerializer, Lesson
from simuladorTiroEjercitoBackend import settings
from simuladorTiroEjercitoBackend.settings import GET_API_URL


class ProgramPractice(models.Model):
    title = models.CharField(max_length=40, unique=True, blank=False)
    instructor = models.ForeignKey(Account, related_name='instructor')
    lesson = models.ManyToManyField(Lesson, null=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    is_evaluation = models.BooleanField(default=False)
    is_test_mode = models.BooleanField(default=False)
    list = models.ManyToManyField(Account, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finish = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s , De: %s ----a---- %s " % (self.title, self.start, self.end,)

    #
    # @property
    # def _get_finish(self):
    #     return 3
    #
    # # @property
    # # def _completed(self):
    # #     return 2dv

    class Meta:
        ordering = ['-created_at']


class ProgramPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramPractice
        fields = (
            'id', 'title', 'instructor', 'lesson', 'start', 'end', 'is_evaluation', 'is_test_mode', 'finish',
            'completed', 'list', 'created_at', 'updated_at')


class ProgramPracticeDetailSerializer(serializers.ModelSerializer):
    instructor = AccountDetailSerializer(read_only=True)
    lesson = LessonDetailSerializer(read_only=True, many=True)
    list = AccountDetailSerializer(read_only=True, many=True)

    class Meta:
        model = ProgramPractice
        fields = (
            'id', 'title', 'instructor', 'lesson', 'start', 'end', 'is_evaluation', 'completed', 'list',
            'is_test_mode', 'finish', 'list', 'completed', 'created_at', 'updated_at')


def get_sum(list_array, label):
    sum_ = 0
    for x in list_array:
        sum_ += int(x[label])
    return sum_


def get_results_by_user(user_id=False, custom_practice_id=False, complete=False):
    from simulador.resources.custom_practices import CustomPractices
    from simulador.resources.custom_practices import CustomPracticesDetailSerializer
    if id is not False:
        practices_object_data = CustomPractices.objects.filter(id=custom_practice_id, practicing=user_id)
        practices_serial_data = CustomPracticesDetailSerializer(practices_object_data, many=True).data
        results_by_practice = {}
        if len(practices_serial_data) > 0:
            results_by_practice = convert_results_data(practices_serial_data, complete)
        return results_by_practice
    else:
        return []


def convert_results_data(practices_serial_data, complete=False):
    results_by_practice = practices_serial_data[0]
    practicing = results_by_practice['practicing']
    if complete is False:
        results_by_practice['practicing'] = "%s. %s %s, %s %s" % (
            practicing['military_grade']['short'], practicing['first_name'], practicing['last_name'],
            practicing['ci'], practicing['city']['short'])
        results_by_practice['practicing_image'] = practicing['image']

    global_time = 0
    global_score = 0

    results_by_practice['result_by_lesson'] = []
    results_by_practice['result_by_type_of_fire'] = []
    results_by_practice['result_by_position'] = []
    for result in results_by_practice['results']:
        # for global
        global_time = get_sum(result['results_zone'], 'time')
        global_score = get_sum(result['results_zone'], 'score')

        # for lesson
        if len(results_by_practice['result_by_lesson']) > 0:
            old_value_lesson = False
            for temp in results_by_practice['result_by_lesson']:
                if temp['lesson'] == result['lesson']['id']:
                    old_value_lesson = temp
            if old_value_lesson is not False:
                old_value_lesson['time'] += get_sum(result['results_zone'], 'time')
                old_value_lesson['score'] += get_sum(result['results_zone'], 'score')
            else:
                results_by_practice['result_by_lesson'].append(
                    {
                        'lesson': result['lesson']['id'],
                        'time': get_sum(result['results_zone'], 'time'),
                        'score': get_sum(result['results_zone'], 'score'),
                    }
                )
        else:
            results_by_practice['result_by_lesson'].append(
                {
                    'lesson': result['lesson']['id'],
                    'time': get_sum(result['results_zone'], 'time'),
                    'score': get_sum(result['results_zone'], 'score'),
                }
            )
        # for type_of_fire
        if len(results_by_practice['result_by_type_of_fire']) > 0:
            old_value_type_of_fire = False
            for temp in results_by_practice['result_by_type_of_fire']:
                if temp['type_of_fire'] == result['type_of_fire']['id']:
                    old_value_type_of_fire = temp
            if old_value_type_of_fire is not False:
                old_value_type_of_fire['time'] += get_sum(result['results_zone'], 'time')
                old_value_type_of_fire['score'] += get_sum(result['results_zone'], 'score')
            else:
                results_by_practice['result_by_type_of_fire'].append(
                    {
                        'type_of_fire': result['type_of_fire']['id'],
                        'time': get_sum(result['results_zone'], 'time'),
                        'score': get_sum(result['results_zone'], 'score'),
                    }
                )
        else:
            results_by_practice['result_by_type_of_fire'].append(
                {
                    'type_of_fire': result['type_of_fire']['id'],
                    'time': get_sum(result['results_zone'], 'time'),
                    'score': get_sum(result['results_zone'], 'score'),
                }
            )
        # for position
        if len(results_by_practice['result_by_position']) > 0:
            old_value_type_of_fire = False
            for temp in results_by_practice['result_by_position']:
                if temp['position'] == result['position']['id']:
                    old_value_type_of_fire = temp
            if old_value_type_of_fire is not False:
                old_value_type_of_fire['time'] += get_sum(result['results_zone'], 'time')
                old_value_type_of_fire['score'] += get_sum(result['results_zone'], 'score')
            else:
                results_by_practice['result_by_position'].append(
                    {
                        'position': result['position']['id'],
                        'time': get_sum(result['results_zone'], 'time'),
                        'score': get_sum(result['results_zone'], 'score'),
                    }
                )
        else:
            results_by_practice['result_by_position'].append(
                {
                    'position': result['position']['id'],
                    'time': get_sum(result['results_zone'], 'time'),
                    'score': get_sum(result['results_zone'], 'score'),
                }
            )
        result['time'] = get_sum(result['results_zone'], 'time')
        result['score'] = get_sum(result['results_zone'], 'score')
        result['min_score'] = result['type_of_fire']['min_score']

        if result['score'] >= result['type_of_fire']['min_score']:
            result['is_approved'] = True
        else:
            result['is_approved'] = False
        if complete is False:
            result['lesson_name'] = result['lesson']['name']
            result['lesson'] = result['lesson']['id']
            result['type_of_fire_name'] = result['type_of_fire']['name']
            result['type_of_fire_distance'] = result['type_of_fire']['distance']
            result['type_of_fire_target_zones'] = result['type_of_fire']['target']['zones']
            result['type_of_fire'] = result['type_of_fire']['id']
            result['position_name'] = result['position']['name']
            result['position'] = result['position']['id']
            # result['results_zone'] = ""
    results_by_practice['result_global'] = {'time': global_time, 'score': global_score}
    return results_by_practice


def get_results_by_user_id(user_id=False, program_practice_id=False, complete=False):
    from simulador.resources.practices import Practices
    from simulador.resources.practices import PracticesDetailSerializer
    if id is not False:
        practices_object_data = Practices.objects.filter(practicing=user_id, program_practice=program_practice_id)
        practices_serial_data = PracticesDetailSerializer(practices_object_data, many=True).data

        results_by_practice = {}
        if len(practices_serial_data) > 0:
            results_by_practice = convert_results_data(practices_serial_data, complete)
            del (results_by_practice['program_practice'])
        return results_by_practice
    else:
        return []


class ProgramPracticeViewSet(viewsets.ModelViewSet):
    """
    Para obtener practicas por usuario, ingresar:

    [_/ProgramPractice/current/?user=**3**_](/ProgramPractice/current/?user=3)

    """
    queryset = ProgramPractice.objects.all()
    serializer_class = ProgramPracticeSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('title', 'is_evaluation', 'is_test_mode', 'list__id')
    search_fields = ('title',)

    def get_serializer_class(self):
        query_params = self.request.query_params
        if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
            return ProgramPracticeDetailSerializer
        else:
            return ProgramPracticeSerializer

    @list_route()
    def current(self, request):
        query_params = self.request.query_params

        if 'user' in query_params:
            user = int(query_params['user'])
            today = timezone.now()
            objects_practice = ProgramPractice.objects.filter(end__gte=today, start__lte=today, list__id=user)
            practice_data = ProgramPracticeDetailSerializer(objects_practice, many=True)

            exist_finish_practice = False
            for practice in practice_data.data:
                del practice["list"]
                from simulador.resources.practices import Practices
                if Practices.objects.filter(program_practice=practice['id'], practicing=user).count() > 0:
                    exist_finish_practice = True
                    break
                else:
                    for lesson in practice['lesson']:
                        lesson['image'] = settings.GET_API_URL(self.request, lesson['image'])
                        for type_of_fire in lesson['type_of_fire']:
                            type_of_fire['position']['image'] = settings.GET_API_URL(self.request,
                                                                                     type_of_fire['position']['image'])
                            type_of_fire['target']['image'] = settings.GET_API_URL(self.request,
                                                                                   type_of_fire['target']['image'])
            if exist_finish_practice:
                return Response({
                    'practice': []
                })
            else:
                return Response({
                    'practice': practice_data.data
                })

        else:
            return Response({"Id de usuario": "debe enviar id de usuario en 'query params', Ejm. '../?user=3'"})

    @detail_route()
    def results(self, request, pk):
        query_params = self.request.query_params
        from simulador.resources.practices import Practices, PracticesSerializer
        practices_object_data = Practices.objects.filter(program_practice=pk)
        practices_serial_data = PracticesSerializer(practices_object_data, many=True).data
        response = {}
        response_status = status.HTTP_200_OK
        if len(practices_serial_data) > 0:
            list_result_practice = []
            if 'practicing' in query_params:
                response = get_results_by_user_id(query_params['practicing'], pk)
                response["practicing_image"] = GET_API_URL(request, response["practicing_image"])
            else:
                for practice_result in practices_serial_data:
                    tmp = get_results_by_user_id(practice_result['practicing'], pk)
                    tmp["practicing_image"] = GET_API_URL(request, tmp["practicing_image"])
                    list_result_practice.append(tmp)
                response = {'result': list_result_practice}
        else:
            response['detail'] = 'No se encontraron resultados'
            response_status = status.HTTP_204_NO_CONTENT
        return Response(response, response_status)
