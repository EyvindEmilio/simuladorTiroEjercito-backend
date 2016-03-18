from django.contrib.auth import authenticate
import datetime

from django.contrib.auth.hashers import SHA1PasswordHasher, PBKDF2PasswordHasher, make_password
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    AnonymousUser, User)
from rest_framework import viewsets, views, serializers, status, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from simulador.pagination import BasePagination
from simulador.resources.city import CitySerializer, City
from simulador.resources.military_grade import MilitaryGrade, MilitaryGradeSerializer
from simulador.resources.people import PeopleSerializer
from simulador import strings
# from simulador.resources.program_practice import ProgramPracticeDetailSerializer, ProgramPractice
from simulador.resources.user_type import UserType, UserTypeSerializer
from simuladorTiroEjercitoBackend import settings

GENDERS_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)


class AccountManager(BaseUserManager):
    def create_user(self, ci, password=None, **kwargs):
        if not ci:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(ci), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, ci, password, **kwargs):
        account = self.create_user(ci, password, **kwargs)
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.ForeignKey(UserType, null=False, blank=False)

    ##Auth
    ci = models.CharField(max_length=10, help_text='Ejem. 9981765', blank=False, null=False, unique=True)
    username = models.CharField(max_length=40, unique=True)
    ##Info
    email = models.EmailField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="People/images/", default='')
    phone_number = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES)
    first_name = models.CharField(max_length=20, help_text='Ejem. Juan', unique=False)
    last_name = models.CharField(max_length=20, help_text='Ejem. Peres', blank=True, null=True, unique=False)
    date_of_birth = models.DateField(help_text='Ejem. 12/03/1993', blank=True, null=True)
    city = models.ForeignKey(City, help_text='Id: Ejem. 1', blank=True, null=True)
    ##Grade
    military_grade = models.ForeignKey(MilitaryGrade, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'ci'
    REQUIRED_FIELDS = ['username']

    # def get_absolute_url(self):
    #     domain = Site.objects.get_current().domain
    #
    #     return 'http://%s' % (domain,)
    # def set_password(self, raw_password):

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __unicode__(self):
        return "%s: %s %s,  %s" % (self.user_type, self.first_name, self.last_name, self.ci,)

    def get_full_name(self):
        return ' '.join([self.username])

    def get_short_name(self):
        return self.first_name

    def is_admin_user(self):
        return self.is_admin


class AccountSerializer(serializers.ModelSerializer):
    # info = PeopleSerializer(read_only=True)
    # image = serializers.SerializerMethodField()
    #
    # def get_image(self, obj):
    #     return self.context['request'].build_absolute_uri(self.image)

    class Meta:
        model = Account

        fields = (
            'is_admin', 'is_staff', 'is_superuser', 'user_type', 'id', 'is_active', 'username', 'email', 'image',
            'phone_number', 'gender', 'ci', 'first_name', 'last_name', 'date_of_birth', 'city', 'military_grade',
            'password', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request', None)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)

        instance.save()

        return instance


class AccountDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    military_grade = MilitaryGradeSerializer(read_only=True)
    user_type = UserTypeSerializer(read_only=True)

    class Meta:
        model = Account

        fields = (
            'id', 'is_active', 'username', 'email', 'image', 'phone_number', 'user_type', 'gender', 'ci', 'first_name',
            'last_name', 'date_of_birth', 'city', 'military_grade', 'created_at', 'updated_at')


class AccountDetailViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


class AccountViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminUser,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = BasePagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = (
        'first_name', 'last_name', 'is_admin', 'is_staff', 'is_superuser', 'user_type', 'id', 'is_active',)
    search_fields = ('$first_name', '$last_name', '$ci')

    def get_serializer_class(self):
        query_params = self.request.query_params
        if 'is_complete_serializer' in query_params and query_params['is_complete_serializer'] == '1':
            return AccountDetailSerializer
        else:
            return AccountSerializer

    def partial_update(self, request, *args, **kwargs):
        user = Account.objects.filter(id=self.kwargs['pk'])[0]
        serializer = AccountSerializer(data=request.data, instance=user, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if 'password' in request.data:
                user.set_password(request.data['password'])
            user.save()
            return Response(AccountSerializer(user).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
    password = serializers.CharField(max_length=30, required=False)


class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        return LoginSerializer

    # noinspection PyTypeChecker
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        is_simulator = data.get('is_simulator', None)

        if not request.user.is_anonymous():
            account = request.user
        else:
            account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)
                serialized = AccountSerializer(account)

                military_data = MilitaryGradeSerializer(
                    MilitaryGrade.objects.filter(id=serialized.data['military_grade']), many=True)
                city_data = CitySerializer(City.objects.filter(id=serialized.data['city']), many=True)
                user_type_data = UserTypeSerializer(UserType.objects.filter(id=serialized.data['user_type']), many=True)

                user_info = serialized.data
                if len(military_data.data) > 0:
                    user_info['military_grade'] = military_data.data[0]
                else:
                    user_info['military_grade'] = military_data.data

                if len(city_data.data) > 0:
                    user_info['city'] = city_data.data[0]
                else:
                    user_info['city'] = city_data.data

                if len(user_type_data.data) > 0:
                    user_info['user_type'] = user_type_data.data[0]
                else:
                    user_info['user_type'] = user_type_data.data

                user_info['image'] = settings.GET_API_URL(request, user_info['image'])

                if is_simulator is None:
                    return Response({
                        'token': token[0].key,
                        'user': user_info,
                    })
                else:
                    today = datetime.datetime.today()
                    from simulador.resources.program_practice import ProgramPractice
                    objects_practice = ProgramPractice.objects.filter(end__gte=today, start__lte=today)
                    from simulador.resources.program_practice import ProgramPracticeDetailSerializer
                    practice_data = ProgramPracticeDetailSerializer(objects_practice, many=True)
                    return Response({
                        'token': token[0].key,
                        'user': user_info,
                        'practice': practice_data.data
                    })

            return Response(
                {
                    'detail': strings.UNAUTHORIZED
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'detail': strings.INVALID_CREDENTIALS}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': strings.LOGOUT_MESSAGE}, status=status.HTTP_200_OK)
