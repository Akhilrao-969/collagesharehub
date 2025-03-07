
import os
import psycopg2
from dotenv import load_dotenv

def create_database():
    """Create PostgreSQL database if it doesn't exist"""
    load_dotenv()
    
    # Get database connection details from environment variables
    db_url = os.environ.get("DATABASE_URL", "")
    
    if not db_url:
        print("No DATABASE_URL found in environment variables")
        return False
    
    # Parse the database URL to get the database name
    db_parts = db_url.split("/")
    db_name = db_parts[-1]
    
    # Create connection string to postgres database
    conn_string = "/".join(db_parts[:-1]) + "/postgres"
    
    try:
        # Connect to postgres database
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully")
        else:
            print(f"Database {db_name} already exists")
        
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
