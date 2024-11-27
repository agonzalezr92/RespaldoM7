from django.db import models

# from django.contrib.auth.models import AbstractUser #User

from django.contrib.auth.models import User


import uuid

# Create your models here.
# class Inmueble(models.Model):
#    nombre = models.CharField(max_length=200)
#    descripcion = models.TextField()
#    m2_construidos = models.FloatField()
#    m2_totales = models.FloatField()
#    estacionamientos = models.IntegerField()
#    habitaciones = models.IntegerField()
#    banos = models.IntegerField()
#    direccion = models.CharField(max_length=200)
#    comuna = models.CharField(max_length=100)
#    tipo_inmueble = models.CharField(max_length=50)
#    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)

# def __str__(self):
#    return self.nombre


class Pais(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID como clave primaria
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"


class EstadoProvincia(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID como clave primaria
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nombre}, {self.pais.nombre}"


class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID como clave primaria
    nombre = models.CharField(max_length=150)
    estado_provincia = models.ForeignKey(EstadoProvincia, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nombre}, {self.estado_provincia.nombre}"


class TipoInmueble(models.Model):
    # TIPOS_INMUEBLE = (
    #     ('casa', 'casa'),
    #     ('departamento', 'departamento'),
    #     ('parcela', 'parcela')
    #     )
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre}"


class Inmueble(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = (
        models.TextField()
    )  # Cambiado a TextField para permitir descripciones más largas
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField()
    n_estacionamientos = models.IntegerField()
    n_habitaciones = models.IntegerField()
    n_baños = models.IntegerField()
    precio = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Cambio a DecimalField para mayor precisión
    moneda = models.CharField(
        max_length=3,default="USD"
    )  # ISO 4217 currency code, e.g., 'USD', 'EUR'
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    ciudad = models.ForeignKey(
        to=Ciudad, on_delete=models.PROTECT
    )  # Referencia como string
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    latitud = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )  # los agregue con el fin de usar eventualmente googlemaps para ubicacion
    longitud = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )  # los agregue con el fin de usar eventualmente googlemaps para ubicacion
    disponible = models.BooleanField(default=True)
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.PROTECT)
    propietario = models.ForeignKey(
        User,null=False, blank=False,default="1",
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return f"{self.nombre} - {self.calle}"


class ImagenInmueble(models.Model):
    propiedad = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="propiedades/")


class TipoUsuario(models.Model):
    TIPOS_USUARIO = (
        # ("0", "Nulo"),
        ("1", "Arrendador"),
        ("2", "Arrendatario"),
        # ("3", "Administrador"),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default="Nulo")

    def __str__(self):
        return self.get_tipo_display()


# class Usuario(AbstractUser):
#    id_nacional = models.CharField(
#        max_length=20, unique=True
#    )  # Identificador más general
#    nombre = models.CharField(max_length=50, default="")
#    estado = models.BooleanField(default=True)
#    apellido_paterno = models.CharField(max_length=50, default="")
#    apellido_materno = models.CharField(max_length=50, default="")
#    correo_electronico = models.EmailField(unique=True, null=True, blank=True)
#    direccion = models.CharField(max_length=150)
#    telefono = models.CharField(
#        max_length=15, unique=True
#    )  # Aumentado a 15 para números internacionales
#    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

#    #def str(self):
#    #    return f"[{self.id_nacional}]"
#    def __str__(self):
#        return f"{self.nombre} {self.apellido_paterno}"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil"
    )  # Relación uno a uno con User
    telefono = models.CharField(
        max_length=15, unique=False, blank=True, null=True
    )  # Campo adicional
    direccion = models.CharField(
        max_length=150, blank=True, null=True
    )  # Campo adicional
    id_nacional = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )  # Identificador adicional
    tipo_usuario = models.ForeignKey(
        TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"


#class UsuarioInmueble(models.Model):
#    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
#    inmueble = models.ForeignKey(Inmueble, on_delete=models.PROTECT)
#    fecha_inicio = models.DateField(null=True, blank=True)
#    fecha_fin = models.DateField(null=True, blank=True)

#    def __str__(self):
#        return f"{self.usuario.id_nacional} - {self.inmueble.nombre}"


class Solicitud(models.Model):
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, default="en espera")

    def __str__(self):
        return f"{self.usuario.id_nacional} - {self.inmueble.nombre}"


class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=64)
    customer_email = models.EmailField()
    message = models.TextField()
