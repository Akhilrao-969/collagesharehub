import os
from dotenv import load_dotenv
from datetime import datetime

def main():
    """Initialize the database and create test data."""
    # Load environment variables
    load_dotenv()

    print("Initializing test data...")

    # First create placeholder images
    print("\n=== Generating placeholder images ===")
    from static.uploads.placeholder_image import generate_placeholder_images
    generate_placeholder_images()

    # Then setup the database
    print("\n=== Setting up database ===")
    from setup_database import setup_database
    setup_database()

    print("\nSetup complete! You can now log in with:")
    print("Username: john_doe")
    print("Password: test123")
    print("\nOr:")
    print("Username: jane_smith")
    print("Password: test123")

    print("\nYou can also log in as:")
    print("Username: student_cs101")
    print("Password: college123")
    print("\nOr:")
    print("Username: prof_physics")
    print("Password: faculty456")

if __name__ == "__main__":
    main()