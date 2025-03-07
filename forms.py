from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, NumberRange

class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Please enter a title"),
        Length(min=3, max=100, message="Title must be between 3 and 100 characters")
    ])
    
    subject = SelectField('Category', validators=[DataRequired()], choices=[
        ('', 'Select a category'),
        ('Laptops', 'Laptops & Computers'),
        ('Tablets', 'Tablets & E-readers'),
        ('Calculators', 'Calculators'),
        ('Textbooks', 'Textbooks'),
        ('Notes', 'Study Notes'),
        ('Study Guides', 'Study Guides')
    ])
    
    condition = SelectField('Condition', validators=[DataRequired()], choices=[
        ('', 'Select condition'),
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Fair', 'Fair')
    ])
    
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=10, max=1000, message="Description must be between 10 and 1000 characters")
    ])
    
    price = DecimalField('Price', validators=[
        DataRequired(),
        NumberRange(min=0, message="Price cannot be negative")
    ])
    
    file = FileField('Image', validators=[])
