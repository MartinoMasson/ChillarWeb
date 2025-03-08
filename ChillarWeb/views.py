from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from ChillarWeb.forms import FormContacto,FormComentario
from ChillarWeb.models import Servicio,Caracteristicas,Cliente,Proyecto, Pagina, Desarrollador

def proyectos(request):
    proy={}
    proy['proyectos'] = Proyecto.objects.all().order_by('?')[:3]
    proy['leng'] = Proyecto.objects.count()
    texto = Pagina.objects.filter(titulo='Portafolio')
    proy['titulo'] = {
        "texto": texto[0].texto,
        "descripcion": texto[0].descripcion if texto[0].descripcion else '',
        "imagen": texto[0].imagen.url if texto[0].imagen else None
    }
    return proy

def cliente(request):
    clientes = Cliente.objects.all().order_by('?')[:3]
    
    return clientes

def servicio(request):
    servicio = request.GET.get('servicio', '')  # Obtener el valor de 'servicio' de la URL
    
    if servicio:
        servicios=Servicio.objects.filter(nombre__icontains=servicio)    
    else:
        servicios=Servicio.objects.filter(nombre__icontains='local')
    
    # Para cada servicio, obtener las características correspondientes
    for ser in servicios:
        ser.caracteristica = Caracteristicas.objects.filter(id_servicio= ser.id_servicio)

    return servicios            

def contacto(request):
    
    if request.method=='POST':
        rtaForm = FormContacto(request.POST)
        
        if rtaForm.is_valid():
            infForm = rtaForm.cleaned_data
            
            mensaje=infForm['nombre'] + ' ' + infForm['apellido'] + '\n\n' + infForm['mensaje'] + '\n\n\nContacto \nEmail: ' + infForm['email'] + '\nTelefono: ' + infForm['telefono']
            recipient_list = ['martinomasson2@gmail.com']
            
            send_mail(infForm['asunto'], mensaje, infForm['email'], recipient_list, fail_silently=False)    
            
            return render(request, 'gracias.html')
        
    else:
        rtaForm=FormContacto()
        
        
    return rtaForm

def equipo(request):
    equipo={}
    equipo['equipo'] = Desarrollador.objects.all().order_by('?')[:3]
    texto = Pagina.objects.filter(titulo='Equipo')
    equipo['titulo'] = {
        "texto": texto[0].texto,
        "descripcion": texto[0].descripcion if texto[0].descripcion else '',
        "imagen": texto[0].imagen.url if texto[0].imagen else None 
    }
    return equipo

def inicio(req):
    # Consultar las páginas 'Inicio' y 'Servicios'
    inicio_data = Pagina.objects.filter(titulo='Inicio')

    inicio = {
        "texto": inicio_data[0].texto,
        "descripcion": inicio_data[0].descripcion if inicio_data[0].descripcion else '',
        "imagen": inicio_data[0].imagen.url if inicio_data[0].imagen else None 
    }

    servicios_data = Pagina.objects.filter(titulo='Servicios')
    servicios = {
        "texto": servicios_data[0].texto,
        "descripcion": servicios_data[0].descripcion if servicios_data[0].descripcion else '',
        "imagen": servicios_data[0].imagen.url if servicios_data[0].imagen else None
    }

    clientes = cliente(req)

    # Si no hay clientes
    if not clientes:
        if req.method == 'POST':
            # Crear el formulario de comentarios
            rtaForm = FormComentario(req.POST)
            
            if rtaForm.is_valid():
                infForm = rtaForm.cleaned_data
                
                nombre_completo = infForm['nombre_completo']
                email = infForm['email']
                comentario = infForm['comentario']
                
                try:
                    # Obtener el proyecto relacionado con el email
                    proyecto = Proyecto.objects.get(email=email)
                except Proyecto.DoesNotExist:
                    # Si no se encuentra el proyecto, redirigir
                    return redirect('/#testimonials')

                # Crear el cliente asociado con el proyecto encontrado
                Cliente.objects.create(
                    name=nombre_completo,
                    email=proyecto.email,  # Asignar el email del proyecto
                    comentario=comentario
                )
                return redirect('/#testimonials')  # Redirigir después de crear el cliente
            
        else:
            rtaForm = FormComentario()  # Si no es POST, mostrar el formulario vacío

        # Renderizar la página de comentarios del cliente
        return render(req, 'inicio.html', {
            'inicio': inicio,
            'servicios': servicios,
            'formContacto': contacto(req),
            'planes': servicio(req),
            'clientes': clientes,
            'proyectos': proyectos(req),
            'equipo': equipo(req),
            'formCli': rtaForm  # El formulario de comentarios
        })
    
    # Si hay clientes, renderizar la página de inicio
    return render(req, 'inicio.html', {
        'inicio': inicio,
        'servicios': servicios,
        'formContacto': contacto(req),
        'planes': servicio(req),
        'clientes': clientes,
        'proyectos': proyectos(req),
        'equipo': equipo(req),
    })
    
def proyectosInd(request):
    proy = Proyecto.objects.all().order_by('name')
    texto = Pagina.objects.filter(titulo='Portafolio')
    titulo = {
        "texto": texto[0].texto,
        "descripcion": texto[0].descripcion if texto[0].descripcion else '',
        "imagen": texto[0].imagen.url if texto[0].imagen else None
    }
    return render(request, 'Individuales/proyectos.html', {'proyectos':proy, 'titulo':titulo})

def servicioInd(request):
    servicio = request.GET.get('servicio', '')  # Obtener el valor de 'servicio' de la URL
    
    if servicio:
        servicios=Servicio.objects.filter(nombre__icontains=servicio)    
    else:
        servicios = Servicio.objects.all().order_by('id_servicio')
    
    # Para cada servicio, obtener las características correspondientes
    for ser in servicios:
        ser.caracteristica = Caracteristicas.objects.filter(id_servicio= ser.id_servicio)

    return render(request, 'Individuales/servicios.html', {'planes':servicios})            


def comentarioCliente(request):    
    if request.method == 'POST':
        rtaForm = FormComentario(request.POST)
        
        if rtaForm.is_valid():
            infForm = rtaForm.cleaned_data
            
            nombre_completo = infForm['nombre_completo']
            email = infForm['email']
            comentario = infForm['comentario']
            
            # Obtener el objeto Proyecto correspondiente al email
            try:
                proyecto = Proyecto.objects.get(email=email)
            except Proyecto.DoesNotExist:
                # Si no se encuentra el proyecto, puedes manejar el error de alguna manera
                return redirect('/#testimonials')  # O mostrar un mensaje de error

            # Crear el cliente con el proyecto encontrado
            Cliente.objects.create(
                name=nombre_completo,
                email=proyecto,  # Asignar el objeto Proyecto
                comentario=comentario
            )
            return redirect('/#testimonials')
            
    else:
        rtaForm = FormComentario()
        
    return render(request, 'comentarioCliente.html', {
        'formContacto': contacto(request),
        'planes':servicio(request),
        'clientes':cliente(request),
        'proyectos':proyectos(request),
        'formCli':rtaForm
    })
