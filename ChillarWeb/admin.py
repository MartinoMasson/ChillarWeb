from django.contrib import admin
from django import forms
from ChillarWeb.models import Servicio,Caracteristicas, Proyecto

admin.site.site_header = 'Power fit'
admin.site.site_title = 'Administrador de Gimnasios'

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'nombre', 'descripcion', 'get_costo')
    list_display_links = ('id_servicio', 'nombre', 'descripcion', 'get_costo')
    search_fields = ('id_servicio', 'nombre')

    def get_costo(self, obj):
        return f"${obj.costo}"  # Precede el valor de costo con un signo de dólar

    get_costo.short_description = 'Costo'  # Cambia el nombre de la columna

class CaracteristicasAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'caracteristica')
    
class ProyectosAdmin(admin.ModelAdmin):
    list_display = ('name','descripcion')

admin.site.register(Servicio,ServicioAdmin)
admin.site.register(Caracteristicas,CaracteristicasAdmin)
admin.site.register(Proyecto,ProyectosAdmin)
