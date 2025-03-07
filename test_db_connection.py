
import os
from dotenv import load_dotenv
import psycopg2

def test_db_connection():
    # Load environment variables
    load_dotenv()
    
    # Get database connection details from environment variables
    db_url = os.environ.get("DATABASE_URL", "")
    
    if not db_url:
        print("No DATABASE_URL found in environment variables")
        return False
    
    try:
        # Connect to the database
        print(f"Attempting to connect to database using: {db_url}")
        conn = psycopg2.connect(db_url)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        print(f"Database connection successful. Test query result: {result}")
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return True
    
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
