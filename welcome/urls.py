from django.urls import path

from welcome import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('edit', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('analyse', views.analyse, name='analyse'),
]