from django.urls import path

from welcome import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('analyse', views.analyse, name='analyse'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('details/<int:id>/', views.details, name='details')
]