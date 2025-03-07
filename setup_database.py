
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

# Get database connection string
db_url = os.environ.get("DATABASE_URL")

def setup_database():
    """Set up the database schema and populate with test data"""
    print("Setting up database...")
    
    # Connect to the database
    conn = psycopg2.connect(db_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS resource CASCADE")
    cursor.execute("DROP TABLE IF EXISTS \"user\" CASCADE")
    
    # Create user table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "user" (
        id SERIAL PRIMARY KEY,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password_hash VARCHAR(256) NOT NULL,
        phone_number VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create resource table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resource (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        subject VARCHAR(50) NOT NULL,
        condition VARCHAR(20) NOT NULL,
        price FLOAT NOT NULL,
        file_path VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER REFERENCES "user"(id) NOT NULL
    )
    """)
    
    print("Tables created successfully")
    
    # Create test users
    print("Creating test users...")
    test_users = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': generate_password_hash('test123'),
            'created_at': datetime.utcnow()
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': generate_password_hash('test123'),
            'created_at': datetime.utcnow() - timedelta(days=1)
        },
        {
            'username': 'student_cs101',
            'email': 'cs101@university.edu',
            'password': generate_password_hash('college123'),
            'created_at': datetime.utcnow() - timedelta(days=3)
        },
        {
            'username': 'prof_physics',
            'email': 'physics@faculty.edu',
            'password': generate_password_hash('faculty456'),
            'created_at': datetime.utcnow() - timedelta(days=10)
        }
    ]
    
    # Insert users
    user_ids = []
    for user in test_users:
        cursor.execute(
            """INSERT INTO "user" (username, email, password_hash, created_at) 
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (user['username'], user['email'], user['password'], user['created_at'])
        )
        user_ids.append(cursor.fetchone()[0])
    
    print(f"Created {len(user_ids)} test users")
    
    # Create test resources
    print("Creating test resources...")
    test_resources = [
        {
            'title': 'MacBook Pro 2023',
            'description': 'Like new MacBook Pro M2, perfect for programming and design work. Includes charger and protective case.',
            'subject': 'Laptops',
            'condition': 'Like New',
            'price': 1200.00,
            'file_path': 'macbook.jpg',
            'user_id': user_ids[0]
        },
        {
            'title': 'TI-84 Plus Calculator',
            'description': 'Texas Instruments graphing calculator, essential for calculus and statistics classes.',
            'subject': 'Calculators',
            'condition': 'Very Good',
            'price': 75.00,
            'file_path': 'calculator.jpg',
            'user_id': user_ids[0]
        },
        {
            'title': 'Chemistry Lab Kit',
            'description': 'Complete chemistry lab equipment set including beakers, test tubes, and safety gear.',
            'subject': 'Lab Equipment',
            'condition': 'Good',
            'price': 150.00,
            'file_path': 'labkit.jpg',
            'user_id': user_ids[1]
        },
        {
            'title': 'iPad Air 4th Gen',
            'description': 'Perfect for note-taking and digital textbooks. Comes with Apple Pencil 2.',
            'subject': 'Tablets',
            'condition': 'Very Good',
            'price': 450.00,
            'file_path': 'ipad.jpg',
            'user_id': user_ids[1]
        },
        {
            'title': 'Physics Textbook Bundle',
            'description': 'Complete set of physics textbooks covering mechanics, thermodynamics, and quantum physics. Perfect for undergraduate studies.',
            'subject': 'Textbooks',
            'condition': 'Good',
            'price': 120.00,
            'file_path': 'physics_books.jpg',
            'user_id': user_ids[2]
        },
        {
            'title': 'Computer Science Study Guide',
            'description': 'Comprehensive study materials for programming fundamentals, data structures, and algorithms.',
            'subject': 'Study Materials',
            'condition': 'Like New',
            'price': 45.00,
            'file_path': 'cs_guide.jpg',
            'user_id': user_ids[2]
        },
        {
            'title': 'Scientific Calculator Casio FX-991EX',
            'description': 'Advanced scientific calculator with 552 functions. Perfect for engineering and science courses.',
            'subject': 'Calculators',
            'condition': 'Very Good',
            'price': 30.00,
            'file_path': 'casio_calculator.jpg',
            'user_id': user_ids[3]
        },
        {
            'title': 'Microscope Set',
            'description': 'Professional biological microscope with 40X-2000X magnification. Includes slides and preparation tools.',
            'subject': 'Lab Equipment',
            'condition': 'Good',
            'price': 250.00,
            'file_path': 'microscope.jpg',
            'user_id': user_ids[3]
        },
        {
            'title': 'Dell XPS 15 Laptop',
            'description': 'Powerful laptop with 32GB RAM, 1TB SSD, and NVIDIA graphics. Excellent for engineering software and 3D modeling.',
            'subject': 'Laptops',
            'condition': 'Good',
            'price': 950.00,
            'file_path': 'dell_xps.jpg',
            'user_id': user_ids[0]
        },
        {
            'title': 'Ergonomic Desk Chair',
            'description': 'Comfortable chair with lumbar support, perfect for long study sessions.',
            'subject': 'Furniture',
            'condition': 'Very Good',
            'price': 85.00,
            'file_path': 'chair.jpg',
            'user_id': user_ids[1]
        }
    ]
    
    # Insert resources
    for resource in test_resources:
        cursor.execute(
            """INSERT INTO resource (title, description, subject, condition, price, file_path, user_id, created_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (resource['title'], resource['description'], resource['subject'], 
             resource['condition'], resource['price'], resource['file_path'], 
             resource['user_id'], datetime.utcnow())
        )
    
    print(f"Created {len(test_resources)} test resources")
    
    # Close the connection
    cursor.close()
    conn.close()
    
    print("Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()
