from flask import Blueprint, render_template

# Create a blueprint for the main routes
main_bp = Blueprint('main', __name__)

# Home route to render the base.html template
@main_bp.route('/')
def home():
    return render_template('base.html')
