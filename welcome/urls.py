from django.urls import path

from welcome import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('put-media', views.put_media, name='put-media'),
    path('search', views.search, name='search')
]