from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.biscuit_list,
        name='biscuit_list'
    ),

    path(
        '<int:id>/',
        views.biscuit_detail,
        name='biscuit_detail'
    ),

]