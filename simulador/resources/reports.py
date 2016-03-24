import base64

from django.shortcuts import render_to_response
from django.views.generic import View
from easy_pdf.views import PDFTemplateView
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.colors import PCMYKColor
from simulador.resources.account import AccountSerializer
from simulador.resources.image_repository import ImageRepository, ImageRepositorySerializer
from simulador.resources.lesson import LessonSerializer
from simulador.resources.military_grade import MilitaryGradeSerializer
from simulador.resources.position import PositionSerializer
from simulador.resources.target_resource import TargetSerializer
from simulador.templatetags.pdf_filters import get64
from simuladorTiroEjercitoBackend.settings import GET_API_URL

ReportsViews = {
    "target": {"name": "Reporte de tipos de blancos", "Serializer": TargetSerializer,
               "params": (('image', 'Imagen', 'image'),
                          ('name', 'Nombre', 'text'),
                          ('description', 'Descripcion', 'text'),
                          ('zones', 'Numero de zonas', 'text'),
                          ('updated_at', 'Ultima modificacion', 'datetime'),
                          )},
    "position": {"name": "Reporte de posiciones de tiro", "Serializer": PositionSerializer,
                 "params": (('image', 'Imagen', 'image'),
                            ('name', 'Posicion', 'text'),
                            ('description', 'Descripcion', 'text'),
                            ('updated_at', 'Ultima modificacion', 'datetime'),
                            )},
    "lesson": {"name": "Reporte de lecciones de tiro", "Serializer": LessonSerializer,
               "params": (('image', 'Imagen', 'image'),
                          ('name', 'Nombre', 'text'),
                          ('description', 'Descripcion', 'text'),
                          ('updated_at', 'Ultima modificacion', 'datetime'),
                          )},
    "military_grade": {"name": "Reporte de grados militares", "Serializer": MilitaryGradeSerializer,
                       "params": (('name', 'Nombre', 'text'),
                                  ('short', 'Abreviatura', 'text'),
                                  ('updated_at', 'Ultima modificacion', 'datetime'),
                                  )},
    "account": {"name": "Reporte de cuentas de usuarios", "Serializer": AccountSerializer,
                "params": (
                    # ('image', 'Perfil', 'image'),
                    ('first_name', 'Nombres', 'text'),
                    ('last_name', 'Apellidos', 'text'),
                    ('ci', 'Carnet', 'text'),
                    ('email', 'Correo', 'text'),
                    ('updated_at', 'Ultima modificacion', 'datetime'),
                )}
}


def get_base_context(self):
    context = {}
    context["logo_ejercito_url"] = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
    context["logo_bolivia_url"] = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
    context["base_url"] = "%s" % GET_API_URL(self.request)
    return context


def generate_table_render(self, data, params):
    content = ()
    for item in data:
        row = ()
        for param in params:
            if param[2] == "image":
                if item[param[0]] is not None and item[param[0]] != "":
                    val = get64("%s%s" % (GET_API_URL(self.request), item[param[0]]))
                else:
                    val = None
            else:
                val = "%s" % item[param[0]]
            row += ((param[2], val,),)
        content += (row,)
    return content


# noinspection PyUnresolvedReferences,PyCallingNonCallable
class BaseReportView(PDFTemplateView):
    template_name = "list_report.html"

    def get_context_data(self, **kwargs):
        req = kwargs["rep"]
        if req == "lesson":
            ModelReport = ReportsViews["lesson"]
        elif req == "target":
            ModelReport = ReportsViews["target"]
        elif req == "military_grade":
            ModelReport = ReportsViews["military_grade"]
        elif req == "account":
            ModelReport = ReportsViews["account"]
        else:
            ModelReport = ReportsViews["position"]
        Serializer = ModelReport["Serializer"]
        Model = Serializer.Meta.model
        params = ModelReport["params"]
        values = Serializer(Model.objects.all(), many=True).data
        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        return super(BaseReportView, self).get_context_data(
            pagesize="A4",
            title=ModelReport["name"],
            logo_ejercito_url=logo_ejercito_url,
            logo_bolivia_url=logo_bolivia_url,
            data=values,
            params=params,
            table=generate_table_render(self, values, params),
            **kwargs)


class BaseReport2View(PDFTemplateView):
    template_name = "list_report_image.html"

    def get_context_data(self, **kwargs):
        req = kwargs["rep"]

        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        obj_Data = ImageRepository.objects.filter(id=int(req))
        data_Serial = ImageRepositorySerializer(obj_Data, many=True).data
        data_Serial = data_Serial[0]['image']
        logo_reporte = "%s" % GET_API_URL(self.request, "%s" %(data_Serial))
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


class HelloPDFView(PDFTemplateView):
    template_name = "demo_pdf.html"

    def get_context_data(self, **kwargs):
        logo_ejercito_url = "%s" % GET_API_URL(self.request, "/static/logo_ejercito.png")
        logo_bolivia_url = "%s" % GET_API_URL(self.request, "/static/escudo_bolivia.png")
        data = {}
        data["title"] = "EMI"
        data["data"] = (("Valor1", 2), ("Valor2", 5), ("Valor3", 43), ("Valor4", 43))
        d = GetPieDrawing(data)
        # d.save(formats=["png"], outDir="static", fnRoot=None)
        aa = d.asString('gif')
        binaryStuff = "%s%s" % ("data:image/png;base64,", base64.b64encode(aa))

        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title=data["title"],
            logo_ejercito_url=logo_ejercito_url,
            logo_bolivia_url=logo_bolivia_url,
            binaryss=binaryStuff,
            **kwargs
        )


class HelloView(View):
    def get(self, request):
        data = {}
        data["title"] = "EMI"
        data["data"] = (("Valor1", 2), ("Valor2", 5), ("Valor3", 43), ("Valor4", 43))
        d = GetPieDrawing(data)
        aa = d.asString('gif')
        binaryStuff = "%s%s" % ("data:image/png;base64,", base64.b64encode(aa))
        return render_to_response("demo_pdf.html", {"binaryss": binaryStuff})
