"""simuladorTiroEjercitoBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from simulador.resources.account import LoginView, AccountViewSet
from simulador.resources.account import LogoutView
from simulador.resources.battalion import BattalionViewSet
from simulador.resources.city import CityViewSet
from simulador.resources.company import CompanyViewSet
from simulador.resources.custom_practices import CustomPracticesViewSet
from simulador.resources.grade import GradeViewSet
from simulador.resources.image_repository import ImageRepositoryViewSet
from simulador.resources.lesson import LessonViewSet
from simulador.resources.logs import LogsView, LogsViewSet
from simulador.resources.military_grade import MilitaryGradeViewSet
from simulador.resources.people import PeopleViewSet
from simulador.resources.position import PositionViewSet
from simulador.resources.practices import PracticesViewSet
from simulador.resources.program_practice import ProgramPracticeViewSet
from simulador.resources.progress import ProgressViewSet
from simulador.resources.regiment import RegimentViewSet
from simulador.resources.reports import BaseReport2View, ReportsView, ReportProgramPracticeView
from simulador.resources.reset_password import ResetPasswordViewSet
from simulador.resources.results import ResultsViewSet
from simulador.resources.results_zone import ResultsZoneViewSet
from simulador.resources.squadron import SquadronViewSet
from simulador.resources.target_resource import TargetViewSet
from simulador.resources.type_of_fire import TypeOfFireViewSet
from simulador.resources.user_type import UserTypeViewSet

router = routers.DefaultRouter()

router.register(r'Account', AccountViewSet)
router.register(r'Battalion', BattalionViewSet)
router.register(r'City', CityViewSet)
router.register(r'Company', CompanyViewSet)
router.register(r'CustomPractices', CustomPracticesViewSet)
router.register(r'Grade', GradeViewSet)
router.register(r'Lesson', LessonViewSet)
router.register(r'MilitaryGrade', MilitaryGradeViewSet)
router.register(r'People', PeopleViewSet)
router.register(r'Position', PositionViewSet)
router.register(r'Practices', PracticesViewSet)
router.register(r'ProgramPractice', ProgramPracticeViewSet)
router.register(r'Regiment', RegimentViewSet)
router.register(r'ResetPassword', ResetPasswordViewSet)
router.register(r'Results', ResultsViewSet)
router.register(r'ResultsZone', ResultsZoneViewSet)
router.register(r'Squadron', SquadronViewSet)
router.register(r'Target', TargetViewSet)
router.register(r'TypeOfFire', TypeOfFireViewSet)
router.register(r'UserType', UserTypeViewSet)
router.register(r'ProgressType', ProgressViewSet)
router.register(r'LogsView', LogsViewSet)
router.register(r'ImageRepository', ImageRepositoryViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^report/(?P<model>[a-zA-Z0-9_.-]+)/$', ReportsView.as_view()),
    url(r'^reportProgramPractice/(?P<id_program_practice>[a-zA-Z0-9_.-]+)/$', ReportProgramPracticeView.as_view()),
    url(r'^view_image/(?P<rep>[a-zA-Z0-9_.-]+)/$', BaseReport2View.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^Login/', LoginView.as_view(), name="login"),
    url(r'^Logout/', LogoutView.as_view(), name="logout"),
    url(r'^Logs/', LogsView.as_view(), name="logs"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, )
