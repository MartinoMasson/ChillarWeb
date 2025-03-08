from django.db import models

class Desarrollador(models.Model):
    dni=models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    trabajo = models.CharField(max_length=50)
    descripcion = models.TextField()
    linkedin = models.CharField(max_length=150)
    github = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
class Pagina(models.Model):
    Titulo = [
        ('Inicio', 'Inicio'),
        ('Servicios', 'Servicios'),
        ('Portafolio', 'Portafolio'),
        ('Equipo', 'Equipo'),
        ('Servicios', 'Servicio'),
    ]
    titulo = models.CharField(max_length=255, choices=Titulo, primary_key=True)
    texto = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Servicio(models.Model):
    id_servicio=models.AutoField(primary_key=True, auto_created=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=500,null=True, blank=True)
    costo=models.IntegerField()
    
    def __str__(self):
        return  self.nombre
    
class Caracteristicas(models.Model):
    id_servicio=models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='caracteristicas')
    caracteristica=models.CharField(max_length=500)

class Proyecto(models.Model):
    email=models.EmailField(primary_key=True)
    name=models.CharField(max_length=50)
    descripcion=models.TextField(max_length=500)
    imagen = models.ImageField(upload_to='proyecto/', null=True, blank=True)
    url = models.URLField(max_length=500)
    creacion=models.DateField(("Creacion"), auto_now=True)
    servicio=models.ForeignKey(Servicio, on_delete=models.CASCADE)
    desarrollador=models.ForeignKey(Desarrollador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('email', 'name')

    def __str__(self):
        return self.name
    
class Cliente(models.Model):
    name=models.CharField(max_length=100)
    email=models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    comentario=models.CharField(max_length=500)