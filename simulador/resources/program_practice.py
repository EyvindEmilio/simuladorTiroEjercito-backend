import simulador
from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountDetailSerializer
from simulador.resources.lesson import LessonDetailSerializer, Lesson


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
        ordering = ['created_at']


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


class ProgramPracticeViewSet(viewsets.ModelViewSet):
    queryset = ProgramPractice.objects.all()
    serializer_class = ProgramPracticeSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('title', 'is_evaluation', 'is_test_mode')
    search_fields = ('title',)

    def get_serializer_class(self):
        query_params = self.request.query_params
        if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
            return ProgramPracticeDetailSerializer
        else:
            return ProgramPracticeSerializer
