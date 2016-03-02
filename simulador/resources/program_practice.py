from django.db import models
from rest_framework import viewsets, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountSerializer, AccountDetailSerializer
from simulador.resources.lesson import Lesson, LessonSerializer, LessonDetailSerializer
from simulador.resources.target_resource import Target
from rest_framework.response import Response

HOURS = (
    (1, "00:00 - 00:30"),
    (2, "00:30 - 01:00"),
    (3, "01:00 - 01:30"),
    (4, "01:30 - 02:00"),
    (5, "02:00 - 02:30"),
    (6, "02:30 - 03:00"),
    (7, "03:00 - 03:30"),
    (8, "03:30 - 04:00"),
    (9, "04:00 - 04:30"),
    (10, "04:30 - 05:00"),
    (11, "05:00 - 05:30"),
    (12, "06:00 - 06:30"),
    (13, "06:30 - 07:00"),
    (14, "07:00 - 07:30"),
    (15, "07:30 - 08:00"),
    (16, "08:00 - 08:30"),
    (17, "08:30 - 09:00"),
    (18, "09:00 - 09:30"),
    (19, "09:30 - 10:00"),
    (20, "10:00 - 10:30"),
    (21, "10:30 - 11:00"),
    (22, "11:00 - 11:30"),
    (23, "11:30 - 12:00"),
    (24, "12:00 - 12:30"),
    (25, "12:30 - 13:00"),
    (25, "13:00 - 13:30"),
    (26, "13:30 - 14:00"),
    (27, "14:00 - 14:30"),
    (29, "14:30 - 15:00"),
    (30, "15:00 - 16:30"),
    (31, "15:30 - 16:00"),
    (32, "16:00 - 14:30"),
)


#
# class ProgramLesson(models.Model):
#     name = models.CharField(max_length=40, unique=True, blank=False)
#     instructor = models.ForeignKey(Account, null=False, related_name='instructor')
#     lesson = models.ForeignKey(Lesson, null=False)
#     date = models.DateField(null=False)
#     hours_assigned = models.IntegerField(null=False, choices=HOURS)
#     list = models.ManyToManyField(Account, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['name']
#

class ProgramPractice(models.Model):
    title = models.CharField(max_length=40, unique=True, blank=False)
    instructor = models.ForeignKey(Account, null=False, related_name='instructor')
    lesson = models.ManyToManyField(Lesson, null=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    is_evaluation = models.BooleanField(default=False)
    is_test_mode = models.BooleanField(default=False)
    list = models.ManyToManyField(Account, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class ProgramPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramPractice
        fields = (
            'id', 'title', 'instructor', 'lesson', 'start', 'end', 'is_evaluation', 'is_test_mode', 'list',
            'created_at', 'updated_at')


class ProgramPracticeDetailSerializer(serializers.ModelSerializer):
    instructor = AccountDetailSerializer(read_only=True)
    lesson = LessonDetailSerializer(read_only=True, many=True)
    list = AccountDetailSerializer(read_only=True, many=True)

    class Meta:
        model = ProgramPractice
        fields = (
            'id', 'title', 'instructor', 'lesson', 'start', 'end', 'is_evaluation', 'is_test_mode', 'list',
            'created_at', 'updated_at')


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
