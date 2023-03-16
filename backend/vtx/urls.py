from django.urls import path
from .views import IndexView, online, nodes, Filtra, Eventos

urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    path('filtra/',Filtra.as_view(),name="filtra"),
    path('eventos/',Eventos.as_view(),name="eventos"),
    path('online/',online,name="online"),
    path('nodes/',nodes,name="nodes"),
]