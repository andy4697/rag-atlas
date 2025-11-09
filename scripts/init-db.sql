-- Initialize databases for the RAG system

-- Create Airflow database
CREATE DATABASE airflow_db;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO rag_user;

-- Create extensions for the main database
\c rag_system;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector" IF EXISTS;