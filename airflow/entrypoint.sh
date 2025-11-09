#!/bin/bash
set -e

# Initialize Airflow database
if [ "$1" = "webserver" ] || [ "$1" = "scheduler" ] || [ "$1" = "worker" ]; then
    echo "Initializing Airflow database..."
    airflow db init
    
    # Create default admin user if it doesn't exist
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin || true
fi

# Start the requested service
case "$1" in
    webserver)
        echo "Starting Airflow webserver..."
        exec airflow webserver --port 8080
        ;;
    scheduler)
        echo "Starting Airflow scheduler..."
        exec airflow scheduler
        ;;
    worker)
        echo "Starting Airflow worker..."
        exec airflow celery worker
        ;;
    *)
        echo "Starting Airflow standalone..."
        exec airflow standalone
        ;;
esac