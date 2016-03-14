import uuid

from django.core.mail import send_mail
from django.db import models
from django.db.models.expressions import Date, DateTime
from django.http import BadHeaderError
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, filters, serializers
from rest_framework.fields import Field
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountSerializer
from simuladorTiroEjercitoBackend import settings


class ResetPassword(models.Model):
    id_user = models.ForeignKey(Account)
    date_expired = models.DateTimeField()
    token_reset = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = ('id', 'id_user', 'date_expired', 'token_reset', 'created_at', 'updated_at')
        # read_only_fields = ('id_user', 'date_expired', 'token_reset',)
        # extra_kwargs = {'password': {'write_only': True}}


class ResetPasswordViewSet(viewsets.ModelViewSet):
    queryset = ResetPassword.objects.all()
    serializer_class = ResetPasswordSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id', 'id_user', 'token_reset')
    search_fields = ('$id_user',)

    def destroy(self, request, *args, **kwargs):
        data = self.request.query_params

        if ('id_user' in data) and ('new_password' in data):
            user = (Account.objects.filter(id=data["id_user"]))[0]
            user.set_password(data["new_password"])
            user.save()
            super(ResetPasswordViewSet, self).destroy(self, request)
            return Response({"detail": "Password restablecido"})
        else:
            return Response({"detail": "No se restablecio password"}, status=400)

    def create(self, request, *args, **kwargs):
        data = request.data
        email = request.data["email"]
        accounts_data = AccountSerializer(Account.objects.filter(email=email), many=True)
        if len(accounts_data.data) > 0:
            user = accounts_data.data[0]
            request.data['id_user'] = user['id']

            response_mail = send_mail_reset(email, user)
            if response_mail["valid"]:
                request.data["date_expired"] = datetime.now()
                request.data["token_reset"] = response_mail["token"]
                serializer = ResetPasswordSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save();
                    return Response(serializer.data)
                else:
                    return Response(serializer.data)
            else:
                return Response({"detail": "Cuenta de usuario no encontrada"}, status=400)
        else:
            return Response({"detail": "Cuenta de usuario no encontrada"}, status=400)


def send_mail_reset(email_to, user):
    token_reset = uuid.uuid1().hex
    message = "Usuario %s %s (%s), ingrese a esta direccion para recuperar su password: Http://127.0.0.1:9000/#/reset/password/%s" % (
        user["first_name"], user["last_name"], user["ci"], token_reset,)
    try:
        mail = send_mail('Recuperar password', message, settings.EMAIL_HOST_USER, [email_to], fail_silently=False)

        return {
            "valid": True,
            "token": token_reset,
            "mail": mail
        }
    except BadHeaderError:
        return {
            "valid": False
        }
