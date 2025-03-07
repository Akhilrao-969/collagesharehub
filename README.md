
# College Resource Hub

A web platform for college students to buy, sell, and exchange academic resources like textbooks, lab equipment, calculators, and other educational materials.

## Live Demo

The application is hosted at: https://mycollegeresources.vigneshchowdaryatthapatala.repl.co/

## Features

- User authentication (registration, login, logout)
- Create, edit, and delete resource listings
- Browse resources with advanced filtering and sorting options
- Upload and manage images for resources
- Responsive design that works on desktop and mobile
- User profile management

## Technologies Used

- **Backend:** Python, Flask
- **Database:** PostgreSQL (via Neon Database)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Authentication:** Flask-Login
- **ORM:** SQLAlchemy
- **Deployment:** Replit

## Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database (or you can use the online Neon database)
- Pip (Python package manager)

### Environment Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd college-resource-hub
   ```

2. Create a `.env` file in the project root with the following content:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_dPKL8YwyMZ1X@ep-little-heart-a5jbb5r3.us-east-2.aws.neon.tech/neondb?sslmode=require
   SESSION_SECRET=your-secret-key-here
   ```

   Note: For local development, you can use your own PostgreSQL database by changing the DATABASE_URL.

### Installation

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

   Required packages include:
   - Flask
   - Flask-SQLAlchemy
   - Flask-Login
   - Psycopg2-binary
   - Python-dotenv
   - Gunicorn
   - Flask-Limiter
   - Pillow

### Database Setup

1. Run the database setup script to create tables and populate with test data:
   ```
   python setup_database.py
   ```

   This will:
   - Connect to your database
   - Create all necessary tables
   - Generate test users and resource listings
   - Create placeholder images

### Running the Application

1. Start the development server:
   ```
   python main.py
   ```

2. Access the application at `http://127.0.0.1:5000`

3. For production, use Gunicorn:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Default Test Users

After running the setup script, you can log in with these credentials:

1. **Student User:**
   - Username: john_doe
   - Password: test123

2. **Another Student:**
   - Username: jane_smith
   - Password: test123

3. **CS Student:**
   - Username: student_cs101
   - Password: college123

4. **Faculty Member:**
   - Username: prof_physics
   - Password: faculty456

## Project Structure

- `app.py` - Main application configuration
- `main.py` - Application entry point
- `models.py` - Database models
- `routes.py` - API routes and views
- `forms.py` - Form definitions and validation
- `static/` - Static assets (CSS, JS, uploaded images)
- `templates/` - HTML templates
- `setup_database.py` - Database initialization script
- `init_test_data.py` - Creates test data

## API Endpoints

- `/explore` - Browse all resources with filtering
- `/my-listings` - View user's own listings
- `/resource/create` - Create a new resource
- `/resource/edit/<id>` - Edit an existing resource
- `/resource/delete/<id>` - Delete a resource
- `/search` - Search for resources
- `/profile` - User profile page
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
