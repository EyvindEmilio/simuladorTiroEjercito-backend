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
import base64
import cStringIO
import urllib

import easy_pdf
from django import template
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View
from easy_pdf.views import PDFTemplateView
from rest_framework import routers
from simulador.resources.account import LoginView, AccountViewSet
from simulador.resources.account import LogoutView
from simulador.resources.battalion import BattalionViewSet
from simulador.resources.city import CityViewSet
from simulador.resources.company import CompanyViewSet
from simulador.resources.position import PositionViewSet
from simulador.resources.practices import PracticesViewSet
from simulador.resources.grade import GradeViewSet
from simulador.resources.lesson import LessonViewSet
from simulador.resources.military_grade import MilitaryGradeViewSet
from simulador.resources.people import PeopleViewSet
from simulador.resources.program_practice import ProgramPracticeViewSet
from simulador.resources.regiment import RegimentViewSet
from simulador.resources.reset_password import ResetPasswordViewSet
from simulador.resources.squadron import SquadronViewSet
from simulador.resources.target_resource import TargetViewSet
from simulador.resources.type_of_fire import TypeOfFireViewSet
from simulador.resources.user_type import UserTypeViewSet
from simuladorTiroEjercitoBackend.settings import GET_API_URL

router = routers.DefaultRouter()

router.register(r'Account', AccountViewSet)
router.register(r'Battalion', BattalionViewSet)
router.register(r'City', CityViewSet)
router.register(r'Company', CompanyViewSet)
router.register(r'Grade', GradeViewSet)
router.register(r'Lesson', LessonViewSet)
router.register(r'MilitaryGrade', MilitaryGradeViewSet)
router.register(r'People', PeopleViewSet)
router.register(r'ProgramPractice', ProgramPracticeViewSet)
router.register(r'Regiment', RegimentViewSet)
router.register(r'Squadron', SquadronViewSet)
router.register(r'Target', TargetViewSet)
router.register(r'UserType', UserTypeViewSet)
router.register(r'Practices', PracticesViewSet)
router.register(r'Position', PositionViewSet)
router.register(r'TypeOfFire', TypeOfFireViewSet)
router.register(r'ResetPassword', ResetPasswordViewSet)


class HelloPDFView(PDFTemplateView):
    template_name = "demo_pdf.html"

    def get_context_data(self, **kwargs):
        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            logo_ejercito_url=logo_ejercito_url,
            logo_bolivia_url=logo_bolivia_url,
            **kwargs
        )


class HelloView(View):
    def get(self, request):
        template_name = loader.get_template("demo_pdf.html")
        BASE_API = GET_API_URL(self.request)
        context = {BASE_API: BASE_API}
        return HttpResponse(template_name.render(context))


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^testPDF', HelloPDFView.as_view()),
    url(r'^testHTML', HelloView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^Login/', LoginView.as_view(), name="login"),
    url(r'^Logout/', LogoutView.as_view(), name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, )
