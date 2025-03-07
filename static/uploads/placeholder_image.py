
import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_placeholder_image(filename, text, color=None):
    """Create a placeholder image with the given text."""
    if color is None:
        # Generate a random pastel color
        r = random.randint(150, 230)
        g = random.randint(150, 230)
        b = random.randint(150, 230)
        color = (r, g, b)
    
    # Create a new image with a random pastel background
    width, height = 500, 350
    image = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, default to a simpler approach if font not available
    try:
        font = ImageFont.truetype('Arial', 30)
        draw.text((width/2, height/2), text, fill=(40, 40, 40), font=font, anchor="mm")
    except Exception:
        # If font loading fails, use a simpler approach
        draw.text((width/2 - 70, height/2 - 10), text, fill=(40, 40, 40))
    
    # Save the image
    image.save(os.path.join('static/uploads', filename))
    print(f"Created placeholder image: {filename}")

def generate_placeholder_images():
    """Generate placeholder images for the test resources."""
    # Make sure the directory exists
    os.makedirs('static/uploads', exist_ok=True)
    
    # Create placeholder images for the test resources
    placeholder_images = [
        ('macbook.jpg', 'MacBook Pro 2023'),
        ('calculator.jpg', 'TI-84 Calculator'),
        ('labkit.jpg', 'Chemistry Lab Kit'),
        ('ipad.jpg', 'iPad Air 4th Gen'),
        ('physics_books.jpg', 'Physics Textbooks'),
        ('cs_guide.jpg', 'CS Study Guide'),
        ('casio_calculator.jpg', 'Casio Calculator'),
        ('microscope.jpg', 'Microscope Set'),
        ('dell_xps.jpg', 'Dell XPS 15'),
        ('chair.jpg', 'Ergonomic Chair')
    ]
    
    # Generate random colors for each image
    colors = [
        (200, 230, 255),  # Light blue
        (255, 230, 200),  # Light orange
        (230, 255, 200),  # Light green
        (255, 200, 230),  # Light pink
        (200, 255, 230),  # Light mint
        (230, 200, 255),  # Light purple
        (240, 240, 200),  # Light yellow
        (200, 240, 240),  # Light cyan
        (240, 200, 240),  # Light magenta
        (220, 220, 220),  # Light gray
    ]
    
    for i, (filename, text) in enumerate(placeholder_images):
        create_placeholder_image(filename, text, colors[i % len(colors)])
    
    print("All placeholder images created successfully!")

if __name__ == "__main__":
    generate_placeholder_images()
