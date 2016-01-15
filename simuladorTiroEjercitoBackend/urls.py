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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from simulador.resources.account import LoginView, AccountViewSet
from simulador.resources.account import LogoutView
from simulador.resources.battalion import BattalionViewSet
from simulador.resources.city import CityViewSet
from simulador.resources.company import CompanyViewSet
from simulador.resources.grade import GradeViewSet
from simulador.resources.military_grade import MilitaryGradeViewSet
from simulador.resources.people import PeopleViewSet
from simulador.resources.regiment import RegimentViewSet
from simulador.resources.squadron import SquadronViewSet

router = routers.DefaultRouter()

router.register(r'Account', AccountViewSet)
router.register(r'Battalion', BattalionViewSet)
router.register(r'City', CityViewSet)
router.register(r'Company', CompanyViewSet)
router.register(r'Grade', GradeViewSet)
router.register(r'MilitaryGrade', MilitaryGradeViewSet)
router.register(r'People', PeopleViewSet)
router.register(r'Regiment', RegimentViewSet)
router.register(r'Squadron', SquadronViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^Login/', LoginView.as_view(), name="login"),
    url(r'^Logout/', LogoutView.as_view(), name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
