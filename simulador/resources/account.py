from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    AnonymousUser)
from rest_framework import viewsets, views, serializers, status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from simulador.resources.people import People, PeopleSerializer
from simulador import strings


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    image = models.ImageField(upload_to="People/images/", default='')
    phone_number = models.CharField(max_length=10, blank=True)

    info = models.ForeignKey(People, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.username])

    def get_short_name(self):
        return self.first_name

    def is_admin_user(self):
        return self.is_admin


class AccountSerializer(serializers.ModelSerializer):
    # info = PeopleSerializer(read_only=True)

    class Meta:
        model = Account

        fields = (
            'is_admin', 'is_staff', 'is_superuser', 'id', 'is_active', 'username', 'email', 'image', 'phone_number',
            'info', 'password')

    def create(self, validated_data):
        request = self.context.get('request', None)

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)

        instance.save()

        return instance


class AccountDetailSerializer(serializers.ModelSerializer):
    info = PeopleSerializer(read_only=True)

    class Meta:
        model = Account

        fields = (
            'id', 'username', 'email', 'image', 'phone_number',
            'info', 'password')


class AccountDetailViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


class AccountViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminUser,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
    password = serializers.CharField(max_length=30, required=False)


class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        return LoginSerializer

    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if not request.user.is_anonymous():
            account = request.user
        else:
            account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)
                serialized = AccountSerializer(account)
                return Response({
                    'token': token[0].key,
                    'user': serialized.data
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
