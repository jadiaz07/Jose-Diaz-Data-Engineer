from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

# Argumentos base para el DAG
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'sales_pipeline_s3_to_redshift',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False, # Evita ejecuciones masivas si se activa tarde
    template_searchpath=['/usr/local/airflow/sql'],
) as dag:

    # 1. Esperar a que el archivo CSV llegue a S3 [cite: 8, 18]
    # Se usa un sensor para manejar el retraso del archivo.
    wait_for_csv = S3KeySensor(
        task_id='wait_for_daily_csv',
        bucket_name='longevo-data-lake',
        bucket_key='sales/{{ ds }}/sales_data.csv',
        timeout=60 * 60 * 2, # Espera hasta 2 horas
        poke_interval=60 * 5, # Revisa cada 5 minutos
    )

    # 2. Cargar datos del CSV a la tabla de STAGING en Redshift [cite: 34, 36]
    # Se usa TRUNCATE en staging para asegurar que solo procesamos el archivo actual.
    load_to_staging = S3ToRedshiftOperator(
        task_id='load_csv_to_staging',
        schema='staging',
        table='stg_sales',
        s3_bucket='longevo-data-lake',
        s3_key='sales/{{ ds }}/sales_data.csv',
        copy_options=['csv', 'ignoreheader 1', 'timeformat "auto"'],
        redshift_conn_id='redshift_default',
        method='REPLACE', # Trunca la tabla antes de cargar
    )

    # 3. Lógica de UPSERT para manejar correcciones y duplicados [cite: 38, 39, 41]
    # Se eliminan de la tabla final los IDs que vienen en el archivo nuevo 
    # y luego se insertan los nuevos registros.
    upsert_to_final = SQLExecuteQueryOperator(
        task_id='upsert_into_fact_sales',
        conn_id='redshift_default',
        sql="""
            BEGIN;
            -- Borrar registros existentes para evitar duplicados por order_id [cite: 39]
            DELETE FROM public.fact_sales 
            WHERE order_id IN (SELECT order_id FROM staging.stg_sales);
            
            -- Insertar la nueva versión (incluyendo correcciones de 7 días) 
            INSERT INTO public.fact_sales 
            SELECT * FROM staging.stg_sales;
            COMMIT;
        """,
    )

    # 4. Validación de datos básica [cite: 42]
    # Detectar si se cargaron registros con montos nulos o negativos.
    data_quality_check = SQLExecuteQueryOperator(
        task_id='data_quality_audit',
        conn_id='redshift_default',
        sql="""
            SELECT COUNT(*) 
            FROM public.fact_sales 
            WHERE amount IS NULL OR amount < 0;
        """,
        # Aquí podrías usar un operador de Check para fallar si el resultado > 0
    )

    wait_for_csv >> load_to_staging >> upsert_to_final >> data_quality_check
