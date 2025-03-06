from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from ChillarWeb.views import inicio, comentarioCliente, proyectosInd, servicioInd

urlpatterns = [
    path('', inicio),
    path('comentario/', comentarioCliente),
    path('proyectos/', proyectosInd),
    path('servicios/', servicioInd),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)