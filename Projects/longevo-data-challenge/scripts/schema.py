import boto3
import csv
from airflow.exceptions import AirflowFailException

def validate_csv_schema(bucket_name, file_key, expected_columns):
    """
    Valida el encabezado del CSV en S3 antes de cargar a Redshift.
    """
    s3 = boto3.client('s3')
    # Solo leemos el primer KB para obtener el header (Eficiente para 10x volumen)
    response = s3.get_object(Bucket=bucket_name, Key=file_key, Range='bytes=0-1024')
    lines = response['Body'].read().decode('utf-8').splitlines()
    
    if not lines:
        raise AirflowFailException("El archivo está vacío.")

    actual_columns = [col.strip().lower() for col in next(csv.reader([lines[0]]))]
    expected_columns = [col.lower() for col in expected_columns]

    if not set(expected_columns).issubset(set(actual_columns)):
        missing = set(expected_columns) - set(actual_columns)
        raise AirflowFailException(f"Error de esquema. Faltan columnas: {missing}")
    
    print("Esquema validado correctamente.")
