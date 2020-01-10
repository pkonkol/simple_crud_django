from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('edit/<int:osoba_id>/', views.edit_view, name='edit'),
    path('add/', views.add_view, name='add'),
    path('delete/<int:osoba_id>/', views.delete_view, name='delete'),
    path('search/', views.search_view, name='search'),
]
