from django.contrib import admin
from .models import Gateway, Node, NodeSetup, Hist, Evento

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('name','address','online')

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name','online')

@admin.register(NodeSetup)
class NodeSetupAdmin(admin.ModelAdmin):
    list_display = ('node','address','nodeId',)

@admin.register(Hist)
class HistAdmin(admin.ModelAdmin):
    list_display = ('node','date')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('node','date','tipo','descricao')
