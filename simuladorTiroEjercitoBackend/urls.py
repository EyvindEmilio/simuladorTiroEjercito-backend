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

import select

import easy_pdf
import reportlab
from PIL import Image
from django.shortcuts import render_to_response
from reportlab.lib.colors import PCMYKColor
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import BarChartLabel
from reportlab.graphics.charts.piecharts import Pie3d
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


class MyBarChartDrawing(Drawing):
    def __init__(self, width=400, height=200, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.add(Pie3d(), name='chart')
        self.add(String(200, 180, 'Hello World'), name='title')
        self.chart.x = 20
        self.chart.y = 20
        self.chart.width = self.width - 40
        self.chart.height = self.height - 80
        self.title.fontName = 'Helvetica-Bold'
        self.title.fontSize = 12
        data = (5, 4, 3, 2, 1)
        categories = ('sale', 'marketing', 'travel', 'health', 'misc')
        colors = [PCMYKColor(100, 50, 30, x) for x in (50, 40, 30, 20, 10)]
        self.chart.data = data
        self.chart.labels = map(str, categories)
        for i, color in enumerate(colors): self.chart.slices[i].fillColor = color


class HelloPDFView(PDFTemplateView):
    template_name = "demo_pdf.html"

    def get_context_data(self, **kwargs):
        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        d = MyBarChartDrawing()
        # d.save(formats=["png"], outDir="static", fnRoot=None)
        aa = d.asString('gif')
        binaryStuff = "%s%s" % ("data:image/png;base64,", base64.b64encode(aa))

        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="ddd",
            logo_ejercito_url=logo_ejercito_url,
            logo_bolivia_url=logo_bolivia_url,
            binaryss=binaryStuff,
            **kwargs
        )


class HelloView(View):
    def get(self, request):
        d = MyBarChartDrawing()
        aa = d.asString('gif')
        binaryStuff = "%s%s" % ("data:image/png;base64,", base64.b64encode(aa))
        # return HttpResponse(binaryStuff, 'image/gif')
        return render_to_response("demo_pdf.html", {"binaryss": binaryStuff})


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
