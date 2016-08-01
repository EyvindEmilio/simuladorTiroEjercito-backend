from django.db import models
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from simulador.pagination import BasePagination
from simulador.resources.account import Account, AccountDetailSerializer
from simulador.resources.company import Company


class Squadron(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=False)
    list = models.ManyToManyField(Account)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SquadronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squadron
        fields = ('id', 'name', 'company', 'list', 'updated_at')


class SquadronViewSet(viewsets.ModelViewSet):
    queryset = Squadron.objects.all()
    serializer_class = SquadronSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('name', 'company')
    search_fields = ('$name', '$company__name', '$list__first_name', '$list__last_name', '$list__ci')

    # permission_classes = (IsAuthenticated,)
    @detail_route()
    def practitioners(self, request, pk):
        data_squadron = SquadronSerializer(Squadron.objects.filter(pk=pk), many=True).data
        object_list_accounts = []
        if len(data_squadron) > 0:
            list_account_squadron = data_squadron[0]['list']
            for id_account in list_account_squadron:
                account = AccountDetailSerializer(Account.objects.filter(pk=id_account), many=True).data[0]
                from simuladorTiroEjercitoBackend.settings import GET_API_URL
                account["image"] = GET_API_URL(request, account["image"])
                object_list_accounts.append(account)

        return Response({"data": object_list_accounts})
