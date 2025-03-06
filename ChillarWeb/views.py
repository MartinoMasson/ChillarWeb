from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from ChillarWeb.forms import FormContacto,FormComentario
from ChillarWeb.models import Servicio,Caracteristicas,Cliente,Proyecto
from ChillarWeb.models import Cliente

def proyectos(request):
    proy={}
    proy['proyectos'] = Proyecto.objects.all().order_by('?')[:3]
    proy['leng'] = Proyecto.objects.count()
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

def inicio(req):
    clientes=cliente(req)
    if not clientes:
        if req.method == 'POST':
            rtaForm = FormComentario(req.POST)
            
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
            
        return render(req, 'comentarioCliente.html', {
            'formContacto': contacto(req),
            'planes':servicio(req),
            'clientes':cliente(req),
            'proyectos':proyectos(req),
            'formCli':rtaForm
        })
    return render(req, 'inicio.html', {
        'formContacto': contacto(req),
        'planes':servicio(req),
        'clientes':clientes,
        'proyectos':proyectos(req),
    })


def proyectosInd(request):
    proy = Proyecto.objects.all().order_by('name')
    
    return render(request, 'Individuales/proyectos.html', {'proyectos':proy})

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
