1. Diseño del Pipeline(End-to-End)
   Opte por un enfoque ELT para aprovechar la capacidad de procesamiento de Redshift.

   Flujo general
   1. Extraccion e ingesta: Un DAG en airflow monitorea la llegada de archvos CSV en S3.
   2. Staging: Los datos de cargan en una tabla temporal usando en comando CoPY para maximizar la velocidad.
   3. Transformacion y Upersert: Se ejecuta una logica de Upersert hacia la tabla final para integrar nuevos registros y aplixar correciones de hasta 7 dias.

   Estrategia de carga e idemponencia
    * Decidi hacerlo con una carga incremental dado el crecimiento proyectado, ya que con un full load quedaria ineficiente.
    * Idemponencia: El pipeline es re-procesable. si se ejecuta el mismo proceso , el resultado en la tabla final no varia, ya que se eliminan los regidtros previo del mismo antes de insertar la nueva version.
    * Validaciones: Se implementan chequeos de calidad(nulos, montos negativos) y alertas automaticas via airflow ante fallas de sensores o carga.

2. Manejo de escenarios operativos
   * Retraso de archivos: el S3KeySensor espera el archivo por un tiempo determinado antes de fallar y alertar.
   * Contenido duplicado: La logica del UPsert asegura que la version mas reciente prevalezca.
   * Evolucion del esquema: Se recomienda el uso de tipos SUPER o validaciones de esquema previas al COPY para evitar rupturas por nuevas columnas.
   * Escalabilidad: EL diseño utiliza Dist Keys y Sort Keys en Redshift para mantener el rendimiento ante el aumento de volumen.
   * Discrepancia de datos: Se propone  un proceso de conciliacion comparando sumas de AMOUNT entre origen y destino para diagnosticar fugas.

3. Modelado y SQL
   * Sort Key(created_at): La elegi para optimizar las consultas de finanzas ya que suelen filtrar por rangos de frechas.
   * Dist Key(user_id): Elegida para optmizar futuros JOINS con dimensiones de usuarios y distribuir la carga uniormemente.
     Nota: La estructura de la tabla y las queries de deteccion se encuentran en la carpeta /sql de este repositorio.

4. Reflecion y Trade-offs
   * Trade-offs asumidos: Priorice la consistencia de datos y la integridad sobre la simplicidad extrema del codigo. Implementar un Upsert es mas complejo que un Append,
     pero es necesario para manejar las correciones de 7 dias.
   * Dudas del diseño: El manejo exaco de los archivosque llegan mas de una vez; se asume que el sistema transaccional envia la verdad absoluta en el archivo mas reciente.
   * Refuerzo para cierre contable: Si el pipeline fuera critico, anadiria una capa de data quiality estricta y un proceso de "Loching" de datos historicos para evitar modoficaciones una vez cerrado el mes.
