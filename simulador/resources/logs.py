from django.apps import apps
import simple_audit
from simple_audit.models import Audit
from simple_audit.models import AuditChange
from simple_audit.models import AuditRequest
from rest_framework.response import Response
from rest_framework import viewsets, views, filters, serializers
from simulador.pagination import BasePagination
from simulador.resources.account import AccountShortDetailSerializer
from simulador.resources.city import City
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id', 'app_label', 'model')


class AuditRequestSerializer(serializers.ModelSerializer):
    user = AccountShortDetailSerializer(read_only=True)

    class Meta:
        model = AuditRequest
        fields = (
            'id', 'request_id', 'ip', 'path', 'date', 'user')
        order_by = (
            ('date',)
        )


class AuditSerializer(serializers.ModelSerializer):
    audit_request = AuditRequestSerializer(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Audit
        fields = (
            'id', 'date', 'operation', 'content_type', 'object_id', 'audit_request', 'description', 'obj_description')


class AuditChangeSerializer(serializers.ModelSerializer):
    audit = AuditSerializer(read_only=True)

    class Meta:
        model = AuditChange
        fields = (
            'id', 'audit', 'field', 'old_value', 'new_value',)


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Audit.objects.order_by('-date')
    serializer_class = AuditSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = (
        '$audit_request__user__first_name', '$audit_request__user__last_name', '$audit_request__user__ci',
        '$audit_request__user__user_type__short', '$date', '$description')
    http_method_names = ('get',)

    def list(self, request, *args, **kwargs):
        data_request = super(LogsViewSet, self).list(self, request)
        data = data_request.data
        for result in data['results']:
            description = result['description']
            operation = result['operation']
            if operation == '1' or operation == 1:
                description = description.replace("field ", "<b>-</b> <b>")
                description = description.replace("' to '", "</spam>' a <spam class='bg-success'>'")
                description = description.replace(" to '", "</spam> a <spam class='bg-success'>")
                description = description.replace(" to ", "</spam> a <spam class='bg-success'>")
                description = description.replace("' was changed from '",
                                                  " </b> de <spam class='bg-danger'> '")
                description = description.replace(" was changed from ",
                                                  " </b> de <spam class='bg-danger'> ")
                description = description.replace("\n", "</spam><br>\n")
                description = description.replace("'\n", "'</spam><br>\n")
                description = "Con ID: <b>%s</b><br> %s" % (result['object_id'], description)
                # description = "<pre>%s</pre>" % description
                result['operation'] = "<b class='btn-warning btn-xs'>Modificar</b>"
            elif operation == '0' or operation == 0:
                description = description.replace("Added ", "Registro ingresado:  <spam class='bg-success'>")
                description = "%s</spam> <br>Con ID: <b>%s</b>" % (description, result['object_id'])
                result['operation'] = "<b class='btn-success btn-xs'>Ingresar</b>"
            elif operation == '2' or operation == 2:
                description = description.replace("Deleted ", "Registro eliminado: <spam class='bg-danger'>")
                description = "%s</spam> <br>Con ID: <b>%s</b>" % (description, result['object_id'])
                result['operation'] = "<b class='btn-danger btn-xs'>Eliminar</b>"
            result['description'] = description

            if ('audit_request' in result) and (result['audit_request'] is not None):
                user = result['audit_request']['user']
                result['ci'] = "%s %s" % (user['ci'], user['city']['short'])
                user_type = "<spam class='btn-info btn-xs'>%s</spam>" % user['user_type']['short']
                result['user'] = "%s. %s %s , %s %s" % (
                    user['military_grade']['short'], user['first_name'], user['last_name'], result['ci'], user_type)

                result['email'] = user['email']
                result['image'] = user['image']
                result['ip_address'] = result['audit_request']['ip']
                result['path'] = result['audit_request']['path']
            else:
                result['ci'] = "-- desconocido --"
                result['user'] = "-- desconocido --"
                result['email'] = "-- desconocido --"
                result['image'] = ""
                result['ip_address'] = "-- desconocido --"
                result['path'] = "-- desconocido --"
            result['table'] = "<pre style='padding: 2px 5px'>%s</pre>" % result['content_type']['model']
            del (result['content_type'])
            if 'ci' in result:
                del (result['ci'])
            if 'audit_request' in result:
                del (result['audit_request'])
            if 'obj_description' in result:
                del (result['obj_description'])
        return Response(data)


class LogsView(views.APIView):
    def get(self, request):
        simple_audit.register()
        return Response({"d": 22})

        # reversion.get_f
