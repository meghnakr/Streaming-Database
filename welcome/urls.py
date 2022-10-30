from django.urls import path

from welcome import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('edit', views.edit, name='edit'),
]