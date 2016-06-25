# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('ci', models.CharField(help_text=b'Ejem. 9981765', unique=True, max_length=10)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('email', models.EmailField(max_length=254, unique=True, null=True, blank=True)),
                ('image', models.ImageField(default=b'', upload_to=b'People/images/')),
                ('phone_number', models.CharField(max_length=10, blank=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Masculino'), (b'F', b'Femenino')])),
                ('first_name', models.CharField(help_text=b'Ejem. Juan', max_length=20)),
                ('last_name', models.CharField(help_text=b'Ejem. Peres', max_length=20, null=True, blank=True)),
                ('date_of_birth', models.DateField(help_text=b'Ejem. 12/03/1993', null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Battalion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('short', models.CharField(unique=True, max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instructor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CustomPractices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_practice', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('practicing', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('short', models.CharField(unique=True, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ImageRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('image', models.ImageField(upload_to=b'ImageRepository/')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MilitaryGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('short', models.CharField(unique=True, max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Masculino'), (b'F', b'Femenino')])),
                ('ci', models.CharField(help_text=b'Ejem. 9981765', max_length=10, unique=True, null=True, blank=True)),
                ('first_name', models.CharField(help_text=b'Ejem. Juan', max_length=20)),
                ('last_name', models.CharField(help_text=b'Ejem. Peres', max_length=20, null=True, blank=True)),
                ('date_of_birth', models.DateField(help_text=b'Ejem. 12/03/1993', null=True, blank=True)),
                ('country', models.CharField(help_text=b'Ejem. Bolivia', max_length=20, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'Profile/', blank=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('city', models.ForeignKey(help_text=b'Id: Ejem. 1', to='simulador.City')),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Practices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_practice', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('practicing', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProgramPractice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=40)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('is_evaluation', models.BooleanField(default=False)),
                ('is_test_mode', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('finish', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('instructor', models.ForeignKey(related_name='instructor', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ManyToManyField(to='simulador.Lesson')),
                ('list', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Regiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ReportRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('file', models.FileField(upload_to=b'ReportRepository/')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(to='simulador.ImageRepository')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_expired', models.DateTimeField()),
                ('token_reset', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(to='simulador.Lesson')),
                ('position', models.ForeignKey(to='simulador.Position')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ResultsZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zone', models.IntegerField()),
                ('time', models.IntegerField()),
                ('score', models.IntegerField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Squadron',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='simulador.Company')),
                ('list', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'fdsf', unique=True, max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('zones', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TypeOfFire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('distance', models.FloatField()),
                ('selector', models.CharField(max_length=30, null=True, blank=True)),
                ('chargers', models.IntegerField()),
                ('cartridges', models.IntegerField()),
                ('modality', models.TextField(max_length=100, null=True, blank=True)),
                ('max_time', models.IntegerField()),
                ('min_score', models.IntegerField()),
                ('max_score', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.ForeignKey(to='simulador.Position')),
                ('target', models.ForeignKey(to='simulador.Target')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('short', models.CharField(unique=True, max_length=10)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='results',
            name='results_zone',
            field=models.ManyToManyField(to='simulador.ResultsZone'),
        ),
        migrations.AddField(
            model_name='results',
            name='type_of_fire',
            field=models.ForeignKey(to='simulador.TypeOfFire'),
        ),
        migrations.AddField(
            model_name='practices',
            name='program_practice',
            field=models.ForeignKey(to='simulador.ProgramPractice'),
        ),
        migrations.AddField(
            model_name='practices',
            name='results',
            field=models.ManyToManyField(help_text=b'\n                                        [\n                                            {\n                                                "lesson":1,\n                                                "type_of_fire":1,\n                                                "position":2,\n                                                "results_zone":[\n                                                    {\n                                                        "zone": 10,\n                                                        "time": 3000,\n                                                        "score": 10\n                                                    },\n                                                    {\n                                                        "zone": 3,\n                                                        "time": 3000,\n                                                        "score": 3\n                                                    }\n                                                ]\n                                            },\n                                            {\n                                                "lesson":1,\n                                                "type_of_fire":2,\n                                                "position":2,\n                                                "results_zone":[\n                                                    {\n                                                        "zone": 5,\n                                                        "time": 3000,\n                                                        "score": 10\n                                                    },\n                                                    {\n                                                        "zone": 5,\n                                                        "time": 3000,\n                                                        "score": 5\n                                                    }\n                                                ]\n                                            }\n                                        ]\n                                    ', to='simulador.Results'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='type_of_fire',
            field=models.ManyToManyField(to='simulador.TypeOfFire'),
        ),
        migrations.AddField(
            model_name='custompractices',
            name='results',
            field=models.ManyToManyField(help_text=b'\n                                        [\n                                            {\n                                                "lesson":1,\n                                                "type_of_fire":1,\n                                                "position":2,\n                                                "results_zone":[\n                                                    {\n                                                        "zone": 10,\n                                                        "time": 3000,\n                                                        "score": 10\n                                                    },\n                                                    {\n                                                        "zone": 3,\n                                                        "time": 3000,\n                                                        "score": 3\n                                                    }\n                                                ]\n                                            },\n                                            {\n                                                "lesson":1,\n                                                "type_of_fire":2,\n                                                "position":2,\n                                                "results_zone":[\n                                                    {\n                                                        "zone": 5,\n                                                        "time": 3000,\n                                                        "score": 10\n                                                    },\n                                                    {\n                                                        "zone": 5,\n                                                        "time": 3000,\n                                                        "score": 5\n                                                    }\n                                                ]\n                                            }\n                                        ]\n                                    ', to='simulador.Results'),
        ),
        migrations.AddField(
            model_name='battalion',
            name='regiment',
            field=models.ForeignKey(to='simulador.Regiment'),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.ForeignKey(help_text=b'Id: Ejem. 1', to='simulador.City'),
        ),
        migrations.AddField(
            model_name='account',
            name='military_grade',
            field=models.ForeignKey(to='simulador.MilitaryGrade'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_type',
            field=models.ForeignKey(to='simulador.UserType'),
        ),
    ]
