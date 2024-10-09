# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categorias'
    def __str__(self):
        return self.nombre_categoria

class Entrenadores(models.Model):
    id_entrenador = models.AutoField(primary_key=True)
    nombre_entrenador = models.CharField(max_length=100)
    apellido_entrenador = models.CharField(max_length=100)
    dni_entrenador = models.CharField(unique=True, max_length=20)
    fecha_nac_entrenador = models.DateField()
    foto_entrenador = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrenadores'


class Equipos(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(max_length=100)
    logo_equipo = models.TextField(blank=True, null=True)
    foto_equipo = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre_equipo

    class Meta:
        managed = False
        db_table = 'equipos'


class EquiposXEntrenadores(models.Model):
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
    id_entrenador = models.ForeignKey(Entrenadores, models.DO_NOTHING, db_column='id_entrenador', blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos_x_entrenadores'


class Fechas(models.Model):
    id_fecha = models.AutoField(primary_key=True)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    nombre_fecha = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'fechas'


class Figuras(models.Model):
    id_figura = models.AutoField(primary_key=True)
    id_partido = models.ForeignKey('Partidos', models.DO_NOTHING, db_column='id_partido', blank=True, null=True)
    id_jugador = models.ForeignKey('Jugadores', models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'figuras'


class Grupos(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=100)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupos'


class Jugadores(models.Model):
    id_jugador = models.AutoField(primary_key=True)
    nombre_jugador = models.CharField(max_length=100)
    apellido_jugador = models.CharField(max_length=100)
    dni_jugador = models.CharField(unique=True, max_length=20)
    fecha_nac_jugador = models.DateField()
    foto_jugador = models.TextField(blank=True, null=True)
    activo_jugador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jugadores'


class Partidos(models.Model):
    id_partido = models.AutoField(primary_key=True)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey('Torneos', models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    id_fecha = models.ForeignKey(Fechas, models.DO_NOTHING, db_column='id_fecha', blank=True, null=True)
    id_equipo_1 = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo_1', blank=True, null=True)
    id_equipo_2 = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo_2', related_name='partidos_id_equipo_2_set', blank=True, null=True)
    id_predio = models.ForeignKey('Predios', models.DO_NOTHING, db_column='id_predio', blank=True, null=True)
    id_grupo = models.ForeignKey(Grupos, models.DO_NOTHING, db_column='id_grupo', blank=True, null=True)
    fecha_partido = models.DateField(blank=True, null=True)
    hora_partido = models.TimeField(blank=True, null=True)
    destacado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partidos'


class Planillas(models.Model):
    id_planilla = models.AutoField(primary_key=True)
    id_partido = models.ForeignKey(Partidos, models.DO_NOTHING, db_column='id_partido', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugadores, models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)
    goles = models.IntegerField(blank=True, null=True)
    num_camiseta = models.IntegerField(blank=True, null=True)
    participo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planillas'


class Predios(models.Model):
    id_predio = models.AutoField(primary_key=True)
    nombre_predio = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'predios'


class PremiosEquipos(models.Model):
    id_premio_equipo = models.AutoField(primary_key=True)
    id_premio_grupal = models.ForeignKey('PremiosGrupales', models.DO_NOTHING, db_column='id_premio_grupal', blank=True, null=True)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey('Torneos', models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'premios_equipos'


class PremiosGrupales(models.Model):
    id_premio_grupal = models.AutoField(primary_key=True)
    nombre_premio_grupal = models.CharField(max_length=100)
    foto_premio_grupal = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'premios_grupales'


class PremiosIndividuales(models.Model):
    id_premio_individual = models.AutoField(primary_key=True)
    nombre_premio_individual = models.CharField(max_length=100)
    foto_premio_individual = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'premios_individuales'


class PremiosJugadores(models.Model):
    id_premio_jugador = models.AutoField(primary_key=True)
    id_premio_individual = models.ForeignKey(PremiosIndividuales, models.DO_NOTHING, db_column='id_premio_individual', blank=True, null=True)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey('Torneos', models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugadores, models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'premios_jugadores'


class Resultados(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    id_partido = models.ForeignKey(Partidos, models.DO_NOTHING, db_column='id_partido', blank=True, null=True)
    goles_equipo_1 = models.IntegerField(blank=True, null=True)
    goles_equipo_2 = models.IntegerField(blank=True, null=True)
    penales = models.IntegerField(blank=True, null=True)
    penales_equipo_1 = models.IntegerField(blank=True, null=True)
    penales_equipo_2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resultados'


class TablaDePosiciones(models.Model):
    id_tabla = models.AutoField(primary_key=True)
    id_temporada = models.ForeignKey('Temporadas', models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    id_grupo = models.ForeignKey(Grupos, models.DO_NOTHING, db_column='id_grupo', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
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
        managed = False
        db_table = 'tabla_de_posiciones'


class Tarjetas(models.Model):
    id_tarjeta = models.AutoField(primary_key=True)
    id_partido = models.ForeignKey(Partidos, models.DO_NOTHING, db_column='id_partido', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugadores, models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)
    tipo_tarjeta = models.CharField(max_length=8, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjetas'


class Temporadas(models.Model):
    id_temporada = models.AutoField(primary_key=True)
    nombre_temporada = models.CharField(max_length=100)
    id_torneo = models.ForeignKey('Torneos', models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temporadas'


class TemporadasXTorneosXEquiposXJugadores(models.Model):
    id_temporada = models.ForeignKey(Temporadas, models.DO_NOTHING, db_column='id_temporada', blank=True, null=True)
    id_torneo = models.ForeignKey('Torneos', models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
    id_jugador = models.ForeignKey(Jugadores, models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temporadas_x_torneos_x_equipos_x_jugadores'


class TipoTorneos(models.Model):
    id_tipo_torneo = models.AutoField(primary_key=True)
    nombre_tipo_torneo = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_torneos'
    def __str__(self):
        return self.nombre_tipo_torneo

class Torneos(models.Model):
    id_torneo = models.AutoField(primary_key=True)
    nombre_torneo = models.CharField(max_length=100)
    id_categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    id_tipo_torneo = models.ForeignKey(TipoTorneos, models.DO_NOTHING, db_column='id_tipo_torneo', blank=True, null=True)
    año = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'torneos'
    def __str__(self):
        return self.nombre_torneo


class Traspasos(models.Model):
    id_traspaso = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey(Jugadores, models.DO_NOTHING, db_column='id_jugador', blank=True, null=True)
    id_equipo_actual = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo_actual', blank=True, null=True)
    id_equipo_nuevo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo_nuevo', related_name='traspasos_id_equipo_nuevo_set', blank=True, null=True)
    id_torneo = models.ForeignKey(Torneos, models.DO_NOTHING, db_column='id_torneo', blank=True, null=True)
    fecha_transferencia = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traspasos'
