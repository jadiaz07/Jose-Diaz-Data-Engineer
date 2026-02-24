from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from scripts.schema_validator import validate_csv_columns

REQUIRED_COLS = ['order_id', 'user_id', 'amount', 'currency', 'status', 'created_at', 'updated_at']

default_args = {
    'owner': 'longevo_de',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'sales_ingestion_pipeline',
    default_args=default_args,
    description='Pipeline incremental con manejo de correcciones de 7 días',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # 1. Esperar archivo (Maneja retrasos)
    wait_for_file = S3KeySensor(
        task_id='wait_for_s3_file',
        bucket_name='longevo-data',
        bucket_key='inbound/sales_{{ ds }}.csv',
        timeout=60 * 60 * 3 # 3 horas de espera
    )

    # 2. Validar esquema (Maneja nuevas columnas)
    check_schema = PythonOperator(
        task_id='validate_schema',
        python_callable=validate_csv_columns,
        op_kwargs={
            'bucket': 'longevo-data',
            'key': 'inbound/sales_{{ ds }}.csv',
            'expected_cols': REQUIRED_COLS
        }
    )

    # 3. Carga a Staging (Incremental e Idempotente)
    load_to_staging = S3ToRedshiftOperator(
        task_id='s3_to_redshift_staging',
        schema='staging',
        table='stg_sales',
        s3_bucket='longevo-data',
        s3_key='inbound/sales_{{ ds }}.csv',
        copy_options=['csv', 'ignoreheader 1', 'timeformat "auto"'],
        method='REPLACE' # Trunca staging antes de cargar
    )

    # 4. Upsert (Maneja duplicados y correcciones de 7 días)
    upsert_final = SQLExecuteQueryOperator(
        task_id='upsert_to_final_table',
        conn_id='redshift_default',
        sql="""
            BEGIN;
            -- Eliminar registros que ya existen para actualizarlos
            DELETE FROM public.fact_sales 
            WHERE order_id IN (SELECT order_id FROM staging.stg_sales);
            
            -- Insertar nueva versión de los datos
            INSERT INTO public.fact_sales 
            SELECT * FROM staging.stg_sales;
            COMMIT;
        """
    )

    wait_for_file >> check_schema >> load_to_staging >> upsert_final
