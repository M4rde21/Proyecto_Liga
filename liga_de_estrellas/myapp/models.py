from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

class Entrenador(models.Model):
    nombre_entrenador = models.CharField(max_length=100)
    apellido_entrenador = models.CharField(max_length=100)
    dni_entrenador = models.CharField(unique=True, max_length=20)
    fecha_nac_entrenador = models.DateField()
    foto_entrenador = models.ImageField(upload_to="fotos_jugador/", blank=True, null=True)
    
class Equipo(models.Model):
    nombre_equipo = models.CharField(max_length=100)
    logo_equipo = models.ImageField(upload_to="logos/", blank=True, null=True)
    foto_equipo = models.ImageField(upload_to="fotos_equipo/", blank=True, null=True)
    
    def __str__(self):
        return self.nombre_equipo
    
class Jugador(models.Model):
    nombre_jugador = models.CharField(max_length=100)
    apellido_jugador = models.CharField(max_length=100)
    dni_jugador = models.CharField(unique=True, max_length=20)
    fecha_nac_jugador = models.DateField()
    foto_jugador = models.ImageField(upload_to="fotos_jugador/", blank=True, null=True)
    activo_jugador = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_jugador + ' ' + self.apellido_jugador
    
class Predio(models.Model):
    nombre_predio = models.CharField(max_length=100)
    
class PremiosGrupal(models.Model):
    nombre_premio_grupal = models.CharField(max_length=100)
    foto_premio_grupal = models.ImageField(upload_to="premio_grupal/", blank=True, null=True)
    
class PremiosIndividual(models.Model):
    nombre_premio_individual = models.CharField(max_length=100)
    foto_premio_individual = models.ImageField(upload_to="premio_individual/", blank=True, null=True)
    
class TipoTorneo(models.Model):
    nombre_tipo_torneo = models.CharField(max_length=100)
    
class EquipoXEntrenador(models.Model):
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo', blank=True, null=True)
    id_entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, db_column='id_entrenador', blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'equipos_x_entrenadores'
        
class Torneo(models.Model):
    nombre_torneo = models.CharField(max_length=100)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria', blank=True, null=True)
    id_tipo_torneo = models.ForeignKey(TipoTorneo, on_delete=models.CASCADE, db_column='id_tipo_torneo', blank=True, null=True)
    año = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'torneos'
        
        
class Traspaso(models.Model):
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador', blank=True, null=True)
    id_equipo_actual = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo_actual', blank=True, null=True)
    id_equipo_nuevo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo_nuevo', related_name='traspasos_id_equipo_nuevo_set', blank=True, null=True)
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo', blank=True, null=True)
    fecha_transferencia = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'traspasos'
        
        
class Temporada(models.Model):
    nombre_temporada = models.CharField(max_length=100)
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo', blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'temporadas'



class PremioEquipo(models.Model):
    id_premio_grupal = models.ForeignKey(PremiosGrupal, on_delete=models.CASCADE, db_column='id_premio_grupal', blank=True, null=True)
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo', blank=True, null=True)

    class Meta:
        db_table = 'premios_equipos'


class PremioJugador(models.Model):
    id_premio_individual = models.ForeignKey(PremiosIndividual, on_delete=models.CASCADE, db_column='id_premio_individual', blank=True, null=True)
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador', blank=True, null=True)

    class Meta:
        db_table = 'premios_jugadores'


class Fecha(models.Model):
    nombre_fecha = models.CharField(max_length=100)
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)
    

    class Meta:
        db_table = 'fechas'

    
class Grupo(models.Model):
    nombre_grupo = models.CharField(max_length=100)
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)

    class Meta:
        db_table = 'grupos'


class Partido(models.Model):
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo', blank=True, null=True)
    id_fecha = models.ForeignKey(Fecha, on_delete=models.CASCADE, db_column='id_fecha', blank=True, null=True)
    id_equipo_1 = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo_1', blank=True, null=True)
    id_equipo_2 = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo_2', related_name='partidos_id_equipo_2_set', blank=True, null=True)
    id_predio = models.ForeignKey(Predio, on_delete=models.CASCADE, db_column='id_predio', blank=True, null=True)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo', blank=True, null=True)
    fecha_partido = models.DateField(blank=True, null=True)
    hora_partido = models.TimeField(blank=True, null=True)
    destacado = models.BooleanField(blank=True, default=False)

    class Meta:
        db_table = 'partidos'
        
        
class Figura(models.Model):
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador', blank=True, null=True)

    class Meta:
        db_table = 'figuras'
        
        
class Planilla(models.Model):
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador', blank=True, null=True)
    goles = models.IntegerField(blank=True, null=True)
    num_camiseta = models.IntegerField(blank=True, null=True)
    participo = models.BooleanField(blank=True, default=False)

    class Meta:
        db_table = 'planillas'
        
        
class Resultado(models.Model):
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido', blank=True, null=True)
    goles_equipo_1 = models.IntegerField(blank=True, null=True)
    goles_equipo_2 = models.IntegerField(blank=True, null=True)
    penales = models.BooleanField(blank=True, default=False)
    penales_equipo_1 = models.IntegerField(blank=True, null=True)
    penales_equipo_2 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'resultados'
        

class TablaDePosicion(models.Model):
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada', blank=True, null=True)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo', blank=True, null=True)
    puntos = models.IntegerField(blank=True, null=True)
    partidos_jugados = models.IntegerField(blank=True, null=True)
    partidos_ganados = models.IntegerField(blank=True, null=True)
    partidos_empatados = models.IntegerField(blank=True, null=True)
    partidos_perdidos = models.IntegerField(blank=True, null=True)
    goles_a_favor = models.IntegerField(blank=True, null=True)
    goles_en_contra = models.IntegerField(blank=True, null=True)
    diferencia_goles = models.IntegerField(blank=True, null=True)
    tarjetas_amarillas = models.IntegerField(blank=True, null=True)
    tarjetas_rojas = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tabla_de_posiciones'
        

class Tarjeta(models.Model):
    id_partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido')
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador')
    tipo_tarjeta = models.CharField(max_length=8)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tarjetas'
        
        
class TemporadaXTorneoXEquipoXJugador(models.Model):
    id_temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, db_column='id_temporada')
    id_torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, db_column='id_torneo')
    id_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='id_equipo')
    id_jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='id_jugador')

    class Meta:
        db_table = 'temporadas_x_torneos_x_equipos_x_jugadores'

