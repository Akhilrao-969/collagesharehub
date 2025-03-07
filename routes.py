import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Resource
from forms import ResourceForm

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    category = request.args.get('category', None)
    condition = request.args.get('condition', None)
    search_query = request.args.get('q', None)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'newest')

    query = Resource.query

    # Apply filters
    if category:
        query = query.filter_by(subject=category)
    if condition:
        query = query.filter_by(condition=condition)
    if search_query:
        query = query.filter(
            (Resource.title.contains(search_query)) |
            (Resource.description.contains(search_query))
        )
    if min_price is not None:
        query = query.filter(Resource.price >= min_price)
    if max_price is not None:
        query = query.filter(Resource.price <= max_price)

    # Apply sorting
    if sort == 'price_low':
        query = query.order_by(Resource.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Resource.price.desc())
    else:  # newest
        query = query.order_by(Resource.created_at.desc())

    resources = query.all()
    return render_template('explore.html',
                         resources=resources,
                         category=category,
                         condition=condition,
                         search_query=search_query,
                         min_price=min_price,
                         max_price=max_price,
                         sort=sort)

@app.route('/my-listings')
@login_required
def my_listings():
    resources = Resource.query.filter_by(user_id=current_user.id).order_by(Resource.created_at.desc()).all()
    return render_template('my_listings.html', resources=resources)

@app.route('/resource/create', methods=['GET', 'POST'])
@login_required
def create_resource():
    form = ResourceForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                resource = Resource(
                    title=form.title.data,
                    description=form.description.data,
                    subject=form.subject.data,
                    condition=form.condition.data,
                    price=float(form.price.data),
                    file_path=filename,
                    user_id=current_user.id,
                    created_at=datetime.utcnow()
                )

                db.session.add(resource)
                db.session.commit()
                flash('Resource listed successfully')
                return redirect(url_for('my_listings'))
            else:
                flash('Please upload a valid image file (jpg, jpeg, or png)')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{form[field].label.text}: {error}")

    return render_template('create_resource.html', form=form)

# API endpoint for form validation
@app.route('/api/validate-form', methods=['POST'])
@login_required
def validate_form():
    form = ResourceForm()
    if form.validate_on_submit():
        return jsonify({'valid': True})
    return jsonify({
        'valid': False,
        'errors': {field: errors for field, errors in form.errors.items()}
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Welcome back!')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=request.form['email']).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        phone_number = request.form.get('phone_number', '')
        
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            phone_number=phone_number,
            created_at=datetime.utcnow()
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()

        # Log the user in after registration
        login_user(user)
        flash('Registration successful! Welcome to College Resource Hub!')
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_resources = Resource.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', resources=user_resources)


@app.route('/resource/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_resource(id):
    resource = Resource.query.get_or_404(id)

    # Check if the current user is the owner of the resource
    if resource.user_id != current_user.id:
        flash('You do not have permission to edit this resource.')
        return redirect(url_for('explore'))

    form = ResourceForm()

    if request.method == 'GET':
        # Pre-populate the form with existing data
        form.title.data = resource.title
        form.description.data = resource.description
        form.subject.data = resource.subject
        form.condition.data = resource.condition
        form.price.data = resource.price

    if request.method == 'POST' and form.validate_on_submit():
        # Update resource details
        resource.title = form.title.data
        resource.description = form.description.data
        resource.subject = form.subject.data
        resource.condition = form.condition.data
        resource.price = float(form.price.data)

        # Handle file upload if a new file is provided
        file = form.file.data
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            resource.file_path = filename

        # Check if remove image checkbox is checked
        if 'remove_image' in request.form and request.form['remove_image'] == 'yes':
            # Remove the file_path, which effectively removes the image association
            resource.file_path = None

        db.session.commit()
        flash('Resource updated successfully')
        return redirect(url_for('my_listings'))

    return render_template('edit_resource.html', form=form, resource=resource)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    resources = Resource.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        # Update phone number if provided
        if 'phone_number' in request.form:
            current_user.phone_number = request.form['phone_number']
            db.session.commit()
            flash('Profile updated successfully')
            return redirect(url_for('profile'))
    
    return render_template('profile.html', resources=resources)


@app.route('/resource/<int:id>')
def view_resource(id):
    resource = Resource.query.get_or_404(id)
    return render_template('view_resource.html', resource=resource)

@app.route('/resource/delete/<int:id>', methods=['POST'])
@login_required
def delete_resource(id):
    resource = Resource.query.get_or_404(id)

    # Check if the current user is the owner of the resource
    if resource.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Delete the resource
    db.session.delete(resource)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    resources = Resource.query.filter(
        (Resource.title.contains(query)) |
        (Resource.description.contains(query)) |
        (Resource.subject.contains(query))
    ).all()
    return render_template('index.html', resources=resources, search_query=query)

@app.route('/create-test-data')
def create_test_data():
    # Only create test data if there are no users
    if User.query.count() == 0:
        # Create test users
        test_users = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'test123',
                'created_at': datetime.utcnow()
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'test123',
                'created_at': datetime.utcnow() - timedelta(days=1)
            }
        ]

        created_users = []
        for user_data in test_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                created_at=user_data['created_at']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            created_users.append(user)

        # Create test resources with various items
        test_resources = [
            {
                'title': 'MacBook Pro 2023',
                'description': 'Like new MacBook Pro M2, perfect for programming and design work. Includes charger and protective case.',
                'subject': 'Laptops',
                'condition': 'Like New',
                'price': 1200.00,
                'user': created_users[0]
            },
            {
                'title': 'TI-84 Plus Calculator',
                'description': 'Texas Instruments graphing calculator, essential for calculus and statistics classes.',
                'subject': 'Calculators',
                'condition': 'Very Good',
                'price': 75.00,
                'user': created_users[0]
            },
            {
                'title': 'Chemistry Lab Kit',
                'description': 'Complete chemistry lab equipment set including beakers, test tubes, and safety gear.',
                'subject': 'Lab Equipment',
                'condition': 'Good',
                'price': 150.00,
                'user': created_users[1]
            },
            {
                'title': 'iPad Air 4th Gen',
                'description': 'Perfect for note-taking and digital textbooks. Comes with Apple Pencil 2.',
                'subject': 'Tablets',
                'condition': 'Very Good',
                'price': 450.00,
                'user': created_users[1]
            }
        ]

        for resource_data in test_resources:
            resource = Resource(
                title=resource_data['title'],
                description=resource_data['description'],
                subject=resource_data['subject'],
                condition=resource_data['condition'],
                price=resource_data['price'],
                user_id=resource_data['user'].id,
                created_at=datetime.utcnow()
            )
            db.session.add(resource)

        db.session.commit()
        flash('Test data created successfully!')
    else:
        flash('Test data already exists!')

    return redirect(url_for('index'))

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="Rate limit exceeded. Please try again later."), 429

# This code block is already in app.py and should not be duplicated here