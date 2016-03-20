from django.db import models
from rest_framework import viewsets, views, serializers
from simulador.resources.city import City, CitySerializer

GENDERS_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)


class People(models.Model):
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES)
    ci = models.CharField(max_length=10, help_text='Ejem. 9981765', blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=20, help_text='Ejem. Juan', unique=False)
    last_name = models.CharField(max_length=20, help_text='Ejem. Peres', blank=True, null=True, unique=False)
    date_of_birth = models.DateField(help_text='Ejem. 12/03/1993', blank=True, null=True)
    country = models.CharField(max_length=20, help_text='Ejem. Bolivia', blank=True, null=True)
    city = models.ForeignKey(City, help_text='Id: Ejem. 1')
    image = models.ImageField(upload_to="Profile/", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name']


class PeopleSerializer(serializers.ModelSerializer):
    # city = CitySerializer(read_only=True)

    class Meta:
        model = People
        fields = (
            'id', 'gender', 'ci', 'first_name', 'last_name', 'date_of_birth', 'country', 'city', 'image',
            'created_at', 'updated_at')


class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

