# -*- coding: UTF-8 -*-
import StringIO

from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import View
from easy_pdf.views import PDFTemplateView
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.colors import PCMYKColor
from simulador.resources.account import AccountSerializer, Account
from simulador.resources.image_repository import ImageRepository, ImageRepositorySerializer
from simulador.resources.lesson import LessonSerializer, Lesson
from simulador.resources.military_grade import MilitaryGradeSerializer, MilitaryGrade
from simulador.resources.position import PositionSerializer, Position
from simulador.resources.target_resource import TargetSerializer, Target
from simuladorTiroEjercitoBackend.settings import GET_API_URL
from xhtml2pdf import pisa

ReportModels = {
    "lesson": {
        "title": "Lista de lecciones de tiro",
        "data": LessonSerializer(Lesson.objects.all(), many=True).data,
        "fields": (
            {"label": "Imagen", "name": "image", "width": "15%", "type": "image"},
            {"label": "Nombre", "name": "name", "width": "30%", "type": "text"},
            {"label": "Descripción", "name": "description", "width": "35%", "type": "text"},
            {"label": "Última modificación", "name": "updated_at", "width": "20%", "type": "datetime"}
        )
    },
    "target": {
        "title": "Lista de tipos de blancos",
        "data": TargetSerializer(Target.objects.all(), many=True).data,
        "fields": (
            {"label": "Blanco", "name": "image", "width": "20%", "type": "image"},
            {"label": "Nombre del blanco", "name": "name", "width": "30%", "type": "text"},
            {"label": "Numero de zonas", "name": "zones", "width": "25%", "type": "text", "class": "center"},
            {"label": "Última modificación", "name": "updated_at", "width": "25%", "type": "datetime"}
        )
    },
    "position": {
        "title": "Lista de posiciones del tirador",
        "data": PositionSerializer(Position.objects.all(), many=True).data,
        "fields": (
            {"label": "Posición", "name": "image", "width": "15%", "type": "image"},
            {"label": "Nombre de posición", "name": "name", "width": "35%", "type": "text"},
            {"label": "Descripción", "name": "description", "width": "25%", "type": "text"},
            {"label": "Última modificación", "name": "updated_at", "width": "25%", "type": "datetime"}
        )
    },
    "military_grade": {
        "title": "Grados militares registrados",
        "data": MilitaryGradeSerializer(MilitaryGrade.objects.all(), many=True).data,
        "show_index": True,
        "fields": (
            {"label": "Nombre", "name": "name", "width": "30%", "type": "text"},
            {"label": "Abreviatura", "name": "short", "width": "25%", "type": "text"},
            {"label": "Última modificación", "name": "updated_at", "width": "35%", "type": "datetime"}
        )
    },
    "account": {
        "title": "Lista de usuarios registrados",
        "data": AccountSerializer(Account.objects.all(), many=True).data,
        "show_index": True,
        "fields": (
            {"label": "Nombres", "name": "first_name", "width": "15%", "type": "text"},
            {"label": "Apellidos", "name": "last_name", "width": "15%", "type": "text"},
            {"label": "Correo", "name": "email", "width": "30%", "type": "text"},
            {"label": "Carnet", "name": "ci", "width": "10%", "type": "text"},
            {"label": "Última modificación", "name": "updated_at", "width": "35%", "type": "datetime"}
        )
    }
}


class BaseReport2View(PDFTemplateView):
    template_name = "list_report_image.html"

    def get_context_data(self, **kwargs):
        req = kwargs["rep"]

        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        obj_Data = ImageRepository.objects.filter(id=int(req))
        data_Serial = ImageRepositorySerializer(obj_Data, many=True).data
        data_Serial = data_Serial[0]['image']
        logo_reporte = "%s" % GET_API_URL(self.request, "%s" % (data_Serial))
        return super(BaseReport2View, self).get_context_data(
            pagesize="A4",
            title="Reporte de progreso en simulador",
            logo_ejercito_url=logo_ejercito_url,
            logo_bolivia_url=logo_bolivia_url,
            logo_imagen_url=logo_reporte,
            **kwargs)


class GetPieDrawing(Drawing):
    def __init__(self, data, width=500, height=500, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        self.add(Pie(), name='chart')
        self.add(String(10, self.height - 20, data["title"]), name='title')
        self.chart.x = 80
        self.chart.y = 80
        self.chart.width = self.width - self.chart.x * 2
        self.chart.height = self.height - self.chart.y * 2
        self.title.fontName = 'Helvetica-Bold'
        self.title.fontSize = 16
        self.chart.data = [dat[1] for dat in data["data"]]
        self.chart.labels = map(str, ["%s" % dat[0] for dat in data["data"]])
        colors = [PCMYKColor(100, 47, 0, x) for x in
                  (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100)]
        for i, color in enumerate(colors):
            self.chart.slices[i].fillColor = color


class ReportsView(View):
    def get(self, request, **kwargs):
        model_name = kwargs['model']
        context = {
            "model": ReportModels[model_name]
        }
        file_data = render_to_string('report_model.html', context, RequestContext(request))
        file = StringIO.StringIO()
        pisa.CreatePDF(file_data, file)
        file.seek(0)
        response = HttpResponse(file.getvalue())
        # response['Content-Disposition'] = 'attachment; filename=test.pdf'
        response['Content-Disposition'] = 'filename=' + ReportModels[model_name]['title'] + '.pdf'
        response['Content-Type'] = 'application/pdf'
        return response


class ReportProgramPracticeView(View):
    def get(self, request, **kwargs):
        id_program_practice = kwargs['id_program_practice']
        from simulador.resources.practices import Practices
        practices_object_data = Practices.objects.filter(program_practice=id_program_practice)
        from simulador.resources.practices import PracticesSerializer
        practices_serial_data = PracticesSerializer(practices_object_data, many=True).data
        from simulador.resources.program_practice import ProgramPractice
        from simulador.resources.program_practice import ProgramPracticeDetailSerializer
        practices_detail_serial_data = ProgramPracticeDetailSerializer(
            ProgramPractice.objects.filter(id=id_program_practice),
            many=True).data

        list_result_practice = []
        if len(practices_serial_data) > 0:
            for practice_result in practices_serial_data:
                from simulador.resources.program_practice import get_results_by_user_id
                tmp = get_results_by_user_id(practice_result['practicing'], id_program_practice, True)
                # tmp["practicing_image"] = GET_API_URL(request, tmp["practicing_image"])
                list_result_practice.append(tmp)
        list_not_practice = []
        for list_user in practices_detail_serial_data[0]['list']:
            if Practices.objects.filter(practicing=list_user['id']).count() == 0:
                list_not_practice.append(list_user)

        context = {
            "program_practice": practices_detail_serial_data[0],
            "data": list_result_practice,
            "list_not_practice": list_not_practice
        }
        file_data = render_to_string('report_program_practice.html', context, RequestContext(request))
        file = StringIO.StringIO()
        pisa.CreatePDF(file_data, file)
        file.seek(0)
        response = HttpResponse(file.getvalue())
        # response['Content-Disposition'] = 'attachment; filename=test.pdf'
        response['Content-Disposition'] = 'filename=Reporte de practica.pdf'
        response['Content-Type'] = 'application/pdf'
        return response
