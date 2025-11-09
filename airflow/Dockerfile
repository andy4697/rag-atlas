# Use the official Airflow image with extended packages
FROM apache/airflow:2.10.2-python3.11

# Switch to root for system setup
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to airflow user
USER airflow

# Install additional providers if needed
RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    apache-airflow-providers-redis \
    apache-airflow-providers-http

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]