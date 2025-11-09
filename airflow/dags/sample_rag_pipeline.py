"""
Sample RAG Pipeline DAG for Multi-Agent System
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'rag-system',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'sample_rag_pipeline',
    default_args=default_args,
    description='Sample RAG processing pipeline',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['rag', 'sample'],
)

def check_system_health():
    """Check if all system components are healthy."""
    import requests
    
    services = {
        'api': 'http://api:8000/api/v1/health',
        'opensearch': 'http://opensearch:9200/_cluster/health',
        'langfuse': 'http://langfuse:3000/api/public/health'
    }
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✓ {service} is healthy")
            else:
                raise Exception(f"{service} returned status {response.status_code}")
        except Exception as e:
            print(f"✗ {service} health check failed: {e}")
            raise

def process_documents():
    """Sample document processing task."""
    print("Processing documents...")
    # Add your document processing logic here
    print("Documents processed successfully!")

def update_embeddings():
    """Sample embedding update task."""
    print("Updating embeddings...")
    # Add your embedding update logic here
    print("Embeddings updated successfully!")

# Define tasks
health_check = PythonOperator(
    task_id='check_system_health',
    python_callable=check_system_health,
    dag=dag,
)

process_docs = PythonOperator(
    task_id='process_documents',
    python_callable=process_documents,
    dag=dag,
)

update_emb = PythonOperator(
    task_id='update_embeddings',
    python_callable=update_embeddings,
    dag=dag,
)

cleanup = BashOperator(
    task_id='cleanup_temp_files',
    bash_command='echo "Cleaning up temporary files..." && rm -f /tmp/rag_*.tmp || true',
    dag=dag,
)

# Set task dependencies
health_check >> [process_docs, update_emb] >> cleanup