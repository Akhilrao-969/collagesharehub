
import os
import sys
import logging
from app import app, db
from sqlalchemy import Column, String
from sqlalchemy.sql import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def alter_user_table():
    """Add phone_number column to the user table if it doesn't exist"""
    try:
        with db.engine.connect() as conn:
            # Check if the column already exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='phone_number'"))
            if not result.fetchone():
                # Add the phone_number column
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN phone_number VARCHAR(20)"))
                logger.info("Added phone_number column to user table")
                return True
            else:
                logger.info("phone_number column already exists in user table")
                return False
    except Exception as e:
        logger.error(f"Error altering user table: {e}")
        return False

def main():
    """Main function to update the database"""
    logger.info("Starting database update...")
    
    # Add phone_number column to user table
    if alter_user_table():
        logger.info("Database schema updated successfully")
    else:
        logger.info("No database schema changes were needed or an error occurred")
    
    logger.info("Database update completed")

if __name__ == "__main__":
    with app.app_context():
        main()
